#!/usr/bin/env python3

import getpass
import json
import os
import boto3
import utils.const as Const
import utils.logger as Logger
from datetime import datetime

######################################
########## Global Variables ##########
######################################

# The global logger variable for Logging
logger = None

json_config_file = ".diskremconf.json"


######################################
############ My Functions ############
######################################

def logger_config():
    global logger
    # log folder path
    LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs/")

    # create log folder
    if os.path.exists(LOG_FOLDER) is False:
        os.mkdir(LOG_FOLDER)

    logger = Logger.create_logger(
        (LOG_FOLDER + datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + ".log")
    )

def retrieve_volume_ids():

    # Log a message about current process
    log("Retrieving volume IDs")

    # Retrieve json file config
    with open(f'/home/{getpass.getuser()}/{json_config_file}') as jsonfile:

        # Load the Json file
        data = json.load(jsonfile)

        # Get the volume list object
        volume_list = data["volumes"]

        # Filter detach IDs only
        detach_ids = list(map(lambda v : v['id'], volume_list))

        # Filter delete IDs only
        delete_ids = [v["id"] for v in volume_list if v['delete'] == 1]

        return detach_ids, delete_ids
    
def create_ec2_client():

    # Log a message about current process
    log("Instatiating Boto3 Client")

    # Instantiate BOTO client for EC2
    ec2 = boto3.client(
        'ec2',
        region_name = "eu-west-1",
        aws_access_key_id = os.environ["ENV_AWS_ACCESS_KEY"],
        aws_secret_access_key = os.environ["ENV_AWS_SECRET_ACCESS_KEY"]
    )

    # Return the client
    return ec2

def process_volumes(client, detach_ids, delete_ids):

    # Log a message about current process
    log("Detaching volumes")
    
    if(len(detach_ids) > 0):

        # Query Detach Ids
        for id in detach_ids:
            
            # Detach the volume
            client.detach_volume(
                VolumeId = id
            )

        waiter = client.get_waiter('volume_available')

        waiter.wait(
            VolumeIds = detach_ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 15
            }
        )

    if(len(delete_ids) > 0):

        # Query Delete Ids
        for id in delete_ids:
            
            # Delete the volume
            client.delete_volume(
                VolumeId = id
            )

        waiter = client.get_waiter('volume_deleted')

        waiter.wait(
            VolumeIds = delete_ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 15
            }
        )

def log(message):
    # Logs an info message
    logger.info(message)

def debug(message):
    # Logs a debug message
    logger.debug(message)


#####################################
########### Main Function ###########
#####################################

def main():

    # Try except clause to
    # handle all possible errors in the whole script
    # to prevent crash
    try:
        # Initialize Logger
        logger_config()

        # Log the script running
        log("delete_volumes.py running...")

        # Fetch volume ids from config file
        detach_ids, delete_ids = retrieve_volume_ids()

        # Instantiate Boto3 client
        client = create_ec2_client()

        # Detach volumes
        process_volumes(client, detach_ids, delete_ids)

        # Log success message
        log("Volume processing completed on AWS")

    except Exception as e:
        error = Const.EXCEPTION_GENERAL.format(e)
        debug(error)       


if __name__ == "__main__":
    main()
