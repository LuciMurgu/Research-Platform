"""Application layer — CommandBus, query handlers, application services.

This layer dispatches validated commands to orchestrators and serves
read queries. It may call orchestrators but must not contain scientific
computation or direct storage logic.
"""
