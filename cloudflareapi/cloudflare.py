from typing import Optional

import requests
import logging
import json

logger = logging.getLogger(__name__)


class CloudFlareApi:
    ENDPOINT = 'https://api.cloudflare.com/client/v4/'

    def __init__(self, auth_key, auth_mail):
        self.x_auth_key = auth_key
        self.x_auth_mail = auth_mail

    def __call_api(self, url, method='GET', data: Optional[dict] = None):
        try:
            headers = {
                'User-Agent': 'DebuguearApi-Browser',
                'X-Auth-Email': self.x_auth_mail,
                'X-Auth-Key': self.x_auth_key,
                'Content - Type': 'application / json'
            }

            response = requests.request(
                method=method,
                url=f"{self.ENDPOINT}{url}",
                headers=headers,
                data=json.dumps(data))
            return response

        except Exception as e:
            logger.error("Calling API: " + str(e))
            raise e

    def list_zones(self):
        return self.__call_api('/zones', method='GET').json()

    def get_zones_mapped_by_name(self) -> dict:
        result = self.list_zones()
        zones = {}
        if result['success']:
            for zone in result['result']:
                zones[zone['name']] = zone['id']
        else:
            logger.error(result)
        return zones

    def __zone_dns_records(self, zone, dns, **kwargs):
        return self.__call_api(f'zones/{zone}/dns_records/{dns}', **kwargs)

    def list_dns_records(self, id_zone) -> list:
        return self.__call_api(f'zones/{id_zone}/dns_records', method='GET').json()['result']

    def dns_records_detail(self, id_dns, id_zone):
        return self.__zone_dns_records(id_zone, id_dns, method='GET')

    def update_dns_record(self, id_dns, data, id_zone):
        return self.__zone_dns_records(id_zone, id_dns, method='PUT', data=data)
