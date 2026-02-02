import boto3

IAM = boto3.client('iam')

def list_users():
    """List IAM users with specified attributes."""
    try:
        print("Listing IAM users...")
        response = IAM.list_users()
        users = response['Users']
        
        for user in users:
            print(f"Username: {user.get('UserName')}, "
                  f"CreateDate: {user.get('CreateDate')}, "
                  f"PasswordLastUsed: {user.get('PasswordLastUsed')}")
                  
    except Exception as e:
        print(f"Error listing IAM users: {e}")

if __name__ == "__main__":
    list_users()
