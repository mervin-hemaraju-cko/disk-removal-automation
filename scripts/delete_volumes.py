#!/usr/bin/env python3
import getpass
import json
import os
import boto3

json_config_file = ".diskremconf.json"

def retrieve_volume_ids():
    # Retrieve json file config
    with open(f'/home/{getpass.getuser()}/{json_config_file}') as jsonfile:
        data = json.load(jsonfile)
        return data["volumes"]
    
def create_ec2_client():

    # Instantiate BOTO client for EC2
    ec2 = boto3.client(
        'ec2',
        region_name = "eu-west-1",
        aws_access_key_id = os.environ["ENV_AWS_ACCESS_KEY"],
        aws_secret_access_key = os.environ["ENV_AWS_SECRET_ACCESS_KEY"]
    )

    # Return the client
    return ec2

def detach_volumes(client, volume_ids):
    
    # Query Ids
    for id in volume_ids:
        
        # Detach the volume
        client.detach_volume(
            VolumeId = id
        )
    
    print("Detaching volumes")

    waiter = client.get_waiter('volume_available')

    waiter.wait(
        VolumeIds = volume_ids,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts': 15
        }
    )

def delete_volumes(client, volume_ids):

    # Query Ids
    for id in volume_ids:
        
        # Delete the volume
        client.delete_volume(
            VolumeId = id
        )
    
    print("Deleting volumes")

    waiter = client.get_waiter('volume_deleted')

    waiter.wait(
        VolumeIds = volume_ids,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts': 15
        }
    )

def main():
    volume_ids = retrieve_volume_ids()

    client = create_ec2_client()

    detach_volumes(client, volume_ids)

    delete_volumes(client, volume_ids)


if __name__ == "__main__":
    main()
