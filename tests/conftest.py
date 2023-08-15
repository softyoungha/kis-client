import pytest
from typing import List


pytest_plugins = [
    "tests.fixtures",
    "tests.unit.domestic",
    "tests.unit.overseas",
]


def pytest_sessionstart():
    pass


def pytest_sessionfinish():
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: List[pytest.Function]):
    pass


def pytest_configure():
    """각 test에서 'shared'를 통해 output을 공유할 수 있습니다."""
    pytest.shared = {}
