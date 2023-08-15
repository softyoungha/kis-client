from kis.core.master import MasterBook


class TestMaster:
    def test_download_kosdaq(self):
        """
        코스닥 전체 종목 리스트를 pandas dataframe으로 가져옵니다.
        한국투자증권에서 제공하는 기타 정보들도 함께 가져옵니다.
        """
        df = MasterBook.get("kosdaq", with_detail=True)
        assert df is not None

    def test_download_kosdaq_only_symbol(self):
        """
        코스닥 전체 종목 리스트를 pandas dataframe으로 가져옵니다.
        종목코드, 거래소 정보, 종목명만 가져옵니다.
        """
        df = MasterBook.get("kosdaq")
        assert df is not None

    def test_download_kospi(self):
        """
        코스피 전체 종목 리스트를 pandas dataframe으로 가져옵니다.
        한국투자증권에서 제공하는 기타 정보들도 함께 가져옵니다.
        """
        df = MasterBook.get("kospi", with_detail=True)
        assert df is not None

    def test_download_kospi_only_symbol(self):
        """
        코스피 전체 종목 리스트를 pandas dataframe으로 가져옵니다.
        종목코드, 거래소 정보, 종목명만 가져옵니다.
        """
        df = MasterBook.get("kospi")
        assert df is not None

    def test_download_amex(self):
        """AMEX 전체 종목 리스트를 pandas dataframe으로 가져옵니다"""
        df = MasterBook.get("ams")
        assert df is not None

    def test_download_nasdaq(self):
        """NASDAQ 전체 종목 리스트를 pandas dataframe으로 가져옵니다"""
        df = MasterBook.get("NAS", with_detail=True)
        assert df is not None

    def test_download_nasdaq_only_symbol(self):
        """NASDAQ 전체 종목 리스트를 pandas dataframe으로 가져옵니다"""
        df = MasterBook.get("NAS")
        assert df is not None
