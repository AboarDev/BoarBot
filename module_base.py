import abc
import asyncio


class module_base(abc.ABC):

    @abc.abstractmethod
    def __init__(self, client):
        pass

    def on_ready(self):
        pass

    def on_message(self, msg):
        pass

    def on_close(self):
        pass
