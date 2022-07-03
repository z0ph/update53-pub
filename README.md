# update53 - DynDNS with Amazon Route53

This version allow you to update your Amazon Route53 record by your current public ip (from [ipinfo.io](https://ipinfo.io/) web service)

**Features:**

- Update Amazon Route53 DNS Record with your current public IP (Useful for home ISP with non-static IP address)
- Optional - Send SNS Notification when your ip change
- Optional - Update the bucket policy of a S3 bucket to only authorize access to this bucket from your public IP (Useful for private static web hosting)

## Requirements

- AWS SDK for Python - [boto3](https://github.com/boto/boto3) `sudo pip install boto3`
- IAM Role attached to your EC2 instance or IAM User with AccessKey/SecretKey
- SNS Topic (Alerting purpose)
- Run `aws configure` to setup at least the region and your AK/SK

## Installation

- Create your Amazon Route 53 Zone first, then create your DNS A Record to update (`home.example.com`)
- Configure your server with AWS CLI : `aws configure` with your `AccessKey` and `SecretKey`

        $ git clone https://github.com/z0ph/update53-pub.git
        $ cd update53-pub/python/
        $ sudo pip install -r requirements.txt

## Usage

        $ python3 update53.py [YOUR_HOSTED_ZONE_ID] [YOUR_DNS]

### Optional

- Use this option to change your bucket policy to only allow your new IP: `"Action": "s3:GetObject"` `-b [YOUR_BUCKET_NAME]`
- Setup your [`sns_topic`](https://github.com/z0ph/update53-pub/blob/master/python/update53.py)

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
          "aws:SourceIp": ["130.211.YY.XXX/32"]
        }
      }
    }
  ]
}
```

#### Example with only Route53

Run `python3 update53.py ZLJT68NZ2IYSF home.example.com`

#### Example with S3 Bucket

Run `python3 update53.py ZLJT68NZ2IYSF home.example.com -b privatewebsite.example.com`

## Automation

- Schedule this script with cron to update record on a daily basis for example.
- `crontab -e` to schedule your job :

`0 * * * * python3 /home/user/update53-pub/python/update53.py ZLJT68NZ2IYSF home.example.com`

## Credits

Adaptation from:

- [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)
