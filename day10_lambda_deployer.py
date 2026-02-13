import boto3
import zipfile
import os
from datetime import datetime

# Create clients
lambda_client = boto3.client('lambda')
s3 = boto3.client('s3')

# Your IAM role ARN
ROLE_ARN = 'arn:aws:iam::865411539109:role/lambda-basic-execution'
BUCKET_NAME = 'lambda-deploy-bucket-865411'

def create_zip(function_file):
    """Zip the Lambda function code"""
    zip_filename = 'lambda_function.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(function_file, arcname='hello_lambda.py')
    
    zip_size = os.path.getsize(zip_filename)
    print(f"✅ Created zip file: {zip_filename} ({zip_size} bytes)")
    return zip_filename

def upload_to_s3(zip_file):
    """Upload zip to S3 first"""
    key = f"lambda-deployments/{zip_file}"
    
    try:
        s3.upload_file(zip_file, BUCKET_NAME, key)
        print(f"✅ Uploaded zip to S3: s3://{BUCKET_NAME}/{key}")
        return key
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")
        return None

def deploy_lambda(function_name, s3_key):
    """Deploy Lambda function via S3"""
    
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.11',
            Role=ROLE_ARN,
            Handler='hello_lambda.lambda_handler',
            Code={
                'S3Bucket': BUCKET_NAME,
                'S3Key': s3_key
            },
            Description=f'Deployed on {datetime.now().strftime("%Y-%m-%d %H-%M")}',
            Timeout=30,
            MemorySize=128
        )
        
        print(f"✅ Lambda function '{function_name}' deployed successfully!")
        print(f"   Function ARN: {response['FunctionArn']}")
        print(f"   Runtime: {response['Runtime']}")
        print(f"   Memory: {response['MemorySize']}MB")
        print(f"   Timeout: {response['Timeout']}s")
        
    except lambda_client.exceptions.ResourceConflictException:
        print(f"Function already exists, updating code...")
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            S3Bucket=BUCKET_NAME,
            S3Key=s3_key
        )
        print(f"✅ Lambda function '{function_name}' updated successfully!")
        
    except Exception as e:
        print(f"❌ Error deploying Lambda: {e}")

def test_lambda(function_name):
    """Test the deployed Lambda function"""
    print(f"\nTesting function '{function_name}'...")
    
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse'
        )
        print(f"✅ Function executed successfully!")
        print(f"   Status: {response['StatusCode']}")
    except Exception as e:
        print(f"❌ Error testing Lambda: {e}")

def cleanup(zip_file, s3_key):
    """Clean up local and S3 files"""
    if os.path.exists(zip_file):
        os.remove(zip_file)
        print(f"🧹 Removed local zip file")
    
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"🧹 Removed S3 zip file")
    except Exception as e:
        print(f"❌ Error cleaning S3: {e}")

if __name__ == "__main__":
    function_name = input("Enter Lambda function name: ")
    
    print(f"\n🚀 Deploying Lambda function '{function_name}'...")
    print("-" * 50)
    
    # Step 1: Zip the function
    zip_file = create_zip('hello_lambda.py')
    
    # Step 2: Upload to S3
    s3_key = upload_to_s3(zip_file)
    if s3_key is None:
        print("❌ Deployment cancelled")
        exit()
    
    # Step 3: Deploy from S3
    deploy_lambda(function_name, s3_key)
    
    # Step 4: Test it
    test_choice = input("\nTest the function? (yes/no): ")
    if test_choice.lower() == 'yes':
        test_lambda(function_name)
    
    # Step 5: Cleanup
    cleanup(zip_file, s3_key)
    
    print("\n✅ Done!")