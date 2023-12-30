from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from modules.database import get_db
from sqlalchemy import text
from modules.index.response.response_index_dto import AlembicVersionResponse, OrdersResponse
from modules.index.request.request_index_dto import CreateOrderRequest
from modules.models import Orders
from modules.index.helpers.helpers import fetch_data, send_data_to_rabbit_mq
import asyncio
from uuid import uuid4
from datetime import datetime
import json
import os
from fastapi.responses import FileResponse

product_service = os.getenv('product-service')
user_service = os.getenv('user-service')

if not (product_service or user_service):
    raise Exception('product or user service variables not set.')

PRODUCT_SERVICE_TIMEOUT = 65 # SLA of product api can be 60 seconds so gave a buffer of 65s
USER_SERVICE_TIMEOUT = 1 # SLA of user api can be 300ms seconds so gave a buffer of 1s

app = FastAPI(
    openapi_url="/api/openapi.json",  # Change the OpenAPI schema URL
    docs_url='/docs',  # Change the URL for documentation
    redoc_url=None,  # Disable ReDoc
    title="[HelloFresh DACH] - Tomrock D'souza",  # Set the documentation title to "Application"
    version="1.0",
)

@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("index.html")

@app.post("/orders",response_model=OrdersResponse)
async def submit_order(
        background_tasks: BackgroundTasks,
        order_request: CreateOrderRequest,
        db: Session = Depends(get_db)
):
    product_task = asyncio.create_task(
        fetch_data(
            service='product-service',
            url=f'http://{product_service}/products/{order_request.product_code}',
            timeout=PRODUCT_SERVICE_TIMEOUT
        )
    )
    user_task = asyncio.create_task(
        fetch_data(
            service='user-service',
            url=f'http://{user_service}/users/{order_request.user_id}',
            timeout=USER_SERVICE_TIMEOUT
        )
    )
    product, user = await asyncio.gather(product_task, user_task)
    order_id = str(uuid4())
    order = Orders(
        id=order_id,
        user_id=user.id,
        product_code=product.code,
        customer_fullname=f'{user.firstName}{f" {user.lastName}" if user.lastName else ""}',
        product_name=product.name,
        total_amount=product.price,
        created_at=datetime.utcnow(),
    )
    message = {
        "producer": "order-service",
        "sent_at": datetime.utcnow().isoformat(),
        "type": "INSERT",
        "payload": {
            "order": {
                "order_id": order.id,
                "customer_fullname": order.customer_fullname,
                "product_name": order.product_name,
                "total_amount": str(order.total_amount),
                "created_at": order.created_at.isoformat()
            }
        }
    }
    try:
        db.add(order)
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail='Something went wrong when inserting data in the database.'
        )
    background_tasks.add_task(send_data_to_rabbit_mq,'orders','created_order',json.dumps(message))
    return {"id": order_id}


@app.get("/check_alembic_version", response_model=AlembicVersionResponse)
async def read_alembic_version(db: Session = Depends(get_db)):
    query = text("SELECT version_num FROM alembic_version")
    alembic_version = await db.execute(query)
    alembic_version = alembic_version.scalar_one_or_none()
    return {"alembic_version": alembic_version}
