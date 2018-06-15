#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from requests import get
import boto3
from botocore.exceptions import ClientError as BotoClientError
import argparse
import datetime

__version__ = '0.1'
__author__ = 'Victor GRENU'
__license__ = "GPLv3+"
__maintainer__ = "Victor GRENU"
__email__ = "victor.grenu@gmail.com"
__status__ = "Production"

# GetIp Fonction
def getIp():
	'''Simple function to get your ip, using ipinfo.co
	API and JSON and then update your AWS Route53 DNS A Record'''

	return(get(('http://ipinfo.io')).json()['ip'])

# Arguements Parser
parser = argparse.ArgumentParser(description="Update your AWS Route53 A record with your new IP address")
parser.add_argument('-v', '--version', action='store_true', help='Print version and exit')
parser.add_argument('id', help='AWS Route53\'s hosted-zone-id hosting your A record')
parser.add_argument('dns', help='AWS Route53\'s A record you want to update')

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

#Check Hosted Zone ID
try:
	hz = r53.get_hosted_zone(
		Id=hostedZoneId,
	)

except BotoClientError:
	print("Hosted-Zone-ID " + hostedZoneId + " is incorrect.")
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
	print("A Record " + myRecord + " does not exist.")
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
    print("Current IP: " +currentIp+ " was successfully updated to Route53")
  else:
    print("Current IP: " +currentIp+ " is equal to old IP: " +oldIp+ ". Nothing to do.")
  
except BotoClientError:
		print("Malformed IP:", currentIp)
		exit(1)
exit(0)