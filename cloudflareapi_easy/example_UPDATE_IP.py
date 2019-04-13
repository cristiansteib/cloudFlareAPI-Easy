from cloudflareapi_easy import cloudflare

auth_key = 'ffffffffffffffffffff'
auth_mail = 'email@example.com'

cloudApi = cloudflare.CloudFlareApi(auth_key, auth_mail)

easyUpdate = cloudflare.EasyUpdate(cloudApi)

response = easyUpdate.update_dns_ip(dns_name='youdomain.com', newIP='1.1.1.1')

print(response)
