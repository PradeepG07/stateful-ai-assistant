import json
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder
DATA_DIR = BASE_DIR / "data"


# Load customers
with open(DATA_DIR / "customers.json", "r", encoding="utf-8") as f:
    customers = json.load(f)


# Load orders
with open(DATA_DIR / "orders.json", "r", encoding="utf-8") as f:
    orders = json.load(f)

def get_customer(customer_id):

    for customer in customers:

        if customer["customer_id"] == customer_id:
            return customer

    return {"error": "Customer not found"}


def get_orders(customer_id, status=None):

    result = [
        order
        for order in orders
        if order["customer_id"] == customer_id
    ]

    if status:
        result = [
            order
            for order in result
            if order["status"].lower() == status.lower()
        ]

    return result


def calculate_total_spending(customer_id):

    customer_orders = get_orders(customer_id)

    total = sum(
        order["amount"]
        for order in customer_orders
    )

    return {
        "customer_id": customer_id,
        "total_spending": total
    }

def get_customer_by_name(name):

    for customer in customers:

        if customer["name"].lower() == name.lower():
            return customer

    raise ValueError(
        f"Customer '{name}' not found"
    )

def get_customer_support_tickets(customer_id):

    tickets = [
        {
            "ticket_id": 9001,
            "customer_id": 101,
            "issue": "Laptop delivery delay",
            "status": "Closed"
        },
        {
            "ticket_id": 9002,
            "customer_id": 101,
            "issue": "Mouse not working",
            "status": "Open"
        }
    ]

    return [
        ticket
        for ticket in tickets
        if ticket["customer_id"] == customer_id
    ]
