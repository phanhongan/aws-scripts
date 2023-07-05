import os
import sys

import boto3
from dotenv import load_dotenv

# Load the AWS credentials from the .env file
load_dotenv()

# Retrieve the AWS credentials from environment variables
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')


def launch_ec2_instance(ami_id):
    # Create a session using the retrieved AWS credentials
    session = boto3.Session(aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            region_name=region)

    # Create an EC2 resource using the session
    ec2_resource = session.resource('ec2')

    # Launch the EC2 instance using the AMI ID
    instances = ec2_resource.create_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1
    )

    # Get the instance ID from the launched instance
    instance_id = instances[0].id

    print(f"EC2 instance launched successfully with ID: {instance_id}")


if __name__ == '__main__':
    launch_ec2_instance(sys.argv[1])
