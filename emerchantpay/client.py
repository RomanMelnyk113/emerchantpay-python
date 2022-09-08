import base64
import hashlib
import hmac
import json
import uuid
from datetime import date, datetime
from http import HTTPStatus
from typing import Optional, Callable, List
from urllib.parse import urlencode
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

    def _prepare_headers(self, with_access_token=True):
        return {
            'Content-Type': 'text/xml',
        }


    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _send_request( self, endpoint: str, data: dict, tx_types:str, headers: dict):
        print(data)
        post_params = dicttoxml(data, attr_type=False, custom_root="wpf_payment")
        post_params = post_params.decode('utf-8').replace("PLACEHOLDER", tx_types).encode('utf-8')
        print(post_params)
        auth = HTTPBasicAuth(self.username,self.password)
        r = requests.post(self._generate_url(endpoint), headers=headers, data=post_params, auth=auth)
        print(r.text)
        if r.status_code != HTTPStatus.OK:
            raise PaymentException(
                'Emerchantpay error: {}. Error code: {}'.format(r.text, r.status_code))

        return json.loads(r.text)
    
    def build_tx_types(self, transaction_types: List[str]) -> str:
        tx_types = []
        for tx in transaction_types:
            tx_types.append(f'<transaction_type name="{tx}"/>')

        return ''.join(tx_types)

    def checkout(self, data: PaymentRequest, transactions_types: List[str]) -> dict:
        endpoint = '/wpf'

        headers = self._prepare_headers()
        tx_types = self.build_tx_types(transactions_types)
        return self._send_request(endpoint, asdict(data), tx_types, headers)
