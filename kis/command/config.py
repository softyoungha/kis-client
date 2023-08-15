import configparser
import os
from textwrap import dedent

import click

from kis.constants import CONFIG_DIR, CONFIG_PATH
from kis.core import DomesticClient
from kis.utils.click_group import OrderedGroup


def attach_config_group(entrypoint: click.Group):
    """attach click group"""

    @entrypoint.group("config", cls=OrderedGroup)
    def config_group():
        """
        kis client에서 사용할 app_key, app_secret, account를 설정합니다.
        app_key, app_secret는 한국투자증권 OpenAPI 페이지에서 발급받아야 하고,
        account는 한국투자증권 계좌번호를 입력합니다.

        입력된 값은 '~/.kis/config.ini' 경로에 저장됩니다.
        """

    config_group.add_command(config_init)
    config_group.add_command(config_show)


@click.command(name="init")
def config_init():
    """
    app_key, app_secret, account를 입력받습니다.(saved: '~/.kis/config.ini')
    """
    is_config_already_exist = os.path.exists(CONFIG_PATH)

    # create config.ini
    config = configparser.ConfigParser()

    if is_config_already_exist:
        config.read(CONFIG_PATH)
        click.echo(
            "🙋‍♂️config.ini가 이미 존재합니다. 새로운 profile을 추가합니다.\n"
            f"    config location: {CONFIG_PATH}"
        )

    # get prompts
    account = click.prompt("✔ 증권계좌번호 (예: 12345678-01)", type=str)
    app_key = click.prompt("✔ app_key", type=str)
    app_secret = click.prompt("✔ app_secret", type=str)
    is_dev = click.prompt("✔ 모의투자 여부", type=str, default="n", show_default=True)
    is_dev = True if is_dev and is_dev.lower() != "n" else False

    data = {
        "app_key": app_key,
        "app_secret": app_secret,
        "account": account,
        "is_dev": is_dev,
    }

    # test connection
    try:
        test_client = DomesticClient(**data)
        test_client.quote.fetch_current_price("005930")
    except Exception as e:
        raise click.Abort(f"🙋‍♂️Connection Test Failed: {e}")

    profile_name = click.prompt(
        "✔ profile_name ", type=str, default="default", show_default=True
    )

    if profile_name in config.sections():
        if not click.confirm(
            f"🙋‍♂️입력한 profile_name('{profile_name}')이 이미 있습니다. 덮어쓰시겠습니까?",
        ):
            raise click.Abort("asdf")

    config[profile_name] = data

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)
    click.echo(f"😁 new profile '{profile_name}' added!")


@click.command(name="show")
@click.argument("profile_name", type=str, default="default")
def config_show(profile_name: str):
    """
    먼저 설정된 config
    """
    if not os.path.exists(CONFIG_PATH):
        raise click.Abort(
            "🙋‍♂️config.ini가 존재하지 않습니다. 먼저 `python -m kis config init`을 실행해주세요."
        )

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    if profile_name not in config.sections():
        raise click.Abort(f"🙋‍♂️입력한 profile_name('{profile_name}')이 존재하지 않습니다.")

    data = {
        "account": config[profile_name]["account"],
        "app_key": config[profile_name]["app_key"],
        "app_secret": config[profile_name]["app_secret"],
        "is_dev": config[profile_name]["is_dev"],
    }

    click.echo(
        dedent(
            f"""\
            [{profile_name}]
            ✔ 증권계좌번호:\t{data['account']}
            ✔ app_key:\t\t{data['app_key']}
            ✔ app_secret:\t\t{data['app_secret']}
            ✔ 모의투자 여부:\t{data['is_dev']}"""
        )
    )
