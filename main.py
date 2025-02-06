from fastapi import FastAPI
from app.config.database import lifespan
from app.routes.auth_routes import auth_router
from app.routes.product_routes import product_api_router
from app.routes.cart_routes import cart_api_router
from app.routes.order_routes import order_api_router
from app.routes.complaint_routes import compliant_api_router

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(product_api_router)
app.include_router(cart_api_router)
app.include_router(order_api_router)
app.include_router(compliant_api_router)

