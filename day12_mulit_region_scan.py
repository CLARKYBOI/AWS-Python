import boto3 
from datetime import datetime



def get_all_regions():
    """Get a list of all AWS regions"""
    ec2 = boto3.client('ec2', region_name='us-east-1')  # ← SPECIFY A REGION
    response = ec2.describe_regions() # Returns a dictionary with a key 'Regions' that contains a list of region info
    region_names = [region['RegionName'] for region in response['Regions']] # Returns a list
    return region_names

def scan_region(region_name):
    """Scan a specific region for security issues"""
    results = {
        'Region': region_name,
        'ec2_instances': [],
        'rds_databases': [],
    }

    try:

        ec2 = boto3.client('ec2', region_name=region_name)

        response = ec2.describe_instances()

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                results['ec2_instances'].append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                })

    except Exception as e:
        print(f"Error scanning EC2 in {region_name}: {e}")

    try:

        rds = boto3.client('rds', region_name=region_name)

        response = rds.describe_db_instances()

        for db in response['DBInstances']:
            results['rds_databases'].append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'DBInstanceClass': db['DBInstanceClass'],
                'Engine': db['Engine'],
                'Status': db['DBInstanceStatus'],
            })

    except Exception as e:
        print(f"Error scanning RDS in {region_name}: {e}")

    return results

def scan_all_regions():
    """Scan all regions and compile results"""
    print("🔍 Multi-Region Security Scan")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get all regions
    print("\nGetting list of AWS regions...")
    regions = get_all_regions()
    print(f"Found {len(regions)} regions to scan\n")
    
    # Track totals
    total_ec2 = 0
    total_rds = 0
    regions_with_resources = []
    
    # Scan each region
    for region in regions:
        print(f"Scanning {region}...", end=" ")
        
        results = scan_region(region)
        
        ec2_count = len(results['ec2_instances'])
        rds_count = len(results['rds_databases'])
        total_ec2 += ec2_count
        total_rds += rds_count
        
        if ec2_count > 0 or rds_count > 0:
            print(f"✅ Found {ec2_count} EC2, {rds_count} RDS")
            regions_with_resources.append(results)
        else:
            print("(empty)")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SCAN RESULTS")
    print("=" * 60)
    print(f"Total EC2 Instances: {total_ec2}")
    print(f"Total RDS Databases: {total_rds}")
    print(f"Regions with resources: {len(regions_with_resources)}/{len(regions)}")
    
    # Print detailed results
    if regions_with_resources:
        print("\n" + "=" * 60)
        print("DETAILED FINDINGS")
        print("=" * 60)
        
        for region_data in regions_with_resources:
            print(f"\n📍 Region: {region_data['Region']}")
            print("-" * 60)
            
            if region_data['ec2_instances']:
                print("  EC2 Instances:")
                for instance in region_data['ec2_instances']:
                    print(f"    • {instance['InstanceId']} ({instance['InstanceType']}) - {instance['State']}")
            
            if region_data['rds_databases']:
                print("  RDS Databases:")
                for db in region_data['rds_databases']:
                    print(f"    • {db['DBInstanceIdentifier']} ({db['Engine']}) - {db['Status']}")
    else:
        print("\n✅ No resources found in any region!")

if __name__ == "__main__":
    scan_all_regions()
