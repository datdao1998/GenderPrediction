class ErrorArgsOrHeader(RuntimeError):
    def __init__(self, message):
        super(ErrorArgsOrHeader, self).__init__(message)
        self.code = 1000


class ErrorAuthentication(RuntimeError):
    def __init__(self, message):
        super(ErrorAuthentication, self).__init__(message)
        self.code = 1001
        self.status = "AUTHENTICATION NOT VALID"


class NotFoundData(RuntimeError):
    def __init__(self, message):
        super(NotFoundData, self).__init__(message)
        self.code = 1002
        self.status = "NOT FOUND"


class InvalidNameCharacter(RuntimeError):
    def __init__(self, message):
        super(InvalidNameCharacter, self).__init__(message)
        self.code = 1003


class InvalidLanguageCharacter(RuntimeError):
    def __init__(self, message):
        super(InvalidLanguageCharacter, self).__init__(message)
        self.code = 1004


class LanguageValueNotFound(RuntimeError):
    def __init__(self, message):
        super(LanguageValueNotFound, self).__init__(message)
        self.code = 1005


class LanguageAndNameNotMatch(RuntimeError):
    def __init__(self, message):
        super(LanguageAndNameNotMatch, self).__init__(message)
        self.code = 1006


class NotFoundNameArray(RuntimeError):
    def __init__(self, message):
        super(NotFoundNameArray, self).__init__(message)
        self.code = 1007
#
#
# class InvalidCharacterArray(RuntimeError):
#     def __init__(self, message):
#         super(InvalidCharacterArray, self).__init__(message)
#         self.code = 1010
#
#
# class NotMatchNameArray(RuntimeError):
#     def __init__(self, message):
#         super(NotMatchNameArray, self).__init__(message)
#         self.code = 1011
