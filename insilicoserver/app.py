"""Main loop event."""

from pathlib import Path
from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers
import pkg_resources as pkg

from insilicodatabase import DatabaseConfig, connect_to_db

PATH_LIB = Path(pkg.resource_filename('insilicoserver', ''))

db_info = DatabaseConfig("properties")

context = {
    "mongodb": connect_to_db(db_info)
}


def run() -> None:
    """Entry point of the application."""
    web.run_app(
        register_graphql_handlers(
            app=web.Application(),
            executor_context=context,
            engine_sdl=(PATH_LIB / "sdl").absolute().as_posix(),
            engine_modules=[
                "insilicoserver.query_resolvers",
                "insilicoserver.mutation_resolvers",
                "insilicoserver.subscription_resolvers",
                "insilicoserver.directives.rate_limiting",
                "insilicoserver.directives.auth",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True
        )
    )


# import asyncio

# from tartiflette import Resolver, create_engine


# @Resolver("Query.hello")
# async def resolver_hello(parent, args, ctx, info):
#     return "hello " + args["name"]


# async def main():
#     engine = await create_engine(
#         """
#         type Query {
#             hello(name: String): String
#         }
#         """
#     )

#     result = await engine.execute(
#         query='query { hello(name: "Chuck") }'
#     )

#     print(result)
#     # {'data': {'hello': 'hello Chuck'}}

# if __name__ == "__main__":
#     asyncio.run(main())
