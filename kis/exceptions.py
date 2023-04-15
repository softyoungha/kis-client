class KISModuleError(Exception):
    msg = "Korea-invest module 에러"

    def __init__(self, msg: str = ""):
        super().__init__(msg or self.msg)


class KISServerHTTPError(KISModuleError):
    msg = "한국투자증권 서버로부터 에러 응답을 받았습니다."

    def __init__(self, url: str):
        super().__init__(f"{self.msg}: url={url}")


class KISServerInternalError(KISModuleError):
    msg = "한국투자증권 서버로부터 응답을 받을 수 없습니다"

    def __init__(self, url: str):
        super().__init__(f"{self.msg}: url={url}")


class KISAccountNotFound(KISModuleError):
    msg = "account를 찾을 수 없습니다."


class KISSecretNotFound(KISModuleError):
    msg = "secret을 찾을 수 없습니다."


class KISBadArguments(KISModuleError):
    msg = "argument 입력이 잘못되었습니다."


class KISSessionNotFound(KISModuleError):
    msg = "session을 찾을 수 없습니다."
