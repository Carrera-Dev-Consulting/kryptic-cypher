import string

from kryptic_cypher.cypher.base import CypherResult, CypherWithKey, ValidationResult


class Direction:
    ENCODE = "encode"
    DECODE = "decode"


def transform_word_into_alphabet(word: str, direction: Direction):
    unique_letters_in_order = []
    alphabet = string.ascii_lowercase
    for letter in word.lower():
        if letter not in unique_letters_in_order and letter in string.ascii_lowercase:
            unique_letters_in_order.append(letter)
            alphabet = alphabet.replace(letter, "")

    # Shift the letters to the front.
    alphabet = "".join(unique_letters_in_order) + alphabet
    translation = {}

    if direction == Direction.ENCODE:
        translation.update(zip(string.ascii_lowercase, alphabet))
        translation.update(zip(string.ascii_uppercase, alphabet.upper()))

    elif direction == Direction.DECODE:
        translation.update(zip(alphabet, string.ascii_lowercase))
        translation.update(zip(alphabet.upper(), string.ascii_uppercase))
    else:
        raise ValueError(f"Invalid direction: {direction}")

    return translation


class CaesarWordCypher(CypherWithKey):
    """
    The caesar word cypher might actually be a misnomer because it isn't really the same as a caesar cypher. in fact, i would argue it would have nothign to do with it.
    it involves using a word and taking out the alphabetical order of the letters from that and leaving the other letters of the alphabet that are unused the same.


    lets say our key is: Goat
    so we would make a new Alphabet starting with the Characters in sequence
    G O A T
    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    then we check off which ones we took on the actually alphabet line
    G O A T
    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    x           x               x         x
    and we fill in the blanks with the rest of the remaining alphabet in alphabetical order like this.

    G O A T B C D E F H I J K L M N P Q R S U V W X Y Z
    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    and now you have the the alpahbet to use to change your message

    So lets say your message is: alex this is cool.
    we look at the regular alphabet for a then we know that should become the letter above it i.e. G
    so
    G
    and then keep going with it
    GJBX SEFR FR AMMN
    and to decrypt you recreate the alphabet again
    and work in reverse i.e. read the top to find  the letter on the bottom that matches
    so we notice our G becomes an A.
    and just repeat through the cyphered text
    ALEX THIS IS COOL
    then blammo that would be the decrypted text.
    """

    @classmethod
    def validate_key(cls, key: str) -> ValidationResult:
        if not key:
            return ValidationResult.fail("Key cannot be empty.")

        if any(c not in string.ascii_letters for c in key):
            return ValidationResult.fail("Key must be only letters.")

        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> CypherResult:
        translate = transform_word_into_alphabet(key, Direction.ENCODE)
        return CypherResult.ok(text, "".join(translate.get(c, c) for c in text))

    def decode(self, text: str, key: str) -> CypherResult:
        translate = transform_word_into_alphabet(key, Direction.DECODE)
        return CypherResult.ok(text, "".join(translate.get(c, c) for c in text))
