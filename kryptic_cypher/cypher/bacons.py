import string

from kryptic_cypher.cypher.base import CypherResult, CypherWithKey, ValidationResult

characters = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 8,
    "K": 9,
    "L": 10,
    "M": 11,
    "N": 12,
    "O": 13,
    "P": 14,
    "Q": 15,
    "R": 16,
    "S": 17,
    "T": 18,
    "U": 19,
    "V": 19,
    "W": 20,
    "X": 21,
    "Y": 22,
    "Z": 23,
}


def sanitize_message(message: str) -> str:
    new_message = ""
    for letter in message.upper():
        if string.ascii_letters.find(letter) != -1:
            new_message += letter
    return new_message


class BaconsCypher(CypherWithKey):
    """
    A keyed cypher that encodes only text using a key to encode the binary value of a letter with a 5 bit value.
    The key's casing is changed to upper or lower depending on the binary value i.e. upper = 1, lower = 0.

    The following table defines what each binary 5 bit value means for each letter:

    | Letter | Code  |  Int Value |
    | ------ | ----  |  --------- |
    |    A   | 00000 |      0     |
    |    B   | 00001 |      1     |
    |    C   | 00010 |      2     |
    |    D   | 00011 |      3     |
    |    E   | 00100 |      4     |
    |    F   | 00101 |      5     |
    |    G   | 00110 |      6     |
    |    H   | 00111 |      7     |
    |   I,J  | 01000 |      8     |
    |    K   | 01001 |      9     |
    |    L   | 01010 |     10     |
    |    M   | 01011 |     11     |
    |    N   | 01100 |     12     |
    |    O   | 01101 |     13     |
    |    P   | 01110 |     14     |
    |    Q   | 01111 |     15     |
    |    R   | 10000 |     16     |
    |    S   | 10001 |     17     |
    |    T   | 10010 |     18     |
    |   U,V  | 10011 |     19     |
    |    W   | 10100 |     20     |
    |    X   | 10101 |     21     |
    |    Y   | 10110 |     22     |
    |    Z   | 10111 |     23     |

    **Examples**

    'Hello World', 'Jared' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> 'jaRED jaRed jArEd jArEd jAReD JaRed jAReD Jared jArEd jarED'
    'Hello World', 'sm' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> 'sm SM Sm sM sm sM sM'
    'Hello World', 'supercoolkeythatwillbeawesome' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> 'suPERcoOlkeYtHatWiLlbEAwESoMe suPErCOolkeyThAtwilLB'
    """

    @staticmethod
    def get_name() -> str:
        return __name__.split(".")[-1]

    def validate_key(self, key: str) -> ValidationResult:
        if len([c for c in key if c in string.ascii_letters]) < 2:
            return ValidationResult.fail(
                "Key must be at least 2 characters long with proper ascii letters."
            )
        return ValidationResult.ok()

    def encode(self, text: str, key: str) -> CypherResult:
        # Remove unsupported characters
        sanitized = sanitize_message(text)

        # Is there anything to encode?
        if len(sanitized) == 0:
            return CypherResult.fail(sanitized, "Message cannot be empty.")

        key_index = 0
        encoded = ""

        # Encode each character
        for character in sanitized:
            value = characters[character]

            # Turn the value into a 5 bit string
            for c in f"{value:05b}":

                # Check to see if we've reached the end of the key
                if key_index >= len(key):
                    key_index = 0
                    encoded += " "

                # Get the character from the key
                visual = key[key_index]
                while visual not in string.ascii_letters:
                    if visual in string.whitespace:
                        encoded += visual
                    key_index += 1
                    if key_index >= len(key):
                        key_index = 0
                        encoded += " "
                    visual = key[key_index]
                key_index += 1

                # Determine casing
                if c == "1":
                    encoded += visual.upper()
                else:
                    encoded += visual.lower()

        return CypherResult.ok(
            sanitized,
            encoded,
        )

    def decode(self, text: str, key: str) -> CypherResult:
        pieces = text.split(" ")
        # Check to make sure the text is encoded with the given key
        if set(c.lower() for c in key if c in string.ascii_letters) != set(
            "".join(pieces).lower()
        ):
            return CypherResult.fail(
                text,
                "Text is not encoded with the given key, cannot trust the decoded text.",
            )
        joined = "".join(pieces)

        # Check that the text is a multiple of 5 since we encode 5 bits at a time
        if len(joined) % 5 != 0:
            return CypherResult.fail(
                text,
                "Text is not properly encoded into 5 bit values, cannot trust the decoded text.",
            )

        message = ""
        for i in range(0, len(joined), 5):
            section = joined[i : i + 5]
            # Turn section into binary
            binary = ""
            for character in section:
                if character.isupper():
                    binary += "1"
                else:
                    binary += "0"
            true_value = int(binary, 2)

            # Deduce letter from binary and make sure to account for collisions
            possible_keys = []
            for key in characters.keys():
                if characters[key] == true_value:
                    possible_keys.append(key)

            # Add the letter to the output message
            if len(possible_keys) == 1:
                message += possible_keys[0]
            else:
                message += f"({', '.join(possible_keys)})"

        # Return the final assmbled message
        return CypherResult.ok(text, message)
