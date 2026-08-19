import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

from knowledge.knowledge_base import (
    load_products,
    load_policies,
    find_product,
    get_return_policy,
    search_knowledge
)

from openai import OpenAI

MODEL_NAME = "gpt-5-mini"

client = OpenAI()

# Load knowledge through the knowledge layer
products = load_products()
policies = load_policies()

# Conversation memory
conversation = {
    "product": None,
    "intent": None
}


# Support case state
support_case = {
    "product": None,
    "intent": None,
    "status": "New",
    "needs_human": False,
    "next_action": "Understand the customer's request"
}



def detect_intent(question):
    question_lower = question.lower()

    price_words = [
        "price",
        "cost",
        "how much",
        "pay",
        "worth"
    ]

    warranty_words = [
        "warranty",
        "covered",
        "coverage",
        "protection"
    ]

    return_words = [
        "return",
        "refund",
        "send it back",
        "take it back",
        "money back"
    ]

    shipping_words = [
        "shipping",
        "delivery",
        "deliver",
        "where is my order",
        "where's my order",
        "track my order",
        "order status",
        "late",
        "delayed",
        "never arrived",
        "didn't arrive",
        "did not arrive",
        "missing",
        "lost",
        "not delivered",
        "wrong delivery",
        "tracking says delivered",
        "marked delivered"
    ]

    payment_words = [
        "payment",
        "paid",
        "charge",
        "charged",
        "transaction"
    ]

    security_words = [
        "privacy",
        "private",
        "security",
        "account security",
        "personal information",
        "accessed my account",
        "access my account",
        "without permission",
        "unauthorized access",
        "hacked",
        "someone got into my account"
    ]

    if any(word in question_lower for word in security_words):
        return "Security"

    if any(word in question_lower for word in return_words):
        return "Return"

    if any(word in question_lower for word in shipping_words):
        return "Shipping"

    if any(word in question_lower for word in payment_words):
        return "Payment"

    if any(word in question_lower for word in warranty_words):
        return "Warranty"

    if any(word in question_lower for word in price_words):
        return "Price"

    return None


def set_case_status(status):
    support_case["status"] = status
    logger.info("Support case status: %s", status)


def update_support_case(product, intent):
    if product:
        conversation["product"] = product
        support_case["product"] = product["name"]

    if intent:
        # Reset case-specific escalation state when a new intent is detected
        if intent != conversation["intent"]:
            support_case["status"] = "New"
            support_case["needs_human"] = False
            support_case["next_action"] = "Understand the customer's request"

        conversation["intent"] = intent
        support_case["intent"] = intent

def generate_ai_response(question, knowledge_results):
    knowledge_text = json.dumps(
        knowledge_results,
        indent=2
    )

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            instructions=(
                "You are Nova, a professional customer-support assistant. "
                "Answer the customer's question using only the provided "
                "company knowledge. "
                "Do not invent product details, prices, policies, "
                "warranties, requirements, timelines, fees, or procedures. "
                "Only state requirements or next steps that are explicitly "
                "supported by the provided company knowledge. "
                "If the knowledge does not contain enough information, "
                "say that the information is not available and do not guess. "
                "Keep responses concise and professional."
            ),
            input=(
                f"Customer question:\n{question}\n\n"
                f"Company knowledge:\n{knowledge_text}"
            )
        )

        return response.output_text

    except Exception:
        return (
            "I'm temporarily unable to generate a response. "
            "Please try again shortly or contact human support if the issue is urgent."
        )


