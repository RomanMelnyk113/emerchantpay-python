import logging
from dataclasses import asdict
from http import HTTPStatus
from typing import Dict, List

import requests
import xmltodict
from requests.auth import HTTPBasicAuth

from emerchantpay.types import RefundRequest

from . import PaymentException

BASE_WPF_URL = "https://wpf.emerchantpay.net"
TRANSACTION_API_URL = "https://gate.emerchantpay.net/process"

STAGING_BASE_WPF_URL = "https://staging.wpf.emerchantpay.net"
STAGING_TRANSACTION_API_URL = "https://staging.gate.emerchantpay.net/process"

logger = logging.getLogger(__name__)


# https://emerchantpay.github.io/gateway-api-docs/?shell#create
class Emerchantpay:
    # password
    password: str

    # username
    username: str

    # terminal_code
    terminal_codes: dict

    # api endpoint
    api_url: str

    def __init__(self, password, username, terminal_codes, sandbox=True):
        self.password = password
        self.username = username
        self.terminal_codes = terminal_codes

        self.wpf_url = STAGING_BASE_WPF_URL if sandbox else BASE_WPF_URL
        self.api_url = STAGING_TRANSACTION_API_URL if sandbox else TRANSACTION_API_URL

    def _prepare_headers(self):
        return {
            "Content-Type": "text/xml",
        }

    def _generate_url(self, endpoint, wpf=True):
        return self.api_url + endpoint

    def _send_request(self, endpoint: str, data: dict, headers: dict) -> dict:
        post_params = xmltodict.unparse(data, expand_iter="coord")
        # print("Emerchantpay request: %s", post_params)
        auth = HTTPBasicAuth(self.username, self.password)
        r = requests.post(endpoint, headers=headers, data=post_params, auth=auth)
        # print("Emerchantpay response: %s", r.text)
        if r.status_code != HTTPStatus.OK:
            raise PaymentException(
                "Emerchantpay error: {}. Error code: {}".format(r.text, r.status_code)
            )

        return xmltodict.parse(r.text)

    def build_tx_types(self, transaction_types: List[Dict[str, str]]) -> list:
        tx_types = []
        for tx in transaction_types:
            data = {"transaction_type": tx}
            tx_types.append(data)

        return tx_types

    def checkout(self, data: dict) -> dict:
        endpoint = f"{self.wpf_url}/wpf"

        headers = self._prepare_headers()
        data["transaction_types"] = self.build_tx_types(data.get("transaction_types"))
        req = {"wpf_payment": data}
        return self._send_request(endpoint, req, headers)

    def refund(self, data: RefundRequest) -> dict:
        headers = self._prepare_headers()
        trx = asdict(data)
        for k in list(trx.keys()):
            if trx[k] is None:
                del trx[k]

        req = {"payment_transaction": trx}
        terminal_code = self.terminal_codes[data.currency]
        endpoint = f"{self.api_url}/{terminal_code}/"
        return self._send_request(endpoint, req, headers)

    def reconcile(self, unique_id: str) -> dict:
        headers = self._prepare_headers()
        req = {"wpf_reconcile": {"unique_id": unique_id}}
        endpoint = f"{self.wpf_url}/wpf/reconcile"
        return self._send_request(endpoint, req, headers)
