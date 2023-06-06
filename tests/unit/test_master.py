from kis.core.master import MasterBook


class TestMaster:

    def test_download_kosdaq(self):
        df = MasterBook.get("kosdaq")
        assert df is not None

    def test_download_kosdaq_only_symbol(self):
        df = MasterBook.get("kosdaq", with_detail=True)
        assert df is not None

    def test_download_kospi(self):
        df = MasterBook.get("kospi")
        assert df is not None

    def test_download_kospi_only_symbol(self):
        df = MasterBook.get("kospi", with_detail=True)
        print(df)
        assert df is not None

    def test_download_amex(self):
        df = MasterBook.get("ams")
        assert df is not None

    def test_download_nasdaq(self):
        df = MasterBook.get("NAS")
        assert df is not None

    def test_download_nasdaq_only_symbol(self):
        df = MasterBook.get("NAS", with_detail=True)
        assert df is not None
