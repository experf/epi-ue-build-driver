import asyncio

def get_or_create_eventloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError as ex:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return asyncio.get_running_loop()
