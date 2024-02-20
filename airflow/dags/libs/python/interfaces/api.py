from abc import ABC, abstractmethod


class InterfaceAPI(ABC):

    @abstractmethod
    def get_request(self):
        pass
