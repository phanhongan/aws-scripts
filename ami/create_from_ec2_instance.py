import os
import sys

import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')


def create_ami(instance_id, ami_name):
    # Create a session using your AWS credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )

    # Create an EC2 client using the session
    ec2_client = session.client('ec2')

    # Create the AMI using the instance_id
    response = ec2_client.create_image(
        InstanceId=instance_id,
        Name=ami_name,
        Description='AMI created from EC2 instance'
    )

    # Get the AMI ID from the response
    ami_id = response['ImageId']

    print(f"AMI created successfully with ID: {ami_id}")


if __name__ == '__main__':
    create_ami(sys.argv[1], sys.argv[2])
