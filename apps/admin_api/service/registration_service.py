from core.handler.exceptions import ResponseHandler
from core.config import G_CIP_API, API_KEY
import re
import socket
import requests
import string, random
from werkzeug.utils import secure_filename
from flask import request
from core.config import azure_options
from apps.middleware import blob_service
from .interface import AdminServiceInterface


class AdminRegistrationService(AdminServiceInterface):

    def get_registration(self, company_id: int) -> dict:
        args = (company_id)
        rs = self.admin_page_dao.one_product_set(args)
        return rs

    def id_generator(self, size=32, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def file_upload_to_azure(self, file):
        pre_filename = secure_filename(file.filename)
        file_extension = pre_filename.rsplit('.', 1)[1]
        GEO_LOCATION = request.headers.get('X-Client-Geo-Location')

        filename = 'product_{}/'.format(GEO_LOCATION) + self.id_generator() + '.' + file_extension
        blob_service.create_blob_from_stream(azure_options['container'], filename, file)

        return 'https://tngstorage01.blob.core.windows.net/tngimage01/' + filename

    def add_registration(self, file_name, **kwargs) -> dict:
        add_args = list(map(lambda arg: arg, kwargs.values()))
        add_args.insert(2, file_name)
        rs_add = self.admin_page_dao.registration_set(add_args)

        cid = self.admin_page_dao.get_id(kwargs['url'])
        whois_info = self.add_whois_data(kwargs['url'])['detail']
        try:
            for whois_data in whois_info:
                address_args = (
                    cid, whois_data['ip_address'], whois_data['org_country_code'], whois_data['local_address'],
                    whois_data['latitude'], whois_data['longitude'], whois_data['asn_name'])
                rs_whois = self.admin_page_dao.product_address_add(address_args)
        except:
            return ResponseHandler(500).response()
        return rs_add

    def add_whois_data(self, url: str) -> dict:
        p = r'^https?:\/\/(?P<domain>[^\/]*)'
        comp = re.compile(p)
        searchs = comp.search(url)
        host = searchs.group('domain')

        result_set = {'detail': []}
        res_fail = {'latitude': '', 'longitude': '',
                    'local_address': '', 'org_country_code': '', 'ip_address': None,
                    'asn_name': '', 'result': ''}
        host_url = host
        host_ip = socket.gethostbyname_ex(host_url)[-1]
        headers = {'x-api-key': API_KEY}
        for ip in host_ip:
            whois_data = requests.get(G_CIP_API['API_URL'] + ip, headers=headers)
            if whois_data.json()['status'] == 200:
                info = whois_data.json()['detail'][0]
                res = {
                    'ip_address': str(ip),
                    'org_country_code': str(info['org_country_code']),
                    'local_address': str(info['local_address']),
                    'latitude': str(info['latitude']),
                    'longitude': str(info['longitude']),
                    'asn_name': str(info['asn_name'])
                }
                result_set['detail'].append(res)
            else:
                res_fail['ip_address'] = str(ip)
                result_set['detail'].append(res_fail)
        return result_set

    def update_registration(self, file_name, company_id: int, **kwargs) -> int:
        if self.get_registration(company_id) == ():
            return 404
        else:
            update_args = [company_id]
            [update_args.append(value) for value in kwargs.values()]
            update_args.insert(3, file_name)
            res = self.admin_page_dao.update_registration_set(update_args)

            self.admin_page_dao.product_address_reset(company_id)
            whois_info = self.add_whois_data(kwargs['url'])['detail']
            try:
                for whois_data in whois_info:
                    address_args = (
                        company_id, whois_data['ip_address'], whois_data['org_country_code'],
                        whois_data['local_address'],
                        whois_data['latitude'], whois_data['longitude'], whois_data['asn_name'])
                    rs_whois = self.admin_page_dao.product_address_add(address_args)
            except:
                return 500
            return 200

    def delete_registration(self, company_id: int) -> int:
        if self.get_registration(company_id) == ():
            return 404
        else:
            self.admin_page_dao.delete_registration_set(company_id)
        return 200
