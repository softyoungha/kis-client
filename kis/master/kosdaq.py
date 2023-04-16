import os

import pandas as pd

from . import MasterBook


class KosdaqMaster(MasterBook):

    def __init__(self):
        super().__init__(exchange="kosdaq")

    def get_dataframe(self) -> pd.DataFrame:
        file_name, part1_file, part2_file = (
            os.path.join(self.cache_dir, "kosdaq_code.mst"),
            os.path.join(self.cache_dir, "kosdaq_code_part1.tmp"),
            os.path.join(self.cache_dir, "kosdaq_code_part2.tmp"),
        )
        if (
                not os.path.exists(file_name)
                or not os.path.exists(part1_file)
                or not os.path.exists(part2_file)
        ):
            self.download_file()

        with open(part1_file, mode="w") as buffer1, open(part2_file, mode="w") as buffer2:
            with open(file_name, mode="r", encoding="cp949") as f:
                for row in f:
                    rf1 = row[0:len(row) - 222]
                    rf1_1 = rf1[0:9].rstrip()
                    rf1_2 = rf1[9:21].rstrip()
                    rf1_3 = rf1[21:].strip()
                    buffer1.write(rf1_1 + "," + rf1_2 + "," + rf1_3 + "\n")
                    rf2 = row[-222:]
                    buffer2.write(rf2)

        part1_columns = ["단축코드", "표준코드", "한글명"]
        df_part1 = pd.read_csv(
            part1_file,
            header=None,
            names=part1_columns,
            encoding="cp949"
        )

        field_specs = [
            2, 1,
            4, 4, 4, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 9,
            5, 5, 1, 1, 1,
            2, 1, 1, 1, 2,
            2, 2, 3, 1, 3,
            12, 12, 8, 15, 21,
            2, 7, 1, 1, 1,
            1, 9, 9, 9, 5,
            9, 8, 9, 3, 1,
            1, 1
        ]

        part2_columns = [
            "증권그룹구분코드", "시가총액 규모 구분 코드 유가",
            "지수업종 대분류 코드", "지수 업종 중분류 코드", "지수업종 소분류 코드", "벤처기업 여부 (Y/N)",
            "저유동성종목 여부", "KRX 종목 여부", "ETP 상품구분코드", "KRX100 종목 여부 (Y/N)",
            "KRX 자동차 여부", "KRX 반도체 여부", "KRX 바이오 여부", "KRX 은행 여부", "기업인수목적회사여부",
            "KRX 에너지 화학 여부", "KRX 철강 여부", "단기과열종목구분코드", "KRX 미디어 통신 여부",
            "KRX 건설 여부", "(코스닥)투자주의환기종목여부", "KRX 증권 구분", "KRX 선박 구분",
            "KRX섹터지수 보험여부", "KRX섹터지수 운송여부", "KOSDAQ150지수여부 (Y,N)", "주식 기준가",
            "정규 시장 매매 수량 단위", "시간외 시장 매매 수량 단위", "거래정지 여부", "정리매매 여부",
            "관리 종목 여부", "시장 경고 구분 코드", "시장 경고위험 예고 여부", "불성실 공시 여부",
            "우회 상장 여부", "락구분 코드", "액면가 변경 구분 코드", "증자 구분 코드", "증거금 비율",
            "신용주문 가능 여부", "신용기간", "전일 거래량", "주식 액면가", "주식 상장 일자", "상장 주수(천)",
            "자본금", "결산 월", "공모 가격", "우선주 구분 코드", "공매도과열종목여부", "이상급등종목여부",
            "KRX300 종목 여부 (Y/N)", "매출액", "영업이익", "경상이익", "단기순이익", "ROE(자기자본이익률)",
            "기준년월", "전일기준 시가총액 (억)", "그룹사 코드", "회사신용한도초과여부", "담보대출가능여부", "대주가능여부"
        ]

        df_part2 = pd.read_fwf(part2_file, widths=field_specs, names=part2_columns)

        # join
        df = pd.merge(df_part1, df_part2, how="outer", left_index=True, right_index=True)

        # clean temporary file and dataframe
        del df_part1, df_part2

        return df
