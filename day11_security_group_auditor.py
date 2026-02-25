import boto3

ec2 = boto3.client('ec2')

def audit_security_groups():
    """Audit security groups for overly permissive rules"""
    print("🔍 Auditing security groups for overly permissive rules...")
    print("-" * 60)
    
    # Gets all security groups in the account
    response = ec2.describe_security_groups()
    security_groups = response['SecurityGroups']

    print(f"Found {len(security_groups)} security groups.\n")

    issues_found = []

    for sg in security_groups:
        group_id = sg['GroupId']
        group_name = sg['GroupName']
        print(f"Checking Security Group: {group_name} ({group_id})")

        # ← INDENT THIS! It needs to be INSIDE the for loop
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort', 'All')
            to_port = rule.get('ToPort', 'All')
            protocol = rule.get('IpProtocol', 'All')  # ← YOU FORGOT THIS LINE!
            
            for ip_range in rule.get('IpRanges', []):
                cidr = ip_range.get('CidrIp')

                if cidr == '0.0.0.0/0':
                    issue = {
                        'SecurityGroup': group_name,
                        'GroupId': group_id,
                        'Protocol': protocol,
                        'FromPort': from_port,
                        'ToPort': to_port,
                        'CIDR': cidr
                    }
                    
                    if from_port == 22:
                        issue['Severity'] = 'High - SSH open to internet'
                    elif from_port == 3389:
                        issue['Severity'] = 'High - RDP open to internet'
                    else:
                        issue['Severity'] = 'Medium - Open to internet'

                    issues_found.append(issue)  # ← INDENT THIS! Only append if 0.0.0.0/0

    # ← INDENT ALL OF THIS! It's part of the function
    print("\n" + "=" * 60)
    print("SECURITY AUDIT RESULTS")
    print("=" * 60)

    if not issues_found:
        print("✅ No overly permissive rules found!")
    else:
        print(f"⚠️  Found {len(issues_found)} security issue(s):\n")
            
        for issue in issues_found:
            print(f"Security Group: {issue['SecurityGroup']} ({issue['GroupId']})")
            print(f"  Protocol: {issue['Protocol']}")
            print(f"  Port Range: {issue['FromPort']} - {issue['ToPort']}")
            print(f"  Open to: {issue['CIDR']}")
            print(f"  ⚠️  {issue['Severity']}")
            print("-" * 60)

if __name__ == "__main__":
    audit_security_groups()
