"""API layer — FastAPI routes.

Routes accept commands and serve queries. They call application services
(CommandBus, query handlers) only. No scientific computation logic here.
"""
