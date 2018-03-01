# DynDNS - update53 

Update AWS Route 53 DNS Record with your current public IP (Usefull for home ISP with non-static IP address)

Adaptation from: [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)

There is two versions: 
- Update53-pub.sh to update form a Linux box, RaspberryPi, macOS...
- Update53-EC2pub.sh to update from EC2 instance

## Requierements

- AWSCLI
- dig (dnsutils)

## Installation (Update53-EC2pub.sh version)

This variant is for AWS EC2 Usage **Only**, it's usefull if you have an AutoScalingGroup (ASG), and you don't want to setup an ALB/ELB (Cost Saving).
With this script, it will get the current IPv4 public IP from instance metadata, and update your route53 DNS record acordingly.

- `git clone https://github.com/z0ph/update53-pub.git` (on your EC2 instance)
- Create your Route 53 Zone, and your DNS A Record to update
- Create a S3 bucket for your artifacts on the same AWS region
- Configure your server with AWS CLI or a role to update route53 and read access to your bucket
- Upload your `update-route53-A.json` and `update53-EC2pub.sh` to an S3 bucket (in a tar.bz2 for example)
- Setup your Launch Configuration of your ASG with the following UserData:

``` bash
#!/bin/bash
/usr/bin/aws s3 cp  s3://YOU_S3_BUCKET/update53.tar.bz2  /home/ec2-user/
tar xjvf /home/ec2-user/update53.tar.bz2 -C /home/ec2-user/
rm /home/ec2-user/update53.tar.bz2
/bin/sh /home/ec2-user/update53/Update53-EC2pub.sh >> /home/ec2-user/update53.log
rm -rf /home/ec2-user/update53/
```

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