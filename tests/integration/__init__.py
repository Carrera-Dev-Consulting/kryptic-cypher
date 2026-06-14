from kryptic_cypher.cypher import (
    Cypher,
    CypherResult,
    CypherWithKey,
    ValidationResult,
    register_cypher,
)

# This is to ensure we have at least two cyphers in the registry


@register_cypher
class TestCypherNoKey(Cypher):
    def encode(self, text: str) -> CypherResult:
        return CypherResult.ok(text, text)

    def decode(self, text: str) -> CypherResult:
        return CypherResult.ok(text, text)


@register_cypher
class TestCypherWithKey(CypherWithKey):
    def validate_key(self, key: str) -> ValidationResult:
        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> CypherResult:
        return CypherResult.ok(text, text + key)

    def decode(self, text: str, key: str) -> CypherResult:
        return CypherResult.ok(text, text + key)
