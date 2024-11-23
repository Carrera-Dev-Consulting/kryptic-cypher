import copy
from io import StringIO
from typing import IO
import pytest
from kryptic_cypher.cypher import Cypher, registered_cyphers, register_cypher


@pytest.fixture(autouse=True)
def clean_registry():
    existing = copy.copy(registered_cyphers)
    yield
    registered_cyphers.clear()
    registered_cyphers.update(existing)


def test_register_cypher__when_registering_not_a_class__raises_type_error():
    with pytest.raises(TypeError):
        register_cypher("not a class")


def test_register_cypher__when_registering_non_cypher_class__raises_value_error():
    class NotCypher:
        pass

    with pytest.raises(ValueError):
        register_cypher(NotCypher)


def test_register_cypher__when_registering_cypher__adds_cypher_to_registery():
    class MyCypher(Cypher):
        def encode(self, text: str) -> IO:
            return StringIO(text)

        def decode(self, text: str) -> IO:
            return StringIO(text)

    register_cypher(MyCypher)

    assert "MyCypher" in registered_cyphers
