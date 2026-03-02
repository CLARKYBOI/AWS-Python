import boto3
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("aws_security.log"),
        logging.StreamHandler()
        ]
)

logger = logging.getLogger(__name__)

ec2 = boto3.client('ec2')

def validate_instance_id(instance_id):
    """Validate instance ID format"""
    if not instance_id or not instance_id.startswith('i-'):
        logger.error(f"Invalid instance ID format: {instance_id}")
        return False
    return True

def create_snapshot(instance_id):
    """Create a snapshot of the specified EC2 instance."""
    logger.info(f"Finding volumes for instance {instance_id}...")

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
        logger.warning(f"Error describing volumes: {e}")
        return

    volumes = volumes_response['Volumes']

    if not volumes:
        logger.warning(f"No volumes found for instance {instance_id}.")
        return
    
    logger.info(f"Found {len(volumes)} volume(s) for instance {instance_id}. Creating snapshots...")

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
            logger.info(f"Created snapshot {snapshot_id} for volume {volume_id}.")

            ec2.create_tags(
                Resources=[snapshot_id],
                Tags=[
                    {'Key': 'Name','Value': f'Backup-{instance_id}-{timestamp}'},
                    {'Key': 'InstanceId','Value': instance_id},
                    {'Key': 'CreatedBy','Value': 'EC2 Backup Script'},
                    {'Key': 'VolumeId','Value': volume_id}
                ]
            )
            logger.info(f"Tagged snapshot {snapshot_id} with metadata.")

        except Exception as e:
            logger.error(f"Error creating snapshot for {volume_id}: {e}")


            
if __name__ == "__main__":
    instance_id = input("Enter the EC2 instance ID to back up: ")
    create_snapshot(instance_id)
