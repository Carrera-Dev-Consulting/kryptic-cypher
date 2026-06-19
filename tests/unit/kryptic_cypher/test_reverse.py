import pytest

from kryptic_cypher.cypher.reverse import ReverseCypher


@pytest.fixture
def cypher():
    return ReverseCypher()


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", "olleh"),
        ("Hello, World!", "!dlroW ,olleH"),
    ],
)
def test_encode_reverses_text(cypher, text, expected):
    result = cypher.encode(text)

    assert result.success is True
    assert result.error is None
    assert result.original_text == text
    assert result.new_text == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("olleh", "hello"),
        ("!dlroW ,olleH", "Hello, World!"),
    ],
)
def test_decode_reverses_text(cypher, text, expected):
    result = cypher.decode(text)

    assert result.success is True
    assert result.error is None
    assert result.original_text == text
    assert result.new_text == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (b"hello", b"olleh"),
        (b"abc123", b"321cba"),
    ],
)
def test_encode_and_decode_support_bytes(cypher, text, expected):
    encode_result = cypher.encode(text)

    assert encode_result.success is True
    assert encode_result.error is None
    assert encode_result.original_text == text
    assert encode_result.new_text == expected

    decode_result = cypher.decode(encode_result.new_text)

    assert decode_result.success is True
    assert decode_result.error is None
    assert decode_result.new_text == text
