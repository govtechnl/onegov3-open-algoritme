import pytest

from openalgoritme import specs
from openalgoritme.explain import DEFAULT_BESLUIT, load_besluit, load_yaml
from openalgoritme.paths import UITLEG_FILE
from openalgoritme.register import load_snapshot


@pytest.fixture(scope="session")
def data():
    return specs.load()


@pytest.fixture(scope="session")
def snap():
    return load_snapshot()


@pytest.fixture(scope="session")
def uitleg():
    return load_yaml(UITLEG_FILE)


@pytest.fixture(scope="session")
def besluit():
    return load_besluit(DEFAULT_BESLUIT)
