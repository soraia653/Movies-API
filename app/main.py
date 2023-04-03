# required libraries
import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from app.query import Query
from app.settings import HOST, PORT

app = FastAPI()

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema, debug=True)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
