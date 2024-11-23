from io import StringIO
from tokenize import String
from typing import IO
from kryptic_cypher.cypher import (
    ValidationResult,
    register_cypher,
    Cypher,
    CypherWithKey,
)


# This is to ensure we have at least two cyphers in the registry


@register_cypher
class TestCypherNoKey(Cypher):
    def encode(self, text: str) -> IO:
        return StringIO(text)

    def decode(self, text: str) -> IO:
        return StringIO(text)


@register_cypher
class TestCypherWithKey(CypherWithKey):
    def validate_key(self, key: str) -> ValidationResult:
        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> str:
        return StringIO(text + key)

    def decode(self, text: str, key: str) -> str:
        return StringIO(text + key)
