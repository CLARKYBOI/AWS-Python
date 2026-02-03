import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=24)

instance_id = input("Enter the EC2 Instance ID to fetch CPU Utilization metrics: ")

response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance_id
        },
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=3600,
    Statistics=['Average'],
)

print(f"\nCPU Utilization metrics for EC2 Instance ID: {instance_id} in the last 24 hours:")
print("-" * 60)

if response['Datapoints']:
    for data_point in sorted(response['Datapoints'], key=lambda x: x['Timestamp']):
        print(f"Timestamp: {data_point['Timestamp']}, Average CPU Utilization: {data_point['Average']:.2f}%")
else:
    print("No CPU Utilization data found for the specified instance in the last 24 hours.")    