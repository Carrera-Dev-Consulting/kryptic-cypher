import pytest

from kryptic_cypher.cypher.vigenre import VigenreCypher, Direction, key_to_alphabets


@pytest.fixture
def cypher():
    return VigenreCypher()


@pytest.mark.parametrize(
    "key, expected_message",
    [
        ("", "Key cannot be empty."),
        ("two words", "Key must be a single word."),
        ("key123", "Key must be only letters."),
    ],
)
def test_validate_key_fails_for_invalid_keys(cypher, key, expected_message):
    result = cypher.validate_key(key)

    assert result.success is False
    assert result.messages == [expected_message]


def test_validate_key_succeeds_for_alpha_key(cypher):
    result = cypher.validate_key("secure")

    assert result.success is True
    assert result.messages == []


def test_encode_shifts_using_key_repeating_alphabet(cypher):
    result = cypher.encode("abcd", "ba")

    assert result.success is True
    assert result.error is None
    assert result.original_text == "abcd"
    assert result.new_text == "bbdd"


def test_decode_reverses_encode(cypher):
    plain_text = "Hello, World!"
    key = "key"

    encoded = cypher.encode(plain_text, key)
    assert encoded.success is True

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True
    assert decoded.new_text == plain_text


def test_decode_preserves_non_alphabetic_characters(cypher):
    result = cypher.decode("Rijvs, Ambpb!", "key")

    assert result.success is True
    assert result.new_text == "Hello, World!"


def test_key_to_alphabets_with_encode_and_decode():
    encode_alphabets = key_to_alphabets("b", Direction.ENCODE)
    decode_alphabets = key_to_alphabets("b", Direction.DECODE)

    assert encode_alphabets[0]["a"] == "b"
    assert decode_alphabets[0]["b"] == "a"
