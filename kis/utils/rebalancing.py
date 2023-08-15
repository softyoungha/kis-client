"""
TODO 리밸런싱 리포트를 만들어줍니다
"""
import os
from datetime import datetime
from textwrap import dedent
from typing import Any, Dict, List

import pandas as pd
from tabulate import tabulate

from kis.core import OverseasClient


def do_rebalance(
    items: List[Dict[str, Any]],
    balance_won: float,
    balance_usd: float,
    multiplier: float = 0.95,
    as_won: bool = True,
    app_key: str = None,
    app_secret: str = None,
    account: str = None,
):
    """

    :param items:
    :param balance_won:
    :param balance_usd:
    :param multiplier:
    :param as_won:
    :return:
    """
    # validation
    required_keys = ["symbol", "weight"]
    total_weight = 0
    for item in items:
        for key in required_keys:
            if key not in item.keys():
                raise KeyError(f"No required key: {key}")
        total_weight += item["weight"]

    if total_weight > 1.0:
        raise ValueError("The sum of weights must be less than equal to 1")

    if multiplier > 1:
        raise ValueError("multiplier must be greater than equal to 1. (default 0.95)")

    client = OverseasClient(
        is_dev=True, app_key=app_key, app_secret=app_secret, account=account
    )

    currency = client.get_currency().price

    # 1. 금액 계산 + 전체 예산 계산
    total_budget = balance_usd + balance_won / currency

    for item in items:
        symbol, count = item["symbol"], item.get("count", 0)

        # get price
        price = client.quote.fetch_current_price(symbol).pretty.current

        # calculate amount
        amount = price * count

        # 전체 예산 계산
        total_budget += amount
        item.update(price=price, amount=amount)

    # 2. weight로 expect, real amount 계산
    for item in items:
        symbol, weight, price, count, amount = (
            item["symbol"],
            item["weight"],
            item["price"],
            item.get("count", 0),
            item["amount"],
        )

        # 전체 중 현재 비율
        pct = amount / total_budget

        # 예상하는 리밸런싱 금액
        expected_amount = total_budget * weight * multiplier
        expected_count = expected_amount / price
        expected_count_diff = expected_count - count
        expected_profit_or_loss = expected_amount - amount

        # 현재가로 계산했을 때 주수
        real_count = expected_amount // price
        real_count_diff = real_count - count

        # 실제 가격
        real_amount = real_count * price
        real_profit_or_loss = real_amount - amount

        item.update(
            weight=weight,
            pct=pct,
            expected_count=expected_count,
            expected_count_diff=expected_count_diff,
            expected_amount=expected_amount,
            expected_profit_or_loss=expected_profit_or_loss,
            real_count=real_count,
            real_count_diff=real_count_diff,
            real_amount=real_amount,
            real_profit_or_loss=real_profit_or_loss,
        )

    # 3. (optional) 원으로 변경
    if as_won:
        total_budget = total_budget * currency
        for item in items:
            for key in item.keys():
                if (
                    key.endswith("amount")
                    or key.endswith("price")
                    or key.endswith("profit_or_loss")
                ):
                    item[key] = item[key] * currency

    # 4. 남은 예수금 계산
    expected_balance = real_balance = total_budget
    for item in items:
        expected_balance -= item["expected_amount"]
        real_balance -= item["real_amount"]
    expected_pct = expected_balance / total_budget * 100
    real_pct = real_balance / total_budget * 100

    # 5. as dataframe
    df = pd.DataFrame(items)
    df.set_index("symbol", inplace=True)

    # 6. round
    for column in df.columns:
        if (
            "price" in column
            or column.endswith("amount")
            or column.endswith("profit_or_loss")
        ):
            if as_won:
                df[column] = df[column].astype(int)
            else:
                df[column] = df[column].round(2)
        elif "count" in column or column in ["pct", "weight"]:
            df[column] = df[column].round(2)

    # rename column
    columns = pd.DataFrame(
        [
            ["AS-IS", "count"],
            ["AS-IS", "weight"],
            ["AS-IS", "price"],
            ["AS-IS", "amount"],
            ["AS-IS", "pct"],
            ["EXPECTED", "count"],
            ["EXPECTED", "diff"],
            ["EXPECTED", "amount"],
            ["EXPECTED", "profit_or_loss"],
            ["REAL", "count"],
            ["REAL", "diff"],
            ["REAL", "amount"],
            ["REAL", "profit_or_loss"],
        ],
        columns=["", ""],
    )

    pretty_df = df.copy()
    pretty_df.columns = pd.MultiIndex.from_frame(columns)

    # 7. print
    if as_won:
        balance_info = dedent(
            f"""\
            # 요약
            ## 전체 예산
            - {total_budget:.0f} 원
            
            ## 예수금
            - AS-IS WON: {balance_won or 0:.0f} 원
            - AS-IS USD: {balance_usd or 0:.2f} $
            - Expected: {expected_balance:.0f} 원 ({expected_pct:.1f} %)
            - Real: {real_balance:.0f} 원 ({real_pct:.1f} %)
            
            ## 종목별 상세
            """
        )
    else:
        balance_info = dedent(
            f"""\
            # 요약
            ## 전체 예산
            - {total_budget:.2f} $

            ## 예수금
            - AS-IS WON: {balance_won or 0:.0f} 원
            - AS-IS USD: {balance_usd or 0:.2f} $
            - Expected: {expected_balance:.2f} $ ({expected_pct:.1f} %)
            - Real: {real_balance:.2f} $ ({real_pct:.1f} %)

            ## 종목별 상세
            """
        )

    # as str
    portfolio_info = tabulate(df, headers="keys", tablefmt="psql", floatfmt=".2f")

    # write
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    portfolio_dir = os.path.join(os.getcwd(), "portfolio", now)
    os.makedirs(portfolio_dir, exist_ok=True)
    with open(os.path.join(portfolio_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(balance_info)
        f.write(portfolio_info)

    pretty_df.to_excel(os.path.join(portfolio_dir, "detail.xlsx"))

    print(balance_info)
    print(pretty_df.to_string())

    return pretty_df
