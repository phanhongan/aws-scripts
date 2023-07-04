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


def modify_instance_type(instance_id, new_instance_type):
    # Create a session using the loaded credentials and region
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )

    # Create an EC2 client using the session
    ec2_client = session.client('ec2')

    # Update the instance type
    response = ec2_client.modify_instance_attribute(
        InstanceId=instance_id,
        InstanceType={
            'Value': new_instance_type
        }
    )

    # Check if the modification was successful
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Successfully modified instance type to ' + new_instance_type)
    else:
        print('Failed to modify instance type.')


def main(instance_id, new_instance_type):
    modify_instance_type(instance_id, new_instance_type)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
