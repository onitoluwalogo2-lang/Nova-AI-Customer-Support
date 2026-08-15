from knowledge.knowledge_base import (
    load_products,
    load_policies,
    search_knowledge
)


products = load_products()
policies = load_policies()


def test_playstation_price():
    results = search_knowledge(
        products,
        policies,
        "What is the price of the Nova Play Station?"
    )

    assert any(
        result["type"] == "product"
        and result["name"] == "Nova Play Station"
        and result["information"]["price"] == 350
        for result in results
    )


def test_playstation_warranty():
    results = search_knowledge(
        products,
        policies,
        "What is the warranty on the Nova Play Station?"
    )

    assert any(
        result["type"] == "warranty"
        and "2-year warranty" in result["information"]
        for result in results
    )


def test_return_policy():
    results = search_knowledge(
        products,
        policies,
        "I want to return my Nova Play Station"
    )

    assert any(
        result["type"] == "policy"
        and result["name"] == "Returns and Refunds"
        for result in results
    )


def test_shipping_policy():
    results = search_knowledge(
        products,
        policies,
        "Where is my order?"
    )

    assert any(
        result["type"] == "policy"
        and result["name"] == "Shipping and Delivery"
        for result in results
    )


def test_privacy_policy():
    results = search_knowledge(
        products,
        policies,
        "How do you protect my personal information?"
    )

    assert any(
        result["type"] == "policy"
        and result["name"] == "Privacy and Security"
        for result in results
    )


print("All knowledge tests passed!")