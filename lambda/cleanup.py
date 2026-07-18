import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    print("===== Cost Optimization Cleanup Started =====")

    # Find Stopped EC2 Instances
    stopped_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )

    for reservation in stopped_instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"Stopped EC2 Found: {instance['InstanceId']}")

    # Find Unattached EBS Volumes
    volumes = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': ['available']
            }
        ]
    )

    for volume in volumes['Volumes']:
        print(f"Deleting Volume: {volume['VolumeId']}")
        ec2.delete_volume(
            VolumeId=volume['VolumeId']
        )

    # Find Unused Elastic IPs
    addresses = ec2.describe_addresses()

    for address in addresses['Addresses']:

        if 'AssociationId' not in address:

            print(f"Releasing Elastic IP: {address['PublicIp']}")

            ec2.release_address(
                AllocationId=address['AllocationId']
            )

    print("===== Cleanup Completed Successfully =====")

    return {
        'statusCode': 200,
        'body': 'Cleanup Completed'
    }
