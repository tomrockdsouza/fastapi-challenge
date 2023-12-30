from pydantic import BaseModel, Field


class AlembicVersionResponse(BaseModel):
    alembic_version: str = Field(
        max_length=256,
        min_length=0,
        description="The migration version of Alembic",
        example="48be8a14b663"
    )


class OrdersResponse(BaseModel):
    id: str = Field(
        max_length=256,
        min_length=0,
        description="ID of the order created via API",
        example="861fae7b-7bb4-4fb2-bf07-5243f3724a56"
    )
