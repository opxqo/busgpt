from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from app.config import settings


@dataclass(frozen=True)
class PaymentResult:
    provider: str
    payment_no: str
    status: str
    paid_at: datetime


class PaymentProvider:
    name = "base"

    async def confirm_payment(self, order_id: int, amount: Decimal) -> PaymentResult:
        raise NotImplementedError


class MockPaymentProvider(PaymentProvider):
    name = "mock"

    async def confirm_payment(self, order_id: int, amount: Decimal) -> PaymentResult:
        if not settings.MOCK_PAYMENT_ENABLED:
            raise RuntimeError("Mock payment provider is disabled")
        return PaymentResult(
            provider=self.name,
            payment_no=f"mock_{order_id}_{uuid4().hex}",
            status="paid",
            paid_at=datetime.utcnow(),
        )


def get_payment_provider(provider_name: Optional[str] = None) -> PaymentProvider:
    provider = provider_name or settings.PAYMENT_PROVIDER
    if provider == "mock":
        return MockPaymentProvider()
    raise ValueError(f"Unsupported payment provider: {provider}")
