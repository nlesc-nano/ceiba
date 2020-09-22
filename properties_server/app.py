"""Main loop event."""

from pathlib import Path
from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers
import pkg_resources as pkg

PATH_LIB = Path(pkg.resource_filename('properties_server', ''))


def run() -> None:
    """Entry point of the application."""
    web.run_app(
        register_graphql_handlers(
            app=web.Application(),
            engine_sdl=(PATH_LIB / "sdl").absolute().as_posix(),
            engine_modules=[
                "properties_server.query_resolvers",
                "properties_server.mutation_resolvers",
                "properties_server.subscription_resolvers",
                "properties_server.directives.rate_limiting",
                "properties_server.directives.auth",
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
