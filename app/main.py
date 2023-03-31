# required libraries
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import uvicorn

from query import Query

app = FastAPI()

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
