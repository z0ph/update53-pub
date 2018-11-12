# update53 - DynDNS with AWS Route53

This version allow you to update your AWS route53 record from your current public ip (from [ipinfo.io](https://ipinfo.io/) WebService)

**Features:**
- Update AWS Route53 DNS Record with your current public IP (Usefull for home ISP with non-static IP address)
- Send SNS Notification when your ip change
- Optional - Update the bucket policy of a S3 bucket to only autorize access to this bucket from your public IP (Usefull for private static web hosting)

## Requierements

- AWS SDK for Python - [boto3](https://github.com/boto/boto3) `sudo pip install boto3`
- IAM Role attached to your EC2 instance or IAM User with AccessKey/SecretKey
- SNS Topic (Alerting purpose)
- Run `aws configure` to setup at least the region and your AK/SK

	$ cd python 
	$ sudo pip install -r requirements.txt

## Installation

- Create your AWS Route 53 Zone first, then create your DNS A Record to update (home.example.com)
- Configure your server with AWS CLI : `aws configure` with your AccessKey ID and SecretAccess ID

	$ git clone https://github.com/z0ph/update53-pub.git

- Setup your SNS ARN on line [113](https://github.com/z0ph/update53-pub/blob/master/python/update53.py#L113) in update53.py

## Usage

	$ python update53.py [YOUR_HOSTED_ZONE_ID] [YOUR_DNS] -b [YOUR_BUCKET_NAME]

### Optinal

`-b [YOUR_BUCKET_NAME]`     Use this option to change your bucket policy to only allow your new IP: `"Action": "s3:GetObject"`


### Example of the Bucket Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::draft.zoph.me/*",
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": [
                        "130.211.YY.XXX/32"
                    ]
                }
            }
        }
    ]
}

```

#### Example with only Route53

Run `python update53.py ZLJT68NZ2IYSF home.example.com`

#### Example with S3 Bucket 

Run `python update53.py ZLJT68NZ2IYSF home.example.com -b privatewebsite.example.com`

## Automation

- Schedule this script with cron to update record on a daily basis for example.
- `crontab -e` to schedule your job : 

`0 * * * * python /home/user/update53-pub/update53.py ZLJT68NZ2IYSF home.example.com`

## Credits

Adaptation from: [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)
