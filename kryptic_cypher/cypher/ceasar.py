"""Caesar cipher implementation for encrypting and decrypting text with a numeric key."""

from .base import CypherResult, CypherWithKey, ValidationResult


def create_alpahbet(key: int):
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    translation_dictionary = {}
    for cypher_index, original_index in zip(
        range(key, key + len(upper_alphabet)),
        range(len(upper_alphabet)),
    ):
        cypher_index_character = cypher_index % len(upper_alphabet)
        translation_dictionary[upper_alphabet[original_index]] = upper_alphabet[
            cypher_index_character
        ]

    for cypher_index, original_index in zip(
        range(key, key + len(lower_alphabet)),
        range(len(lower_alphabet)),
    ):
        cypher_index_character = cypher_index % len(lower_alphabet)
        translation_dictionary[lower_alphabet[original_index]] = lower_alphabet[
            cypher_index_character
        ]

    return translation_dictionary


def create_reverse_alphabet(key: int):
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    translation_dictionary = {}
    for cypher_index, original_index in zip(
        range(key, key + len(upper_alphabet)),
        range(len(upper_alphabet)),
    ):
        cypher_index_character = cypher_index % len(upper_alphabet)
        translation_dictionary[upper_alphabet[cypher_index_character]] = upper_alphabet[
            original_index
        ]

    for cypher_index, original_index in zip(
        range(key, key + len(lower_alphabet)),
        range(len(lower_alphabet)),
    ):
        cypher_index_character = cypher_index % len(lower_alphabet)
        translation_dictionary[lower_alphabet[cypher_index_character]] = lower_alphabet[
            original_index
        ]

    return translation_dictionary


class Ceasar(CypherWithKey):
    """
    The Caeser Cypher uses each letter and shifts it the given number of times in the alphabet.

    EX:

    Given Phrase: Caesar
    Key: 2

    To encrypt the given phrase we first get the full alphabet and shift each letter by the key.

    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    CDEFGHIJKLMNOPQRSTUVWXYZAB

    After shifting the alphabet we can then input our new letters for our phrase.

    Encrypted: Ecguct

    To decrypt just do the opposite to the alphabet with the key shifting.

    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    YZABCDEFGHIJKLMNOPQRSTUVWX

    Again we just input the shifted text into the decoded text.

    Decoded: Caesar
    """

    @classmethod
    def validate_key(cls, key):
        if not key.isnumeric():
            return ValidationResult.fail("Key must be numeric")
        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> CypherResult:
        try:
            true_key = int(key)
        except ValueError:
            return CypherResult.fail(text, "Key must be numeric")

        if true_key < 0:
            return CypherResult.fail(text, "Key must be positive")

        alphabet = create_alpahbet(true_key)
        encoded_text = ""
        for letter in text:
            # If the letter is a space then just add it
            encoded_text += alphabet.get(letter, letter)
        return CypherResult.ok(text, encoded_text)

    def decode(self, text: str, key: str) -> CypherResult:
        try:
            true_key = int(key)
        except ValueError:
            return CypherResult.fail(text, "Key must be numeric")

        if true_key < 0:
            return CypherResult.fail(text, "Key must be positive")

        alphabet = create_reverse_alphabet(true_key)
        decoded_text = ""
        for letter in text:
            # If the letter is a space then just add it
            decoded_text += alphabet.get(letter, letter)
        return CypherResult.ok(text, decoded_text)
