import string

from kryptic_cypher.cypher.base import CypherResult, CypherWithKey, ValidationResult
from .ceasar import LOWER_ALPHABET, create_alpahbet, create_reverse_alphabet


class Direction:
    ENCODE = "encode"
    DECODE = "decode"


def key_to_alphabets(key: str, direction: Direction) -> list[dict[str, str]]:
    alpha_method = (
        create_alpahbet if direction == Direction.ENCODE else create_reverse_alphabet
    )
    all_alphabets = []

    for letter in key.lower():

        shift_value = LOWER_ALPHABET.index(letter)
        if shift_value < 0:
            raise ValueError("Somehow got a letter that isn't in the alphabet.")

        all_alphabets.append(alpha_method(shift_value))
    return all_alphabets


class VigenreCypher(CypherWithKey):
    """
    The Vigen\u00e9re Cypher is a polyalphabetic cypher based on the use of mulitple Caesar Cyphers to encrypt.

    First you choose the message you wish to encrypt and then a key word or phrase if you want
        text: This is something important
        key: sure

    then you place the key under the text to start the encryption
        encrypt: This is something important
                 sure su resuresur suresures

    we use the ordinal value of the key for example and shift each letter by that amount to encrypt the phrase.
         t  h  i s
         s  u  r e
        18 20 17 4

        so then t would be l, h would be b, i would be z, and s would be w and so forth for a fully encoded phrase of
        Encrypted: lbzw am jseyklahx mejfvluex

    """

    @classmethod
    def validate_key(cls, key: str):
        if not key:
            return ValidationResult.fail("Key cannot be empty.")
        keys = key.split(" ")
        if len(keys) > 1:
            return ValidationResult.fail("Key must be a single word.")
        if any(c not in string.ascii_letters for c in key):
            return ValidationResult.fail("Key must be only letters.")

        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> CypherResult:
        alphabits = key_to_alphabets(key, Direction.ENCODE)
        encoded_text = ""
        alphbits_index = 0
        for letter in text:
            alphabet = alphabits[alphbits_index % len(alphabits)]
            encoded_text += alphabet.get(letter, letter)
            alphbits_index += 1
        return CypherResult.ok(text, encoded_text)

    def decode(self, text: str, key: str) -> CypherResult:
        alphabits = key_to_alphabets(key, Direction.DECODE)
        decoded_text = ""
        alphbits_index = 0
        for letter in text:
            alphabet = alphabits[alphbits_index % len(alphabits)]
            decoded_text += alphabet.get(letter, letter)
            alphbits_index += 1
        return CypherResult.ok(text, decoded_text)
