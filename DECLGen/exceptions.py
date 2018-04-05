

class DECLException(Exception):
    exitcode = 1


class LibraryNotInitializedError(DECLException):
    exitcode = 2


class LibraryExistsError(DECLException):
    exitcode = 3


class LibraryTemplateException(DECLException):
    exitcode = 10


class LibraryCategoryException(DECLException):
    exitcode = 20


class LibraryCategoryNotFoundException(LibraryCategoryException):
    exitcode = 22


class LibraryCategoryExistsException(LibraryCategoryException):
    exitcode = 23


class LibraryCategoryFullException(LibraryCategoryException):
    exitcode = 24


class LibraryElementException(DECLException):
    exitcode = 30


class LibraryElementNotFoundException(LibraryCategoryException):
    exitcode = 32


class LibraryElementExistsException(LibraryCategoryException):
    exitcode = 33

