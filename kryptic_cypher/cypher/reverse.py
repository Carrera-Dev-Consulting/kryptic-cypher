from .base import CypherResult, Cypher, ValidationResult


class ReverseCypher(Cypher):
    def encode(self, text: str | bytes) -> CypherResult:
        return CypherResult.ok(text, text[::-1])

    def decode(self, text: str | bytes) -> CypherResult:
        return CypherResult.ok(text, text[::-1])
