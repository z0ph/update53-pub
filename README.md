# update53-pub
Update Route 53 DNS Record with your current public IP (Usefull for home setupbox with non-static IP address from your ISP)

## Install

- git clone https://github.com/z0ph/update53-pub.git
- Create your Route 53 Zone, and your DNS A Record to update
- Configure your server with AWS CLI or a role to update route53


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
