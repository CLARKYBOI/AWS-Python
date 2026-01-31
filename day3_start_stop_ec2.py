import boto3

ec2 = boto3.client('ec2')

def start_instance(instance_id):
    """Start an EC2 instance given its instance ID."""
    print(f"Starting instance {instance_id}...")
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(f" Instance {instance_id} is starting.")
        return response
    except Exception as e:
        print(f" Error: {e}")

def stop_instance(instance_id):
    """Stop an EC2 instance given its instance ID."""
    print(f"Stopping instance {instance_id}...")
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f" Instance {instance_id} is stopping.")
        return response
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    instance_id  = input("Enter instance ID: ")
    action = input("Enter action (start/stop): ").lower()

    if action == "start":
        start_instance(instance_id)
    elif action == "stop":
        stop_instance(instance_id)
    else:
        print("Invalid action. Please enter 'start' or 'stop'.")