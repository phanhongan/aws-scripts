import os
import sys

import boto3
from dotenv import load_dotenv


def start_ec2_instance(instance_id):
    # Create a session using your AWS credentials
    session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                            region_name=os.getenv('AWS_REGION'))

    # Create an EC2 resource object
    ec2_resource = session.resource('ec2')

    # Start the EC2 instance
    instance = ec2_resource.Instance(instance_id)
    print(f"Starting EC2 instance {instance.id}...")
    instance.start()

    # Wait for the instance to enter the running state
    instance.wait_until_running()

    print(f"EC2 instance {instance.id} has been started.")


def stop_ec2_instance(instance_id):
    # Create a session using your AWS credentials
    session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                            region_name=os.getenv('AWS_REGION'))

    # Create an EC2 resource object
    ec2_resource = session.resource('ec2')

    # Stop the EC2 instance
    instance = ec2_resource.Instance(instance_id)
    instance.stop()

    # Wait for the instance to enter the stopped state
    instance.wait_until_stopped()

    print(f"EC2 instance {instance.id} has been stopped.")


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get instance_id from sys.argv
    if len(sys.argv) < 3:
        print("Please provide the instance ID and action (start/stop) as arguments.")
        return

    instance_id = sys.argv[1]
    action = sys.argv[2]

    if action == 'start':
        start_ec2_instance(instance_id)
    elif action == 'stop':
        stop_ec2_instance(instance_id)
    else:
        print("Invalid action. Please choose either 'start' or 'stop'.")


if __name__ == '__main__':
    main()
