from fastapi import FastAPI, applications, Depends

from routes.products import productsRouter
from routes.product_category import categotyTypeRouter
from fastapi.staticfiles import StaticFiles
import strawberry
from graphqlFile.queries import Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from config.db import SessionLocal
from strawberry.fastapi import GraphQLRouter


app = FastAPI()

# Serve files from the uploads/category_image directory
app.mount("/uploads", StaticFiles(directory="/home/sekoph/projects/online_bidding_fastapi-v2/uploads"), name="uploads")


origins = [
    'http://localhost:8001',
    'http://localhost:8003',
    'http://localhost:3000',
    'http://localhost:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
schema = strawberry.Schema(query=Query)


async def get_context(db:Session = Depends(get_db)):
    return {"db":db}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)


app.include_router(graphql_app, prefix="/graphql")
app.include_router(productsRouter)
app.include_router(categotyTypeRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)