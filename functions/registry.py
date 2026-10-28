tools = [
    {
            "type": "function",
            "name": "get_customer",
            "description": (
                "Get customer information using customer ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "customer id of the customer"
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            },
            "strict": True
        },  

    {
        "type": "function",
        "name": "get_customer_by_name",
        "description": (
             "Find a customer using their full name and return "
            "their customer details including customer ID."
            
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the customer"
                }
            },
            "required": ["name"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_orders",
        "description": (
            "Get orders for a customer. "
            "Optionally filter orders by status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Unique ID of the customer"
                },
                "status": {
                    "type": ["string", "null"],
                    "description": (
                        "Optional order status such as "
                        "Delivered, Shipped or Processing"
                    )
                }
            },
            "required": ["customer_id", "status"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "calculate_total_spending",
        "description": "Calculate the total spending of a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Unique ID of the customer"
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_customer_support_tickets",
        "description": "Get support tickets for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Unique ID of the customer"
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False
        },
        "strict": True
    }

]