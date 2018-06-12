# update53 - DynDNS with Route53

Update AWS Route53 DNS Record with your current public IP (Usefull for home ISP with non-static IP address)

Adaptation from: [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)


## Requierements

- boto3
- AccessKey/SecretKey

## Installation

This version allow you to update your AWS route53 record from your current public ip (from [ipinfo.io](https://ipinfo.io/) WebService)

- `git clone https://github.com/z0ph/update53-pub.git`
- Create your AWS Route 53 Zone first, and then your DNS A Record to update (home.example.com)
- Configure your server with AWS CLI : `aws configure` with your Access Key ID / Secret Access ID

## Usage

python update53.py HOSTED_ZONE_ID YOUR_DNS

Example: `python update53.py ZLJT68NZ2IYSF home.example.com`

## Run

- Schedule this script with cron to update record on a daily basis for example.
- `crontab -e` to schedule your job : 

`0 * * * * python /home/user/update53-pub/update53.py hosted-zone-id home.example.com`