import boto3
ec2 = boto3.client('ec2')

response = ec2.describe_instances()

print("Existing EC2 Instances:")
print("-" * 60)
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        launch_time = instance['LaunchTime']
        print(f"Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"State: {state}")
        print(f"Launch Time: {launch_time}")
        print("-" * 60)