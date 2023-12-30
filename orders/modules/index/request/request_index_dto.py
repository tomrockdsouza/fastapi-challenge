from pydantic import BaseModel, Field
from decimal import Decimal

class CreateOrderRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=256,
        pattern=r"^[a-z0-9-]+$",
        description="The migration version of Alembic",
        example="7c11e1ce2741"
    )
    product_code: str = Field(
        min_length=1,
        max_length=256,
        pattern=r"^[a-z0-9-]+$",
        example="classic-box"
    )


class ParseProductDetails(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=256,
        pattern=r"^[a-z0-9-]+$"
    )
    name: str = Field(
        min_length=1,
        max_length=256,
        pattern=r"^[A-Za-z0-9- ]+$"
    )
    price:Decimal = Field(ge=0,le=999_999_999_999, decimal_places=2)


class ParseUserDetails(BaseModel):
    id: str = Field(
        min_length=1,
        max_length=256,
        pattern=r"^[a-z0-9-]+$"
    )
    firstName: str = Field(
        max_length=128,
        pattern=r"^[A-Za-z0-9- ]+$"
    )
    lastName: str = Field(
        max_length=128,
        pattern=r"^[A-Za-z0-9- ]+$"
    )
