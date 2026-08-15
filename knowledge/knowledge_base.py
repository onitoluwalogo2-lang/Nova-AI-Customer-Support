import json


def load_products():
    with open("data/products.json", "r") as file:
        return json.load(file)


def load_policies():
    with open("data/policies.json", "r") as file:
        return json.load(file)


def find_product(products, question):
    question = question.lower()

    for product in products["products"]:
        product_name = product["name"].lower()

        if product_name in question:
            return product

        if "play station" in question and "play station" in product_name:
            return product

        if "smart glasses" in question and "smart glasses" in product_name:
            return product

        if "camera" in question and "camera" in product_name:
            return product

        if "wifi router" in question or "wi-fi router" in question:
            if "wifi router" in product_name:
                return product

    return None

def get_return_policy(policies):
    return policies["policies"]["returns_and_refunds"]


def search_knowledge(products, policies, question):
    question_lower = question.lower()

    results = []

    # Product information
    product = find_product(products, question)

    if product:
        results.append({
            "type": "product",
            "name": product["name"],
            "information": product
        })

    # Warranty questions
    warranty_words = [
        "warranty",
        "covered",
        "coverage",
        "protection"
    ]

    if any(word in question_lower for word in warranty_words):
        if product and product.get("warranty_years"):
            results.append({
                "type": "warranty",
                "information": (
                    f"{product['name']} has a "
                    f"{product['warranty_years']}-year warranty."
                )
            })

    # Price questions
    price_words = [
        "price",
        "cost",
        "how much",
        "pay",
        "worth"
    ]

    if any(word in question_lower for word in price_words):
        if product and "price" in product:
            results.append({
                "type": "price",
                "information": (
                    f"{product['name']} costs "
                    f"${product['price']}."
                )
            })

            # Return/refund policy
    return_words = [
        "return",
        "return it",
        "send it back",
        "send this back",
        "send it",
        "refund",
        "get a refund"
    ]

    if any(word in question_lower for word in return_words):
        if "returns_and_refunds" in policies["policies"]:
            results.append({
                "type": "policy",
                "name": "Returns and Refunds",
                "information": policies["policies"]["returns_and_refunds"]
            })

    # Shipping policy
    shipping_words = [
        "shipping",
        "delivery",
        "where is my order",
        "where's my order",
        "order status",
        "track my order"
    ]

    if any(word in question_lower for word in shipping_words):
        if "shipping_and_delivery" in policies["policies"]:
            results.append({
                "type": "policy",
                "name": "Shipping and Delivery",
                "information": policies["policies"]["shipping_and_delivery"]
            })

    # Payment policy
    payment_words = [
        "payment",
        "charged",
        "charge",
        "billing",
        "paid",
        "pay"
    ]

    if any(word in question_lower for word in payment_words):
        if "payments" in policies["policies"]:
            results.append({
                "type": "policy",
                "name": "Payments",
                "information": policies["policies"]["payments"]
            })
    # Security policy
    security_words = [
        "hacked",
        "hack",
        "unauthorized",
        "unauthorised",
        "someone accessed my account",
        "accessed my account",
        "account compromised",
        "security",
        "stolen account",
        "someone got into my account"
    ]

    if any(word in question_lower for word in security_words):
        if "privacy_and_security" in policies["policies"]:
            results.append({
                "type": "policy",
                "name": "Privacy and Security",
                "information": policies["policies"]["privacy_and_security"]
            })
    return results