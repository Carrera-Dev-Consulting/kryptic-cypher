import pytest

from kryptic_cypher.cypher.ceasar_word import CaesarWordCypher


@pytest.fixture
def cypher():
    return CaesarWordCypher()


@pytest.mark.parametrize(
    "key, expected_message",
    [
        ("", "Key cannot be empty."),
        ("key123", "Key must be only letters."),
    ],
)
def test_validate_key_fails_for_invalid_key(cypher, key, expected_message):
    result = cypher.validate_key(key)

    assert result.success is False
    assert result.messages == [expected_message]


def test_validate_key_succeeds_for_alpha_key(cypher):
    result = cypher.validate_key("Goat")

    assert result.success is True
    assert result.messages == []


def test_encode_transforms_text_using_word_alphabet_and_preserves_punctuation(cypher):
    result = cypher.encode("Alex, this is cool!", "Goat")

    assert result.success is True
    assert result.error is None
    assert result.original_text == "Alex, this is cool!"
    assert result.new_text == "Gjbx, sefr fr ammj!"


def test_decode_reverses_encoded_text(cypher):
    encoded_text = "Gjbx, sefr fr ammj!"
    result = cypher.decode(encoded_text, "Goat")

    assert result.success is True
    assert result.error is None
    assert result.new_text == "Alex, this is cool!"


def test_encode_decode_round_trip(cypher):
    original = "Hello, World!"
    key = "Goat"

    encoded = cypher.encode(original, key)
    assert encoded.success is True
    assert encoded.error is None

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True
    assert decoded.error is None
    assert decoded.new_text == original
