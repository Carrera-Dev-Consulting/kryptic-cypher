import pytest

from kryptic_cypher.cypher.bacons import BaconsCypher


def test_validate_key__when_key_too_short__fails():
    cypher = BaconsCypher()

    result = cypher.validate_key("a")

    assert result.success is False
    assert "Key must be at least 2 characters long" in result.messages


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
