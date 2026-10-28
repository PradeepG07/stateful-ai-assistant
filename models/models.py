from pydantic import BaseModel, Field
from typing import Optional, Literal


class GetCustomerByNameArgs(BaseModel):

    name: str = Field(
        min_length=1,
        description="Full customer name"
    )

class GetOrdersArgs(BaseModel):

    customer_id: int = Field(gt=0)

    status: Optional[
        Literal[
            "Delivered",
            "Shipped",
            "Processing"
        ]
    ] = None


class CalculateTotalSpendingArgs(BaseModel):

    customer_id: int = Field(gt=0)

class GetCustomerSupportTicketsArgs(BaseModel):

    customer_id: int = Field(
        gt=0,
        description="Unique ID of the customer"
    )

class GetCustomerArgs(BaseModel):
    customer_id: int = Field(gt=0)
