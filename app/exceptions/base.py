class DomainError(Exception):

    code = "domain_error"

    def __init__(
        self,
        message: str = "Operation failed"
    ):
        self.message = message
        super().__init__(message)


class RedirectException(Exception):

    def __init__(
        self,
        url: str,
        status_code: int = 303
    ):
        self.url = url
        self.status_code = status_code
