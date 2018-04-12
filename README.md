# update53 - DyDNS with Route53

Update AWS Route53 DNS Record with your current public IP (Usefull for home ISP with non-static IP address)

Adaptation from: [Lambros Petrou](https://www.lambrospetrou.com/articles/aws-update-route53-recordset-diy-load-balancer/)

There is two versions: 
- Update53-pub.sh to update form a Linux box, RaspberryPi, macOS...
- Update53-EC2pub.sh to update from EC2 instance: please follow this [installation instructions](EC2-Install.md)

## Requierements

- AWSCLI
- dig (dnsutils)

## Installation (Update53-pub.sh version)

This version allow you to update your AWS route53 record from your current public ip (from ifconfig.co webservice)

- `git clone https://github.com/z0ph/update53-pub.git`
- Create your AWS Route 53 Zone first, and then your DNS A Record to update (home.example.com)
- Configure your server with AWS CLI : `aws configure` with your Access Key ID / Secret Access ID

## Config

Edit `config.json` file

Change with your values:

- `YOUR_DNS_A_RECORD_NAME` : Line 7 - Example: home.example.com

Edit `update53-pub.sh` file

Change `$MYJSONPATH` : Line 6 - Example: /home/zoph/update53-pub (without last `/`)

Save

## Run

- Schedule this script with cron to update record on a daily basis for example.
- `crontab -e` to schedule your job : 

`0 * * * * bash /home/user/update53-pub/update53-pub.sh`