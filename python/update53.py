#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from requests import get
import boto3
import json
from botocore.exceptions import ClientError as BotoClientError
import argparse
import datetime

__version__ = '0.3'
__author__ = 'Victor GRENU'
__license__ = "GPLv3+"
__maintainer__ = "Victor GRENU"
__email__ = "victor.grenu@gmail.com"

# GetIp Fonction
def getIp():
	'''Simple function to get your ip, using ipinfo.co
	API and JSON and then update your AWS Route53 DNS A Record'''

	return(get(('http://ipinfo.io')).json()['ip'])

# Arguements Parser
parser = argparse.ArgumentParser(description="Update your AWS Route53 A record and S3 Bucket Policy with your new public IP address")
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

# Required args
required.add_argument('id', help='AWS Route53\'s hosted-zone-id hosting your A record')
required.add_argument('dns', help='AWS Route53\'s A record you want to update')

# Optional args
optional.add_argument('-b','--b','-bucket','--bucket', dest='bucket', help='S3 Bucket Name to update permissions (Bucket Policy)')
optional.add_argument('-v', '--version', action='version', version="%(prog)s - "+ __version__ +"")

args = vars(parser.parse_args())

# Missing Args Checker
if not args['id']:
	parser.print_help()
	exit(1)
	
if not args['dns']:
	parser.print_help()
	exit(1)

# Variables
r53 = boto3.client('route53')
hostedZoneId = args['id']
currentIp = getIp()
date = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
myRecord = args['dns']

# Check Hosted Zone ID
try:
	hz = r53.get_hosted_zone(
		Id=hostedZoneId,
	)

except BotoClientError:
	print(date + " - Hosted-Zone-ID " + hostedZoneId + " is incorrect.")
	exit(1)

# Get old IP from API Call (not DNS resolution)
try:
  record = r53.list_resource_record_sets(
    HostedZoneId=hostedZoneId,
    StartRecordType='A',
    StartRecordName=myRecord,
    MaxItems="1"
)

except BotoClientError:
	print(date + " - A Record " + myRecord + " does not exist.")
	exit(1)
	
# Set Variable oldIP
oldIp = record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

# Try to update route53
try:
  if oldIp != currentIp:

    input = r53.change_resource_record_sets(
      HostedZoneId=hostedZoneId,
      ChangeBatch={
          'Comment': date,
          'Changes': [
              {
                  'Action': 'UPSERT',
                  'ResourceRecordSet': {
                      'Name': myRecord,
                      'Type': 'A',
                      'TTL': 60,
                      'ResourceRecords': [
                          {
                              'Value': currentIp
                          },
                          ],
                  },
              },
              ]
      }
  )
    print(date + " - Current IP: " +currentIp+ " was successfully updated to Route53")
    
  else:
    print(date + " - Current IP: " +currentIp+ " is equal to old IP: " +oldIp+ ". Nothing to do with Route53.")
  
except BotoClientError:
		print(date + " - Malformed IP Address:", currentIp)
		exit(1)

# Try to update bucket policy
try:
  if oldIp != currentIp:
    s3 = boto3.client('s3')
    bucket_name = args['bucket']
    # Create the bucket policy
    bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': "arn:aws:s3:::%s/*" % bucket_name,
        'Condition': {
                'IpAddress': {
                    'aws:SourceIp': [
                        ''+ currentIp + '/32'
                    ]
                }
            }
      }]
    }

    # Convert the policy to a JSON string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy on the given bucket
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    print(date + " - Bucket Policy of S3 Bucket: " +bucket_name+ " was successfully updated")
  else:
    print(date + " - Current IP: " +currentIp+ " is equal to old IP: " +oldIp+ ". Nothing to do with the S3 bucket policy.")
    
except BotoClientError:
		print(date + " - Malformed Bucket Name:", bucket_name)
		exit(1)
exit(0)
