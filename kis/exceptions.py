class KISModuleError(Exception):
    msg = "Korea-invest module 에러"

    def __init__(self, msg: str = ""):
        super().__init__(msg or self.msg)


class KISConfigFileNotFound(KISModuleError):
    msg = (
        "config yaml 파일을 찾을 수 없습니다."
        "$KIS_HOME $KIS_CONFIG 환경변수를 설정할 수 있습니다.\n"
        "- windows: set KIS_CONFIG=/path/config.yaml\n"
        "- linux: export KIS_CONFIG=/path/config.yaml"
    )


class KISConfigNotFound(KISModuleError):
    msg = "해당 Config를 찾을 수 없습니다."


class KISServerHTTPError(KISModuleError):
    msg = "한국투자증권 서버로부터 에러 응답을 받았습니다."

    def __init__(self, url: str):
        super().__init__(f"{self.msg}: url={url}")


class KISServerInternalError(KISModuleError):
    msg = "한국투자증권 서버로부터 응답을 받을 수 없습니다"

    def __init__(self, url: str):
        super().__init__(f"{self.msg}: url={url}")


class KISBadArguments(KISModuleError):
    msg = "argument 입력이 잘못되었습니다."
