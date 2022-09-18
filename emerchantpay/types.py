from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BillingAddress:
    country:str
    city:str

    first_name:str = ""
    last_name:str = ""
    address1:str = ""
    zip_code:str = ""
    state:str = ""

@dataclass
class PaymentRequest:
    transaction_id: str
    description: str
    notification_url: str
    return_success_url: str
    return_failure_url: str
    return_cancel_url: str
    return_pending_url: str
    amount: str
    currency: str
    customer_email: str
    billing_address:BillingAddress
    transaction_types: List[str]

    consumer_id: str = ""


@dataclass
class RefundRequest:
    transaction_id: str
    reference_id: str
    amount: int
    currency:Optional[str] = None

    transaction_type:str = "refund"
