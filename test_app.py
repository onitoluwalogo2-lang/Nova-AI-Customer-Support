from app import detect_intent


def test_price_intent():
    assert detect_intent("What is the price of the Nova Play Station?") == "Price"


def test_warranty_intent():
    assert detect_intent("How long is the Nova Play Station covered?") == "Warranty"


def test_return_intent():
    assert detect_intent("I want to return my Play Station.") == "Return"


def test_shipping_intent():
    assert detect_intent("Where is my order?") == "Shipping"


def test_late_delivery_intent():
    assert detect_intent("My order is late.") == "Shipping"


def test_payment_intent():
    assert detect_intent("I was charged for my order.") == "Payment"


def test_payment_dispute_intent():
    assert detect_intent("I was charged twice.") == "Payment"


def test_security_intent():
    assert detect_intent(
        "I think someone accessed my account without permission."
    ) == "Security"


def test_unknown_intent():
    assert detect_intent("Can you tell me tomorrow's weather?") is None


print("All intent tests passed!")