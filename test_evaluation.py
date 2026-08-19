import app

from app import answer_question, conversation, support_case


def fake_ai_response(question, knowledge_results):
    return "Test AI response"


app.generate_ai_response = fake_ai_response


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

def test_product_memory():
    reset_state()

    answer_question("What is the price of the Nova Play Station?")

    assert conversation["product"]["name"] == "Nova Play Station"

    answer_question("What about the warranty?")

    assert conversation["product"]["name"] == "Nova Play Station"
    assert support_case["product"] == "Nova Play Station"
    assert support_case["intent"] == "Warranty"


def test_product_context_switch():
    reset_state()

    answer_question("What is the price of the Nova Play Station?")

    assert conversation["product"]["name"] == "Nova Play Station"

    answer_question("What is the warranty on the Nova Camera?")

    assert conversation["product"]["name"] == "Nova Camera"
    assert support_case["product"] == "Nova Camera"
    assert support_case["intent"] == "Warranty"


def test_api_failure_fallback():
    original_client = app.client
    original_generate_ai_response = app.generate_ai_response

    class FakeResponses:
        def create(self, **kwargs):
            raise Exception("Simulated OpenAI failure")

    class FakeClient:
        responses = FakeResponses()

    app.client = FakeClient()
    app.generate_ai_response = original_generate_ai_response

    try:
        result = app.generate_ai_response(
            "What is the price of the Nova Play Station?",
            []
        )

        expected = (
            "I'm temporarily unable to generate a response. "
            "Please try again shortly or contact human support if the issue is urgent."
        )

        assert result == expected

    finally:
        app.client = original_client
        app.generate_ai_response = original_generate_ai_response
        

if __name__ == "__main__":
    tests = [
        ("Price handling", test_price_request),
        ("Return handling", test_return_request),
        ("Shipping handling", test_shipping_request),
        ("Delivery escalation", test_late_delivery_escalation),
        ("Payment escalation", test_payment_escalation),
        ("Security escalation", test_security_escalation),
        ("Unknown request handling", test_unknown_request_escalation),
        ("Escalation reset", test_new_intent_resets_human_escalation),
        ("Product memory", test_product_memory),
        ("Product context switching", test_product_context_switch),
        ("API failure fallback", test_api_failure_fallback),
    ]

    print()
    print("Nova AI Evaluation Report")
    print("-------------------------")

    passed = 0

    for name, test in tests:
        test()
        print(f"{name:<30} PASS")
        passed += 1

    print()
    print(f"{passed}/{len(tests)} evaluation scenarios passed")