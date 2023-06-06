from enum import Enum
from kis.exceptions import KISBadArguments


class Exchange(str, Enum):
    """거래소 코드"""
    KOSPI = "KOSPI"  # 코스피
    KOSDAQ = "KOSDAQ"  # 코스닥

    NYS = "NYS"  # 뉴욕
    NAS = "NAS"  # 나스닥
    AMS = "AMS"  # 아멕스

    TSE = "TSE"  # 도쿄

    HKS = "HKS"  # 홍콩
    SHS = "SHS"  # 상해
    SHI = "SHI"  # 상해지수
    SZS = "SZS"  # 심천
    SZI = "SZI"  # 심천지수
    HSX = "HSX"  # 호치민
    HNX = "HNX"  # 하노이
    BAY = "BAY"  # 뉴욕(주간)
    BAQ = "BAQ"  # 나스닥(주간)
    BAA = "BAA"  # 아멕스(주간)

    @classmethod
    def from_value(cls, value: str) -> "Exchange":
        if isinstance(value, str):
            try:
                exchange = Exchange(value.upper())
            except ValueError as err:
                raise KISBadArguments("No such ExchangeCode") from err
        elif isinstance(value, cls):
            exchange = value
        else:
            raise KISBadArguments("Wrong type of value")
        if exchange not in (
                cls.KOSPI,
                cls.KOSDAQ,
                cls.NAS,
                cls.NYS,
                cls.AMS
        ):
            raise KISBadArguments("Only NAS, NYS, AMS are supported")
        return exchange

    @property
    def master_file_name(self):
        """마스터 zip 파일명"""
        if self.name == "KOSPI":
            return "kospi_code.mst.zip"
        if self.name == "KOSDAQ":
            return "kosdaq_code.mst.zip"
        return f"{self.name.lower()}mst.cod.zip"

    @property
    def code(self):
        """
        거래소 코드
        주문시 Query Parameter로 들어가는 코드는 4글자 string이므로 변환 필요
        """

        if self.name == "NAS":  # 나스닥
            return "NASD"
        if self.name == "NYS":  # 뉴욕
            return "NYSE"
        if self.name == "AMS":  # 아멕스
            return "AMEX"
        if self.name == "HKS":  # 홍콩
            return "SEHK"
        if self.name == "SHS":  # 중국상해
            return "SHAA"
        if self.name == "SZS":  # 중국심천
            return "SZAA"
        if self.name == "TSE":  # 일본
            return "TKSE"
        if self.name == "HNX":  # 베트남 하노이
            return "HASE"
        if self.name == "HSX":  # 베트남 호치민
            return "VNSE"

    def currency(self):
        if self.name in ("NAS", "NYS", "AMS"):
            return "USD"
        if self.name in ("HKS", "SHS", "SZS"):
            return "HKD"
        if self.name in ("TSE", "SHI", "SZI"):
            return "JPY"
        if self.name in ("HSX", "HNX"):
            return "VND"
        return "KRW"


class Sign(str, Enum):
    CEILING = "상한"  # 상한
    INCREASING = "상승"  # 상승
    UNCHANGED = "보합"  # 보합
    DECREASING = "하락"  # 하락
    FLOOR = "하한"  # 하한

    @classmethod
    def from_value(cls, value: str):
        """ 한국투자증권 코드를 Sign Enum으로 변환 """
        if value == "1":
            return cls.CEILING
        elif value == "2":
            return cls.INCREASING
        elif value == "3":
            return cls.UNCHANGED
        elif value == "4":
            return cls.FLOOR
        return cls.DECREASING


class OverseasOrderPrice(str, Enum):
    """ 주문가격구분 """
    LIMIT = "LIMIT"  # 지정가
    MARKET = "MARKET"  # 시장가
    LOO = "LOO"  # 장개시지정가
    LOC = "LOC"  # 장마감지정가
    MOO = "MOO"  # 장개시시장가
    MOC = "MOC"  # 장마감시장가

    @property
    def code(self):
        if self.name == "MOO":
            return "31"
        if self.name == "LOO":
            return "32"
        if self.name == "MOC":
            return "33"
        if self.name == "LOC":
            return "34"
        return "00"

