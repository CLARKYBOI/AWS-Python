import boto3 
import os

s3 = boto3.client('s3')

def upload_file(bucket_name, file_path, object_name=None):
    """Upload a file to an S3 bucket."""

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        print(f"Uploading {file_path} to s3://{bucket_name}/{object_name}...")
        s3.upload_file(file_path, bucket_name, object_name)
        print("Upload successful.")
    except Exception as e:
        print(f"Error during upload: {e}")
def download_file(bucket_name, object_name, file_path=None):
    """Download a file from an S3 bucket."""

    try:
        print(f"Downloading s3://{bucket_name}/{object_name} to {file_path or object_name}...")
        s3.download_file(bucket_name, object_name, file_path or object_name)
        print(f"Download successful!")

    except Exception as e:
        print(f"Error during download: {e}")

if __name__ == "__main__":
    action = input("Upload or Download? (u/d): ").lower()
    bucket_name = input("Enter S3 bucket name: ")

    if action == 'u':
        file_path = input("Enter the file path to upload: ")
        upload_file(bucket_name, file_path)
    elif action == 'd':
        object_name = input("Enter the S3 object name to download: ")
        file_path = input("Enter the file path to save the downloaded file (leave blank to use object name): ")
        download_file(bucket_name, object_name, file_path if file_path else None)
    else: 
        print ("Invalid action. Please enter 'u' for upload or 'd' for download.")