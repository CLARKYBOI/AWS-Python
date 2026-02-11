import boto3
from datetime import datetime, timedelta, timezone

s3 = boto3.client('s3')

def delete_old_files(bucket_name, days_old=30):
    """Delete files older than specified days from the S3 bucket."""
    print(f"Scanning bucket '{bucket_name}' for files older than {days_old} days...")
    days_old = int(days_old)
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=days_old)

    print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response:
            print(f"No files found in bucket '{bucket_name}'.")
            return  
        
    except Exception as e:
        print(f"Error accessing bucket: {e}")
        return
    
    old_files = []

    for obj in response['Contents']:
        file_key = obj['Key']
        last_modified = obj['LastModified']

        if last_modified < cutoff_date:
            old_files.append({
                'Key': file_key,
                'LastModified': last_modified,
                'Size': obj['Size']
            })

    if not old_files:
        print(f"No files older than {days_old} days found in bucket '{bucket_name}'.")
        return
    
    print(f"\nFound {len(old_files)} file(s) to delete:")
    for file in old_files:
        print(f" - {file['Key']} (Last Modified: {file['LastModified']}.strftime('%Y-%m-%d')")

    confirm = input(f"\nDelete these {len(old_files)} file(s)? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("Deletion cancelled.")
        return  
    
    print("\nDeleting files...")
    deleted_count = 0

    for file in old_files:
        try:
            s3.delete_object(Bucket=bucket_name, Key=file['Key'])
            print(f"Deleted: {file['Key']}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {file['Key']}: {e}")
    print(f"\nDeletion complete. {deleted_count} file(s) deleted.")


if __name__ == "__main__":
    bucket = input("Enter the S3 bucket name to clean up: ")
    days = input("Enter the age threshold in days (default 30): ").strip()
    delete_old_files(bucket, days)