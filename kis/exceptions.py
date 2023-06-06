from typing import Any, Dict


class KISModuleError(Exception):
    msg = "Korea-invest module 에러"

    def __init__(self, msg: str = ""):
        self.msg = msg or self.msg
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


class KISWrongAccount(KISModuleError):
    msg = "계좌정보가 잘못되었습니다."


class KISBadArguments(KISModuleError):
    msg = "argument 입력이 잘못되었습니다."


class KISDevModeError(KISModuleError):
    msg = "모의투자 모드에서는 사용할 수 없는 기능입니다."


class KISRecursionError(KISModuleError):
    msg = "재귀 호출이 발생했습니다."


class KISSessionNotFound(KISModuleError):
    msg = "session을 찾을 수 없습니다."


class KISNoData(KISModuleError):
    msg = "데이터가 없습니다."


def handle_error(data: Dict[str, Any]):
    status_code, msg_code, msg = data["rt_cd"], data["msg_cd"], data["msg1"]
    err_msg = f"[{data.get('tr_id', 'NO tr_id return')}] '{msg_code}': {msg}"

    if status_code == "0":
        if msg_code == "70070000":
            # 조회 결과가 없는 경우
            raise KISNoData(err_msg)

    else:
        if msg_code == "OPSQ2000":
            # 잘못된 계좌번호일 경우
            raise KISWrongAccount(err_msg)

        if msg_code == "40650000":
            # 모의투자 주문시 지정가 외에 선택할 경우
            raise KISDevModeError(err_msg)

        raise KISBadArguments(err_msg)