def answer_question(question):
    question_lower = question.lower()

    product = find_product(products, question)

    if product:
        logger.info("Product identified: %s", product["name"])

    # Use remembered product if no product is mentioned
    if not product and conversation["product"]:
        product = conversation["product"]

    # Include the remembered product when searching the knowledge base
    knowledge_question = question

    if product and product["name"].lower() not in question_lower:
        knowledge_question = f"{product['name']} {question}"

    knowledge_results = search_knowledge(
        products,
        policies,
        knowledge_question
    )
    intent = detect_intent(question)

    if intent:
        logger.info("Intent detected: %s", intent)

            # Only remember the previous intent when the customer
    # is continuing the same conversation.
    if not intent and conversation["intent"] and product:
        intent = conversation["intent"]

    update_support_case(product, intent)

        # Price
    if intent == "Price":

        for result in knowledge_results:
            if result["type"] == "price":
                set_case_status("Resolved")
                logger.info("Support case resolved: price request")
                support_case["next_action"] = "Provide product price"

                return generate_ai_response(question, [result])

        if product:
            set_case_status("Needs information")
            support_case["next_action"] = "Add product price to knowledge base"

            return (
                f"I don't currently have the price for the "
                f"{product['name']} in my knowledge base."
            )

        set_case_status("Needs clarification")
        support_case["next_action"] = "Identify the product"

        return "Which product would you like the price for?"
           # Warranty
    if intent == "Warranty":

        for result in knowledge_results:
            if result["type"] == "warranty":
                set_case_status("Resolved")
                logger.info("Support case resolved: warranty request")
                support_case["next_action"] = "Provide warranty information"

                return generate_ai_response(question, [result])
        if product:
            set_case_status("Needs information")
            support_case["next_action"] = "Add warranty information to knowledge base"

            return (
                f"I don't currently have the warranty information for "
                f"the {product['name']} in my knowledge base."
            )

        set_case_status("Needs clarification")
        support_case["next_action"] = "Identify the product"

        return "Which product would you like to ask about?"
        support_case["status"] = "Needs clarification"
        support_case["next_action"] = "Identify the product"

        return "Which product would you like to ask about?"

               # Returns and refunds
    if intent == "Return":

        return_problem_words = [
            "return was rejected",
            "return rejected",
            "refund was rejected",
            "refund rejected",
            "refund never arrived",
            "never got my refund",
            "didn't get my refund",
            "did not get my refund",
            "haven't received my refund",
            "have not received my refund",
            "return dispute",
            "dispute my return",
            "dispute the return",
            "wrongly rejected",
            "return denied",
            "refund denied"
        ]

        if any(word in question_lower for word in return_problem_words):
            set_case_status("Human review recommended")
            support_case["needs_human"] = True
            support_case["next_action"] = "Verify return or refund status and escalate disputed case if necessary"

            return (
                "I'm sorry you're having trouble with your return or refund. "
                "I'll need to verify the return or refund information. "
                "Because this may be a disputed or unusual case, "
                "it may need to be escalated to human support."
            )

        return_policy = None

        for result in knowledge_results:
            if (
                result["type"] == "policy"
                and result["name"] == "Returns and Refunds"
            ):
                return_policy = result["information"]
                break

        if product and return_policy:
            set_case_status("Needs verification")
            support_case["next_action"] = "Verify order information"

            return generate_ai_response(question, [
                {
                    "type": "policy",
                    "name": "Returns and Refunds",
                    "information": return_policy
                }
            ])
        if product:
            set_case_status("Needs information")
            support_case["next_action"] = "Retrieve return policy"

            return (
                f"I can help you with returning the {product['name']}, "
                "but I need to retrieve the applicable return policy first."
            )

        support_case["status"] = "Needs clarification"
        support_case["next_action"] = "Identify the product"

        return (
            "I can help with your return or refund request. "
            "Which product would you like to return?"
        )

           # Shipping
    if intent == "Shipping":

        delivery_problem_words = [
            "late",
            "delayed",
            "never arrived",
            "didn't arrive",
            "did not arrive",
            "missing",
            "lost",
            "not delivered",
            "wrong delivery",
            "tracking says delivered",
            "marked delivered"
        ]

        if any(word in question_lower for word in delivery_problem_words):
            set_case_status("Human review recommended")
            support_case["needs_human"] = True
            support_case["next_action"] = "Verify order and escalate delivery issue if necessary"

            return (
                "I'm sorry you're having trouble with your delivery. "
                "I'll need to verify your order and delivery information. "
                "If the order is delayed, missing, or marked delivered "
                "but hasn't been received, the issue may need to be "
                "escalated to human support."
            )

        shipping_policy = None

        for result in knowledge_results:
            if (
                result["type"] == "policy"
                and result["name"] == "Shipping and Delivery"
            ):
                shipping_policy = result["information"]
                break

        if shipping_policy:
            set_case_status("Needs verification")
            support_case["next_action"] = "Check order and delivery information"

            return generate_ai_response(question, [
                {
                    "type": "policy",
                    "name": "Shipping and Delivery",
                    "information": shipping_policy
                }
            ])

        set_case_status("Needs information")
        support_case["next_action"] = "Retrieve shipping policy"

        return (
            "I can help with your shipping or delivery question, "
            "but I need to retrieve the applicable shipping policy first."
        )

               # Payment
    if intent == "Payment":

        payment_problem_words = [
            "charged twice",
            "charged two times",
            "double charged",
            "duplicate charge",
            "duplicate payment",
            "don't recognize this charge",
            "do not recognize this charge",
            "unrecognized charge",
            "unauthorized charge",
            "charged but didn't receive",
            "charged but did not receive",
            "charged but never received",
            "charged the wrong amount",
            "wrong amount",
            "incorrect charge"
        ]

        if any(word in question_lower for word in payment_problem_words):
            set_case_status("Human review recommended")
            support_case["needs_human"] = True
            support_case["next_action"] = "Verify transaction and escalate payment dispute if necessary"

            return (
                "I'm sorry you're experiencing a payment issue. "
                "I'll need to verify the transaction details. "
                "Because this may involve a disputed or unauthorized "
                "charge, the issue may need to be escalated to human support."
            )

        payment_policy = None

        for result in knowledge_results:
            if (
                result["type"] == "policy"
                and result["name"] == "Payments"
            ):
                payment_policy = result["information"]
                break

        if payment_policy:
            set_case_status("Needs verification")
            support_case["next_action"] = "Identify the order or transaction"

            return generate_ai_response(question, [
                {
                    "type": "policy",
                    "name": "Payments",
                    "information": payment_policy
                }
            ])

        set_case_status("Needs information")
        support_case["next_action"] = "Retrieve payment policy"

        return (
            "I can help with your payment-related question, "
            "but I need to retrieve the applicable payment policy first."
        )

        # Security
    if intent == "Security":

        security_policy = None

        for result in knowledge_results:
            if result["type"] == "policy" and result["name"] == "Privacy and Security":
                security_policy = result["information"]
                break

        support_case["status"] = "Human review recommended"
        support_case["needs_human"] = True
        support_case["next_action"] = "Escalate suspected security issue if necessary"

        if security_policy:
            return (
                "Protecting your information is important to Nova. "
                "Suspected security incidents are escalated to human support."
            )

        return (
            "I can help with your security concern, but this issue "
            "should be reviewed by human support."
        )


        # Unknown request
    support_case["intent"] = None
    support_case["status"] = "Needs human support"
    support_case["needs_human"] = True
    logger.warning("Support case escalated to human support")
    support_case["next_action"] = "Escalate to human support"

    return (
        "I don't have enough information to answer that accurately. "
        "I can escalate the question to human support."
    )


def show_case():
    print()
    print("----- Support Case -----")
    print(f"Product: {support_case['product'] or 'Not identified'}")
    print(f"Intent: {support_case['intent'] or 'Not identified'}")
    print(f"Status: {support_case['status']}")
    print(f"Needs human: {support_case['needs_human']}")
    print(f"Next action: {support_case['next_action']}")
    print("------------------------")
    print()


def main():
    print("Nova AI Customer Support")
    print("------------------------")
    print("Ask a customer-support question.")
    print("Type 'case' to view the current support case.")
    print("Type 'exit' to stop.")
    print()

    while True:
        question = input("Customer: ")

        if question.lower() == "exit":
            print("Nova: Thank you for contacting Nova Support.")
            break

        if question.lower() == "case":
            show_case()
            continue

        answer = answer_question(question)

        print(f"Nova: {answer}")
        print()


if __name__ == "__main__":
    main()