import pytest

from kryptic_cypher.cypher.ceasar import Ceasar


@pytest.fixture
def cypher():
    return Ceasar()


def test_validate_key_with_non_numeric_key_fails(cypher):
    result = cypher.validate_key("abc")

    assert result.success is False
    assert result.messages == ["Key must be numeric"]


def test_validate_key_with_numeric_key_succeeds(cypher):
    result = cypher.validate_key("7")

    assert result.success is True
    assert result.messages == []


def test_encode_with_positive_key_shifts_letters_and_preserves_punctuation(cypher):
    result = cypher.encode("Hello, World!", "2")

    assert result.success is True
    assert result.error is None
    assert result.original_text == "Hello, World!"
    assert result.new_text == "Jgnnq, Yqtnf!"


def test_decode_with_positive_key_reverses_shift(cypher):
    result = cypher.decode("Jgnnq, Yqtnf!", "2")

    assert result.success is True
    assert result.error is None
    assert result.new_text == "Hello, World!"


def test_encode_decode_round_trip(cypher):
    original = "Caesar"

    encoded = cypher.encode(original, "2")
    assert encoded.success is True
    assert encoded.error is None

    decoded = cypher.decode(encoded.new_text, "2")
    assert decoded.success is True
    assert decoded.error is None
    assert decoded.new_text == original


@pytest.mark.parametrize("key", ["-1", "-10"])
def test_encode_fails_with_negative_key(key, cypher):
    result = cypher.encode("HELLO", key)

    assert result.success is False
    assert result.error == "Key must be positive"


def test_decode_fails_with_non_numeric_key(cypher):
    result = cypher.decode("ABC", "x")

    assert result.success is False
    assert result.error == "Key must be numeric"
