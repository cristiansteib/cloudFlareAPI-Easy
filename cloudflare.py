'''Author: Cristian Steib date : 16/11/2016'''

import sys
import requests

class CloudFlareApi():
    def __init__(self, auth_key, auth_mail):
        # The stable HTTPS endpoint for the latest version is:
        self.endpoint = 'https://api.cloudflare.com/client/v4/'
        self.x_auth_key = auth_key
        self.x_auth_mail = auth_mail

    def __call_api(self, url, method=None, data=None):
        try:
            headers = {'User-Agent': 'DebuguearApi-Browser',
                       'X-Auth-Email': self.x_auth_mail,
                       'X-Auth-Key': self.x_auth_key,
                       'Content - Type': 'application / json'}

            if (method == 'PUT'):
                response = requests.request(method='PUT', url=self.endpoint + url, data=data, headers=headers)
                return response
            if (method == 'GET'):
                response = requests.request(method='GET', url=self.endpoint + url, headers=headers, data=data)
                return response
        except:
            print("error call api : " + str(sys.exc_info()))

    def set_id_zone(self, id_zona):
        self.id_zona = id_zona

    def list_zones(self):
        return self.__call_api('/zones', method='GET')

    def list_frindly_zones(self):
        list_zones = self.list_zones().json()
        if (list_zones['success']):
            zonas = {}
            for zone in list_zones['result']:
                zonas[zone['name']] = zone['id']
            return zonas

    def list_dns_records(self, id_zona=False):
        if (id_zona):
            # print("You can use method set_id_zone()")
            return self.__call_api('zones/' + str(id_zona) + '/dns_records', method='GET')
        else:
            if (self.id_zona):
                return self.__call_api('zones/' + str(self.id_zona) + '/dns_records', method='GET')

    def dns_records_detail(self, id_dns, id_zona=False):
        ''' Se necesita enviar un id para que retorne solo uno en especifico
            sino va a retornar lo mismo que list_dns_record'''
        if (id_zona):
            return self.__call_api('zones/' + str(id_zona) + '/dns_records/' + id_dns, method='GET')
        else:
            if (self.id_zona):
                return self.__call_api('zones/' + str(self.id_zona) + '/dns_records/' + id_dns, method='GET')

    def update_dns_record(self, id_dns, data, id_zona=False):
        if (id_zona):
            return self.__call_api('zones/' + str(id_zona) + '/dns_records/' + id_dns + '/', method='PUT', data=data)
        else:
            if (self.id_zona):
                return self.__call_api('zones/' + str(self.id_zona) + '/dns_records/' + id_dns + '/', method='PUT',
                                       data=data)


class EasyUpdate():
    def __init__(self, instanceCloudFlareApi):
        self.cloudInstace = instanceCloudFlareApi

    def update_dns_ip(self, dns_name, newIP):
        searchFor = dns_name
        dns_hit_record = {}
        try:
            zones = self.cloudInstace.list_frindly_zones()
            id_zone = zones[searchFor]
            dns_records = self.cloudInstace.list_dns_records(id_zona=id_zone).json()['result']
            for dns_record in dns_records:
                try:
                    if dns_record['name'] == searchFor:
                        dns_hit_record = dns_record
                except:
                    # miss
                    pass
            if dns_hit_record:
                id_dns = (dns_hit_record['id'])
                dns_hit_record.pop('meta')
                dns_hit_record['data'] = {}
                dns_hit_record['content'] = newIP
                # despues de aca dns_hit_record lo manejo con str

                dns_hit_record = str(dns_hit_record).replace('\'', '"')
                response = self.cloudInstace.update_dns_record(id_dns=id_dns, id_zona=id_zone, data=dns_hit_record)
                return {'error': False, 'value': response}
            else:
                return {'error': False, 'value': response}
        except (KeyError,TypeError):
            return {'error': True}


# example
# c = CloudFlareApi(auth_key, auth_mail)
# x = EasyUpdate(c)
#  ret= x.update_dns_ip('dominio.com','111.311.111.111')

