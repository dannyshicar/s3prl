from enum import Enum
from operator import setitem

import torch

from .container import Container


class LogDataType(Enum):
    SCALAR = 0
    TEXT = 1
    AUDIO = 2
    IMAGE = 3
    HIDDEN_STATE = 4


class LogData:
    def __init__(self, name, data, data_type) -> None:
        assert isinstance(name, str)
        assert isinstance(data_type, LogDataType)
        if isinstance(data, torch.Tensor):
            data = data.detach().cpu()

        self.name = name
        self.data = data
        self.data_type = data_type


class Logs(Container):
    def __setitem__(self, k, v) -> None:
        assert isinstance(v, LogData)
        return super().__setitem__(k, v)

    def add_data(self, name, data, data_type):
        setitem(self, name, LogData(name, data, data_type))

    def add_scalar(self, name, data):
        self.add_data(name, data, LogDataType.SCALAR)

    def add_text(self, name, data):
        self.add_data(name, data, LogDataType.TEXT)

    def add_audio(self, name, data):
        self.add_data(name, data, LogDataType.AUDIO)

    def add_image(self, name, data):
        self.add_data(name, data, LogDataType.IMAGE)

    def add_hidden_state(self, name, data):
        self.add_data(name, data, LogDataType.HIDDEN_STATE)
