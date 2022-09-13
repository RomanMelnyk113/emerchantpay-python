import os
from random import randint
import pytest

from emerchantpay.client import Emerchantpay
from emerchantpay.types import PaymentRequest, BillingAddress, RefundRequest

def test_wpf():
    u = os.environ.get("MERCHANT_USERNAME")
    p = os.environ.get("MERCHANT_PASSWORD")
    t = os.environ.get("MERCHANT_TERMINAL")
    client = Emerchantpay(username=u, password=p, terminal_code=t)

    req = PaymentRequest(
        transaction_id=str(randint(1, 10000)),
        description="test",
        notification_url= "https://notification.test",
        return_success_url= "https://success.test",
        return_failure_url= "https://failure.test",
        return_cancel_url= "https://cancel.test",
        return_pending_url= "https://pending.test",
        amount= str(randint(1, 10000)),
        currency= "USD",
        customer_email= "test@gmail.com",
        billing_address=BillingAddress(country="USA", city="Sundasky"),
        transaction_types=["authorize3d"]
    )

    res = client.checkout(req)

    assert res is not None
    assert "wpf_payment" in res
    assert res["wpf_payment"]["status"] == "new"
    assert res["wpf_payment"]["amount"] == req.amount
    assert res["wpf_payment"]["currency"] == req.currency
    assert "redirect_url" in res["wpf_payment"]


def test_refund():
    u = os.environ.get("MERCHANT_USERNAME")
    p = os.environ.get("MERCHANT_PASSWORD")
    t = os.environ.get("MERCHANT_TERMINAL")
    client = Emerchantpay(username=u, password=p, terminal_code=t)

    req = RefundRequest(
        transaction_id=str(randint(1, 10000)),
        reference_id="",
        amount=randint(1, 10000),
        currency= "USD",
    )

    res = client.refund(req)

    assert res is not None
    assert res == 1
