from datetime import datetime, date
from typing import List, Union, Optional, TYPE_CHECKING
import pandas as pd
import bt
from kis.core import MasterBook

if TYPE_CHECKING:
    from kis.core import DomesticClient, OverseasClient


def get_data_from_kis(
        client: Union["DomesticClient", "OverseasClient"],
        symbols: Union[str, List[str]],
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
):
    if isinstance(symbols, str):
        symbols = [symbols]

    if client.NAME == "DOMESTIC":
        master = MasterBook.get("KRX")
    elif client.NAME == "OVERSEAS":
        master = MasterBook.get("USA")
    else:
        raise ValueError(f"Invalid client name: {client.NAME}")

    dfs = []
    for symbol in symbols:
        symbol_name = master[master["symbol"] == symbol]["korean"].values[0]

        _, histories = client.quote.fetch_histories(
            symbol,
            start_date,
            end_date,
            standard="D"
        )
        histories = histories[::-1]
        df = pd.DataFrame(
            [row.close for row in histories],
            index=pd.to_datetime([row.business_date for row in histories]),
            columns=[symbol_name],
        )
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    return df


def do_backtest(
        client: Union["DomesticClient", "OverseasClient"],
        symbols: Union[str, List[str]],
        start_date: str,
        end_date: str,
        algos: List[bt.algos.Algo] = None,

):
    if isinstance(symbols, str):
        symbols = [symbols]

    if client.NAME == "DOMESTIC":
        master = pd.concat([
            MasterBook.get("KOSPI", with_detail=True),
            MasterBook.get("KOSDAQ", with_detail=True)
        ], axis=0)
    elif client.NAME == "OVERSEAS":
        master = MasterBook.get("OVERSEAS", with_detail=True)
    else:
        raise ValueError(f"Invalid client name: {client.NAME}")

    dfs = []
    for symbol in symbols:
        symbol_name = master[master["symbol"] == symbol]["korean"].values[0]

        _, histories = client.quote.fetch_histories(
            symbol,
            start_date,
            end_date,
            standard="D"
        )
        histories = histories[::-1]
        df = pd.DataFrame(
            [row.close for row in histories],
            index=pd.to_datetime([row.business_date for row in histories]),
            columns=[symbol_name],
        )
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    print(df.head())

    if algos is None:
        algos = [
            bt.algos.SelectAll(),
            bt.algos.WeighEqually(),
            bt.algos.RunMonthly(),
            bt.algos.Rebalance()
        ]

    strategy = bt.Strategy("Test", algos)
    backtest = bt.Backtest(strategy, df, initial_capital=10000000)
    return bt.run(backtest)


def do_backtester(
        client: Union["DomesticClient", "OverseasClient"],
        symbols: Union[str, List[str]],
        start_date: str,
        end_date: str,
        algos: List[bt.algos.Algo] = None,

):
    if isinstance(symbols, str):
        symbols = [symbols]

    if client.NAME == "DOMESTIC":
        master = pd.concat([
            MasterBook.get("KOSPI", with_detail=True),
            MasterBook.get("KOSDAQ", with_detail=True)
        ], axis=0)
    elif client.NAME == "OVERSEAS":
        master = MasterBook.get("OVERSEAS", with_detail=True)
    else:
        raise ValueError(f"Invalid client name: {client.NAME}")

    dfs = []
    for symbol in symbols:
        symbol_name = master[master["symbol"] == symbol]["korean"].values[0]

        _, histories = client.quote.fetch_histories(
            symbol,
            start_date,
            end_date,
            standard="D"
        )
        histories = histories[::-1]
        df = pd.DataFrame(
            [row.close for row in histories],
            index=pd.to_datetime([row.business_date for row in histories]),
            columns=[symbol_name],
        )
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    print(df.head())

    if algos is None:
        algos = [
            bt.algos.SelectAll(),
            bt.algos.WeighEqually(),
            bt.algos.RunMonthly(),
            bt.algos.Rebalance()
        ]

    strategy = bt.Strategy("Test", algos)
    backtest = bt.Backtest(strategy, df, initial_capital=10000000)
    return bt.run(backtest)
