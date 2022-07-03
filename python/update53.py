#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from requests import get
import boto3
import json
from botocore.exceptions import ClientError as BotoClientError
import argparse
import datetime
import logging

__version__ = "0.4"
__author__ = "Victor GRENU"
__license__ = "GPLv3+"
__maintainer__ = "Victor GRENU"
__email__ = "victor.grenu@gmail.com"

# Logging configuration
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# GetIp Fonction
def getIp():
    """Simple function to get your ip, using ipinfo.co
    API and JSON and then update your AWS Route53 DNS A Record"""

    return get(("https://ipinfo.io")).json()["ip"]


# Arguements Parser
parser = argparse.ArgumentParser(
    description="Update your AWS Route53 A record and S3 Bucket Policy with your new public IP address"
)
parser._action_groups.pop()
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required args
required.add_argument("id", help="AWS Route53's hosted-zone-id hosting your A record")
required.add_argument("dns", help="AWS Route53's A record you want to update")

# Optional args
optional.add_argument(
    "-b",
    "--b",
    "-bucket",
    "--bucket",
    dest="bucket",
    help="S3 Bucket Name to update permissions (Bucket Policy)",
)
optional.add_argument(
    "-v", "--version", action="version", version="%(prog)s - " + __version__ + ""
)

args = vars(parser.parse_args())

# Missing Args Checker
if not args["id"]:
    parser.print_help()
    exit(1)

if not args["dns"]:
    parser.print_help()
    exit(1)

# Variables
r53 = boto3.client("route53")
sns = boto3.client("sns")
hostedZoneId = args["id"]
currentIp = getIp()
date = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
myRecord = args["dns"]
sns_topic = "arn:aws:sns:eu-west-1:567589703415:Alert-me"

# Check Hosted Zone ID
try:
    hz = r53.get_hosted_zone(
        Id=hostedZoneId,
    )

except BotoClientError as e:
    logging.error("Error while trying to check the R53 zone-id: %s", e)
    exit(1)

# Get old IP from API Call (not a DNS resolution)
try:
    record = r53.list_resource_record_sets(
        HostedZoneId=hostedZoneId,
        StartRecordType="A",
        StartRecordName=myRecord,
        MaxItems="1",
    )

    # Set Variable oldIP
    oldIp = record["ResourceRecordSets"][0]["ResourceRecords"][0]["Value"]

except BotoClientError as e:
    logging.error("Error while trying to check the previous record: %s", e)
    exit(1)

# Try to update route53
try:
    if oldIp != currentIp:
        message = {"Update53 - New IP set to": currentIp}
        input = r53.change_resource_record_sets(
            HostedZoneId=hostedZoneId,
            ChangeBatch={
                "Comment": date,
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": myRecord,
                            "Type": "A",
                            "TTL": 60,
                            "ResourceRecords": [
                                {"Value": currentIp},
                            ],
                        },
                    },
                ],
            },
        )
        logging.info(
            "Current IP: %s was successfully updated to R53. Old was: %s",
            currentIp,
            oldIp,
        )

        # Publish Alert to sns topic if ip change
        try:
            response = sns.publish(
                TargetArn=sns_topic,
                Message=json.dumps({"default": json.dumps(message)}),
                MessageStructure="json",
            )
        except BotoClientError as e:
            logging.error("Failed to publish message on the SNS Topic: %s", e)

    else:
        logging.info(
            "Current IP: %s, is equal to old IP: %s. Nothing to do with r53",
            currentIp,
            oldIp,
        )

except BotoClientError as e:
    logging.error("Mailformed IP Address: %s. Error: %s", oldIp, e)
    exit(1)

# Try to update bucket policy
try:
    if oldIp != currentIp:
        s3 = boto3.client("s3")
        bucket_name = args["bucket"]
        # Create the bucket policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": "arn:aws:s3:::%s/*" % bucket_name,
                    "Condition": {
                        "IpAddress": {"aws:SourceIp": ["" + currentIp + "/32"]}
                    },
                }
            ],
        }

        # Convert the policy to a JSON string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy on the given bucket
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        logging.info("Bucket Policy was successfully updated on: %s", bucket_name)
    else:
        logging.info(
            "Current IP: %s, is equal to old IP: %s, nothing to do with the S3 Bucket.",
            currentIp,
            oldIp,
        )

except BotoClientError as e:
    logging.error("Failed to update bucket policy: %s", e)
    exit(1)
exit(0)
