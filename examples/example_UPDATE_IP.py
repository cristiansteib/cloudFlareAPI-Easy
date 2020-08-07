from cloudflareapi import cloudflare
from cloudflareapi.ip_update import IpUpdater

auth_key = 'AUTH-KEY'
auth_mail = 'CLOUDFLARE_USER_EMAIL'

cloudApi = cloudflare.CloudFlareApi(auth_key, auth_mail)

easyUpdate = IpUpdater(cloudApi)

_, response = easyUpdate.update_dns_ip(dns_name='YOUR-DOMAIN', new_ip='1.1.1.1')

print(response)
