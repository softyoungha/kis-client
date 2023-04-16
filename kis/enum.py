from typing import Optional
from enum import Enum
from kis.exceptions import KISBadArguments


class Exchange(str, Enum):
    """거래소 코드"""
    KOSPI = "KOSPI"  # 코스피
    KOSDAQ = "KOSDAQ"  # 코스닥
    HKS = "HKS"  # 홍콩
    NYS = "NYS"  # 뉴욕
    NAS = "NAS"  # 나스닥
    AMS = "AMS"  # 아멕스
    TSE = "TSE"  # 도쿄
    SHS = "SHS"  # 상해
    SZS = "SZS"  # 심천
    SHI = "SHI"  # 상해지수
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
                return Exchange(value.upper())
            except ValueError as err:
                raise KISBadArguments("No such ExchangeCode") from err
        elif isinstance(value, cls):
            return value
        raise KISBadArguments("Wrong type of value")

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
