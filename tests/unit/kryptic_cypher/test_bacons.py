import pytest

from kryptic_cypher.cypher.bacons import BaconsCypher


def test_validate_key__when_key_too_short__fails():
    cypher = BaconsCypher()

    result = cypher.validate_key("a")

    assert result.success is False
    assert (
        "Key must be at least 2 characters long with proper ascii letters."
        in result.messages
    )


def test_validate_key__when_key_long_enough__succeeds():
    cypher = BaconsCypher()

    result = cypher.validate_key("sm")

    assert result.success is True
    assert result.messages == []


def test_encode__when_text_is_sanitized_and_encoded_returns_bacon_casing():
    cypher = BaconsCypher()

    result = cypher.encode("HELLO", "sm")

    assert result.success is True
    assert result.error is None
    assert result.original_text == "HELLO"
    assert result.new_text == "sm SM Sm sM sm sM sM sm Sm Sm sM Sm S"


def test_decode__when_text_is_encoded_with_matching_key_returns_decoded_message():
    cypher = BaconsCypher()

    encoded = "sm SM Sm sM sm sM sM sm Sm Sm sM Sm S"
    result = cypher.decode(encoded, "sm")

    assert result.success is True
    assert result.error is None
    assert result.new_text == "HELLO"


def test_decode__when_key_does_not_match_fails():
    cypher = BaconsCypher()

    encoded = "sm SM Sm sM sm sM sM sm Sm Sm sM Sm S"
    result = cypher.decode(encoded, "xy")

    assert result.success is False
    assert (
        result.error
        == "Text is not encoded with the given key, cannot trust the decoded text."
    )


def test_decode__when_text_length_is_not_multiple_of_five_fails():
    cypher = BaconsCypher()

    result = cypher.decode("sM sm", "sm")

    assert result.success is False
    assert (
        result.error
        == "Text is not properly encoded into 5 bit values, cannot trust the decoded text."
    )


def test_encode_decode__when_key_contains_spaces_round_trips():
    cypher = BaconsCypher()

    message = "HELLO"
    key = "s m"

    encoded = cypher.encode(message, key)
    assert encoded.success is True
    assert "s m" in encoded.new_text

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True
    assert decoded.new_text == message


def test_encode_decode__when_message_is_long_round_trips():
    cypher = BaconsCypher()

    message = "THE DARK FOX BROWNS BY PLANK SEZ GHOST"
    key = "super long key with spaces"

    encoded = cypher.encode(message, key)
    assert encoded.success is True
    assert encoded.new_text is not None
    assert len(encoded.new_text) > len(message)

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True
    assert decoded.new_text == "THEDARKFOXBROWNSBYPLANKSEZGHOST"


def test_encode_decode__when_key_is_mixed_case_round_trips():
    cypher = BaconsCypher()

    message = "HELLO"
    key = "Sm"

    encoded = cypher.encode(message, key)
    assert encoded.success is True, encoded.error
    assert encoded.original_text == "HELLO"

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True, decoded.error
    assert decoded.new_text == "HELLO"


def test_encode__when_message_contains_unsupported_characters_sanitizes_before_encoding():
    cypher = BaconsCypher()

    message = "Hello, World! 123"
    key = "sm"

    encoded = cypher.encode(message, key)
    assert encoded.success is True
    assert encoded.original_text == "HELLOWORLD"
    assert (
        encoded.new_text
        == "sm SM Sm sM sm sM sM sm Sm Sm sM Sm SM sM sm sM Sm SM sm sm sM sM sm sm SM"
    )

    decoded = cypher.decode(encoded.new_text, key)
    assert decoded.success is True
    assert decoded.new_text == "HELLOWORLD"
