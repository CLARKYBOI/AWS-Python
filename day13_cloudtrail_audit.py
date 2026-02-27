import boto3
from datetime import datetime

def check_cloudtrail():
    """Check if CloudTrail is enabled in the account"""
    print("🔍 Checking CloudTrail configuration...")
    print("=" * 60)

    cloudtrail = boto3.client('cloudtrail')

    try:
        response = cloudtrail.describe_trails()
        trails = response['trailList']

        if not trails:
            print("❌ No CloudTrail trails found! This is a critical security risk.")
            print("   CloudTrail is NOT enabled in this account.")
            return False
        
        print(f'✅ Found {len(trails)} CloudTrail trail(s):')
        return trails
    
    except Exception as e:
        print(f"Error checking CloudTrail: {e}")
        return False
    

def analyze_trail(trail):
    """Analyze a single CloudTrail trail for security best practices"""
    
    cloudtrail = boto3.client('cloudtrail')

    trail_name = trail['Name']
    s3_bucket = trail.get('S3BucketName', 'N/A')

    print (f" Trail: {trail_name}")
    print("-" * 60)
    print(f" S3 Bucket: {s3_bucket}")

    is_multi_region = trail.get('IsMultiRegionTrail', False)

    if is_multi_region:
        print(" Multi-Region Trail: ✅")
    else:
        print(" Multi-Region Trail: ❌ This trail is not multi-region, which may miss important events in other regions.")

    log_validation = trail.get('LogFileValidationEnabled', False)

    if log_validation:
        print(" Log File Validation: ✅")
    else:
        print(f" Log File Validation: ❌ This trail does not have log file validation enabled, which can help detect tampering with logs.")

    kms_key = trail.get('KmsKeyId')
    if kms_key:
        print(f" KMS Key: {kms_key} (✅ Logs are encrypted with KMS)")
    else:
        print(" KMS Key: N/A")
              
    print()

def provide_recommendations(trails):
    """Provide recommendations based on the CloudTrail configuration"""
    print("=" * 60)
    print("SECURITY RECOMMENDATIONS")
    print("=" * 60)

    recommendations = []

    for trail in trails:
        trail_name = trail['Name']

        if not trail.get('IsMultiRegionTrail', False):
            recommendations.append(
                f" Consider enabling multi-region logging for trail '{trail_name}' to ensure comprehensive coverage across all regions."
            )

        if not trail.get('LogFileValidationEnabled', False):
            recommendations.append(
                f" Enable log file validation for trail '{trail_name}' to help detect any tampering with your logs."
            )

        if not trail.get('KmsKeyId'):
            recommendations.append(
                f" Consider encrypting logs with a KMS key for trail '{trail_name}' to enhance security."
            )

    if recommendations:
        print("\n Issues found:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("✅ No issues found with CloudTrail configuration. Keep up the good work!")

    print("\n" + "=" * 60)

def audit_cloudtrail():
    """Main function to audit CloudTrail configuration"""
    print("\n🔍 CloudTrail Security Audit")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    trails = check_cloudtrail()

    if not trails:
        print("\n CloudTrail is not configured!")
        print("CloudTrail should be enabled for:")
        print("  • Security monitoring")
        print("  • Compliance requirements")
        print("  • Incident response")
        print("  • Audit trails")
        return

    print("Analyzing trail configuration...\n")
    for trail in trails:
        analyze_trail(trail)

    provide_recommendations(trails)

if __name__ == "__main__":
    audit_cloudtrail()
