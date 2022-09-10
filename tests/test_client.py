import os
from random import randint
import pytest

from emerchantpay.client import Emerchantpay
from emerchantpay.types import PaymentRequest, BillingAddress

def test_client():
    u = os.environ.get("MERCHANT_USERNAME")
    p = os.environ.get("MERCHANT_PASSWORD")
    client = Emerchantpay(username=u, password=p)

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


