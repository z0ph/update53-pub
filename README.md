# DynDNS - update53 

Update AWS Route 53 DNS Record with your current public IP (Usefull for home ISP with non-static IP address)

Adaptation from: [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)

There is two versions: 
- Update53-pub.sh to update form a Linux box, RaspberryPi, macOS...
- Update53-EC2pub.sh to update from EC2 instance: please follow this [installation instructions](EC2-Install.md)

## Requierements

- AWSCLI
- dig (dnsutils)

## Installation (Update53-pub.sh version)

This version allow you to update your aws route53 record from your current public ip (from ifconfig.co webservice)

- `git clone https://github.com/z0ph/update53-pub.git`
- Create your AWS Route 53 Zone, and your DNS A Record to update (home.example.com)
- Configure your server with AWS CLI : `aws configure` with your AccessKey

## Config

Edit `update53-pub.sh` and `update-route53-A.json`

Change with your values in `update53-pub.sh`: 

- `YOU_DNS_A_RECORD_NAME` : Line 7 - Example: home.example.com
- `YOUR_PARENT_DNS_NAME` : Line 15 - Example: example.com

Change with your values in `update-route53-A.json`:

- `YOUR_DNS_A_RECORD_NAME` : Line 7 - Example: home.example.com

## Run

- `chmod +x update53-pub.sh`
- Schedule this script with cron to update record on a daily basis for example.