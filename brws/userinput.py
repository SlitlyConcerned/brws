import os


class UserInput:
    def __init__(self, string):
        self.string = string

    @property
    def _split_string(self):
        return self.string.split(" ")

    @property
    def _list_to_bytes(self):
        return list(map(os.fsencode, self._split_string))

    @property
    def as_byte_string(self):
        return b" ".join(self._list_to_bytes)
