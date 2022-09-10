import json
import xmltodict
from datetime import date, datetime
from http import HTTPStatus
from typing import List
from dataclasses import asdict
from dicttoxml import dicttoxml

import requests
from requests.auth import HTTPBasicAuth

from . import PaymentException
from emerchantpay.types import PaymentRequest

DEFAULT_BASE_API_URL = 'https://staging.wpf.emerchantpay.net'


# https://emerchantpay.github.io/gateway-api-docs/?shell#create
class Emerchantpay:
    # password
    password: str

    # username
    username: str

    # api endpoint
    api_url: str

    def __init__(self, password, username, api_url=None):
        self.password = password
        self.username = username

        self.api_url = api_url or DEFAULT_BASE_API_URL

    def _prepare_headers(self):
        return {
            'Content-Type': 'text/xml',
        }


    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _send_request( self, endpoint: str, data: dict, headers: dict):
        req = {
            "wpf_payment": data
        }
        print(req)
        post_params = xmltodict.unparse(req, expand_iter="coord")
        print(post_params)
        auth = HTTPBasicAuth(self.username,self.password)
        r = requests.post(self._generate_url(endpoint), headers=headers, data=post_params, auth=auth)
        print(r.text)
        if r.status_code != HTTPStatus.OK:
            raise PaymentException(
                'Emerchantpay error: {}. Error code: {}'.format(r.text, r.status_code))

        # return json.loads(r.text)
        return xmltodict.parse(r.text)
    
    def build_tx_types(self, transaction_types: List[str]) -> list:
        tx_types = []
        for tx in transaction_types:
            tx_types.append({
                "transaction_type": {
                    "@name": tx
                }
            })

        return tx_types

    def checkout(self, data: PaymentRequest) -> dict:
        endpoint = '/wpf'

        headers = self._prepare_headers()
        data.transaction_types = self.build_tx_types(data.transaction_types)
        return self._send_request(endpoint, asdict(data), headers)
