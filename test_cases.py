from app import (
    update_support_case,
    support_case,
    conversation
)


# Reset the shared state before testing
support_case["product"] = None
support_case["intent"] = None

conversation["product"] = None
conversation["intent"] = None


# Test product memory
test_product = {
    "name": "Nova Play Station"
}

update_support_case(
    test_product,
    "Price"
)


assert support_case["product"] == "Nova Play Station"
assert support_case["intent"] == "Price"

assert conversation["product"]["name"] == "Nova Play Station"
assert conversation["intent"] == "Price"


print("Support case memory tests passed!")