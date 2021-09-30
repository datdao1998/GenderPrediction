import traceback

__all__ = ["WSException"]

default_codes = {200, 500}
codes = dict()


class WSException(Exception):
    def __init__(self, message, code=None, **kwargs):
        super(WSException, self).__init__(message)

        assert (
            code not in default_codes and code not in codes.values()
        ), "code: {} is used".format(code)

        self.name = self.__class__.__name__
        if self.name not in codes and code is not None:
            codes[self.name] = code

        self.code = codes.get(self.name, 500)

        self.__dict__.update(kwargs)

    def __repr__(self):
        return "<{code}> {message}".format(code=self.code, message=super().__repr__())

    @property
    def traceback(self):
        return "".join(traceback.format_tb(self.__traceback__))
