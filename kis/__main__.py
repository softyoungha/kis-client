from kis import www
from click.testing import CliRunner
from streamlit.__main__ import main


if __name__ == "__main__":
    args = [
        "run",
        www.__file__,
        "--server.runOnSave", "True"
    ]
    print(args)
    runner = CliRunner()
    runner.invoke(
        main,
        ["run", www.__file__, "--server.runOnSave", "True"],
        prog_name="streamlit",
        catch_exceptions=True
    )