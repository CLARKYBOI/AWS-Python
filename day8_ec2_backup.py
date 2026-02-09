import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def create_snapshot(instance_id):
    """Create a snapshot of the specified EC2 instance."""
    print(f"Finding volumes for instance {instance_id}...")

    try:
        volumes_response = ec2.describe_volumes(
            Filters=[
                {
                    'Name': 'attachment.instance-id', 
                    'Values': [instance_id]
                }
            ]   
        )   
    except Exception as e:
        print(f"Error describing volumes: {e}")
        return

    volumes = volumes_response['Volumes']

    if not volumes:
        print(f"No volumes found for instance {instance_id}.")
        return
    
    print(f"Found {len(volumes)} volume(s) for instance {instance_id}. Creating snapshots...")

    for volume in volumes:
        volume_id = volume['VolumeId']

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        description = f"Backup of {volume_id} from instance {instance_id} on {timestamp}"

        try:
            snapshot_response = ec2.create_snapshot(
                VolumeId=volume_id,
                Description=description
            )   
            snapshot_id = snapshot_response['SnapshotId']
            print(f"Created snapshot {snapshot_id} for volume {volume_id}.")

        except Exception as e:
            print(f"Error creating snapshot for {volume_id}: {e}")

    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {'Key': 'Name','Value': f'Backup-{instance_id}-{timestamp}'},
            {'Key': 'InstanceId','Value': instance_id},
            {'Key': 'CreatedBy','Value': 'EC2 Backup Script'},
            {'Key': 'VolumeId','Value': volume_id}
        ]
    )
    print(f"Tagged snapshot {snapshot_id} with metadata.")


if __name__ == "__main__":
    instance_id = input("Enter the EC2 instance ID to back up: ")
    create_snapshot(instance_id)
