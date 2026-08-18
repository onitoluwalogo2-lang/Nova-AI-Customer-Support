from app import answer_question, conversation, support_case


def reset_state():
    conversation["product"] = None
    conversation["intent"] = None

    support_case["product"] = None
    support_case["intent"] = None
    support_case["status"] = "New"
    support_case["needs_human"] = False
    support_case["next_action"] = "Understand the customer's request"


def test_price_request():
    reset_state()

    answer_question("What is the price of the Nova Play Station?")

    assert support_case["intent"] == "Price"
    assert support_case["product"] == "Nova Play Station"
    assert support_case["status"] == "Resolved"
    assert support_case["needs_human"] is False


def test_return_request():
    reset_state()

    answer_question("I want to return my Nova Play Station.")

    assert support_case["intent"] == "Return"
    assert support_case["product"] == "Nova Play Station"
    assert support_case["status"] == "Needs verification"
    assert support_case["needs_human"] is False


def test_shipping_request():
    reset_state()

    answer_question("Where is my order?")

    assert support_case["intent"] == "Shipping"
    assert support_case["status"] == "Needs verification"
    assert support_case["needs_human"] is False


def test_late_delivery_escalation():
    reset_state()

    answer_question("My order is late.")

    assert support_case["intent"] == "Shipping"
    assert support_case["status"] == "Human review recommended"
    assert support_case["needs_human"] is True


def test_payment_escalation():
    reset_state()

    answer_question("I was charged twice.")

    assert support_case["intent"] == "Payment"
    assert support_case["status"] == "Human review recommended"
    assert support_case["needs_human"] is True


def test_security_escalation():
    reset_state()

    answer_question("I think someone accessed my account.")

    assert support_case["intent"] == "Security"
    assert support_case["status"] == "Human review recommended"
    assert support_case["needs_human"] is True


def test_unknown_request_escalation():
    reset_state()

    answer_question("What is the weather tomorrow?")

    assert support_case["intent"] is None
    assert support_case["status"] == "Needs human support"
    assert support_case["needs_human"] is True


def test_new_intent_resets_human_escalation():
    reset_state()

    answer_question("My order is late.")

    assert support_case["needs_human"] is True

    answer_question("What is the price of the Nova Play Station?")

    assert support_case["intent"] == "Price"
    assert support_case["status"] == "Resolved"
    assert support_case["needs_human"] is False


if __name__ == "__main__":
    test_price_request()
    test_return_request()
    test_shipping_request()
    test_late_delivery_escalation()
    test_payment_escalation()
    test_security_escalation()
    test_unknown_request_escalation()
    test_new_intent_resets_human_escalation()

    print("All evaluation tests passed!")