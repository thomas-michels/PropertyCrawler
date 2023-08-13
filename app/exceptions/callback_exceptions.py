"""
Module for callback expeptions
"""


class CallbackNotMethod(Exception):
    """
    Raised when attribute function is not a function
    """

    def __init__(self, *args: object) -> None:
        message = "Callback needs function"
        super().__init__(*args, message)


class FunctionAnnotation(Exception):
    """
    Raised when annotation of function is not a bool
    """

    def __init__(self, *args: object) -> None:
        message = "Annotation of function is not a bool"
        super().__init__(*args, message)


class QueueNotFound(Exception):
    """
    Raised when queue not found
    """

    def __init__(self, *args: object) -> None:
        message = "Queue not found"
        super().__init__(*args, message)


class CallbackAlreadyCreated(Exception):
    """
    Raise when callback already created
    """

    def __init__(self, *args: object) -> None:
        message = "Callback already created"
        super().__init__(*args, message)
