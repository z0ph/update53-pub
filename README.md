# update53-pub
Update Route 53 DNS Record with your current public IP (Usefull for home setupbox with non-static IP address from your ISP)

Adaptation from : [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)

## Install (Update53-pub.sh)

- git clone https://github.com/z0ph/update53-pub.git
- Create your Route 53 Zone, and your DNS A Record to update
- Configure your server with AWS CLI or a role to update route53

## Install (Update53-EC2pub.sh)

This variant is for AWS EC2 Usage Only, it is usefull if you have an ASG, and you don't want to setup an ALB/ELB (Cost Saving).
With this script, it will get the current IPv4 public IP from instance metadata, and update your DNS record acordingly.

- git clone https://github.com/z0ph/update53-pub.git
- Create your Route 53 Zone, and your DNS A Record to update
- Configure your server with AWS CLI or a role to update route53
- Upload your `update-route53-A.json` and `update53-EC2pub.sh` to an S3 bucket (tar.bz2 for example)
- Setup your Launch Configuration of your ASG with the following UserData:

``` bash
/usr/bin/aws s3 cp  s3://YOU_S3_BUCKET/update53.tar.bz2  /home/ec2-user/
tar xjvf /home/ec2-user/update53.tar.bz2 -C /home/ec2-user/
rm /home/ec2-user/update53.tar.bz2
/bin/sh /home/ec2-user/update53/update.sh >> /home/ec2-user/update53.log
rm -rf /home/ec2-user/update53/
```

## Config

Edit `update53-pub.sh` and `update-route53-A.json`

Change with your values in `update53-pub.sh`: 

- `YOU_DNS_A_RECORD_NAME` : Line 7 - Example: home.mydomain.com
- `YOUR_PARENT_DNS_NAME` : Line 15 - Example: mydomain.com

Change with your values in `update-route53-A.json`:

- `YOUR_DNS_A_RECORD_NAME` : Line 7 - Example: home.mydomain.com

## Run

- `chmod +x update53-pub.sh`
- Schedule this script with cron to update record on a daily basis for example.
