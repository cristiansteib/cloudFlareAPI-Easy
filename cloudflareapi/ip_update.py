from cloudflareapi.cloudflare import CloudFlareApi


class DnsRecordNotFoundError(Exception):
    pass


class IpUpdater:

    def __init__(self, cloudflare_api: CloudFlareApi):
        self.cloudflare_api = cloudflare_api

    def update_dns_ip(self, dns_name, new_ip, dns_type='A'):

        # get all zones
        zones = self.cloudflare_api.get_zones_mapped_by_name()
        id_zone = zones[dns_name]

        dns_records = self.cloudflare_api.list_dns_records(id_zone=id_zone)

        # Lookup for the record
        for dns_record_data in dns_records:
            if dns_record_data['name'] == dns_name and dns_record_data['type'] == dns_type:
                dns_record_data_found = dns_record_data
                break
        else:
            raise DnsRecordNotFoundError(f"DNS record not found: {dns_name} '{dns_type}'.")

        data = dns_record_data_found.copy()
        data['content'] = new_ip

        response = self.cloudflare_api.update_dns_record(
            id_dns=dns_record_data_found['id'],
            id_zone=id_zone,
            data=data)
        assert response.status_code == 200, "Failed to update dns record. {0}".format(response.content)
        return True, response
