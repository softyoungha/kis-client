import os

import pandas as pd

from . import MasterBook


class KospiMaster(MasterBook):

    def __init__(self):
        super().__init__(exchange="kospi")

    def get_dataframe(self) -> pd.DataFrame:
        file_name, part1_file, part2_file = (
            os.path.join(self.cache_dir, "kospi_code.mst"),
            os.path.join(self.cache_dir, "kospi_code_part1.tmp"),
            os.path.join(self.cache_dir, "kospi_code_part2.tmp"),
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
                    rf1 = row[0:len(row) - 228]
                    rf1_1 = rf1[0:9].rstrip()
                    rf1_2 = rf1[9:21].rstrip()
                    rf1_3 = rf1[21:].strip()
                    buffer1.write(rf1_1 + "," + rf1_2 + "," + rf1_3 + "\n")
                    rf2 = row[-228:]
                    buffer2.write(rf2)

        part1_columns = ["단축코드", "표준코드", "한글명"]
        df_part1 = pd.read_csv(
            part1_file,
            header=None,
            names=part1_columns,
            encoding="cp949"
        )

        field_specs = [
            2, 1, 4, 4, 4,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 9, 5, 5, 1,
            1, 1, 2, 1, 1,
            1, 2, 2, 2, 3,
            1, 3, 12, 12, 8,
            15, 21, 2, 7, 1,
            1, 1, 1, 1, 9,
            9, 9, 5, 9, 8,
            9, 3, 1, 1, 1
        ]

        part2_columns = [
            "그룹코드", "시가총액규모", "지수업종대분류", "지수업종중분류", "지수업종소분류",
            "제조업", "저유동성", "지배구조지수종목", "KOSPI200섹터업종", "KOSPI100",
            "KOSPI50", "KRX", "ETP", "ELW발행", "KRX100",
            "KRX자동차", "KRX반도체", "KRX바이오", "KRX은행", "SPAC",
            "KRX에너지화학", "KRX철강", "단기과열", "KRX미디어통신", "KRX건설",
            "Non1", "KRX증권", "KRX선박", "KRX섹터_보험", "KRX섹터_운송",
            "SRI", "기준가", "매매수량단위", "시간외수량단위", "거래정지",
            "정리매매", "관리종목", "시장경고", "경고예고", "불성실공시",
            "우회상장", "락구분", "액면변경", "증자구분", "증거금비율",
            "신용가능", "신용기간", "전일거래량", "액면가", "상장일자",
            "상장주수", "자본금", "결산월", "공모가", "우선주",
            "공매도과열", "이상급등", "KRX300", "KOSPI", "매출액",
            "영업이익", "경상이익", "당기순이익", "ROE", "기준년월",
            "시가총액", "그룹사코드", "회사신용한도초과", "담보대출가능", "대주가능"
        ]

        df_part2 = pd.read_fwf(part2_file, widths=field_specs, names=part2_columns)

        # join
        df = pd.merge(df_part1, df_part2, how="outer", left_index=True, right_index=True)

        # clean temporary file and dataframe
        del df_part1, df_part2

        return df
