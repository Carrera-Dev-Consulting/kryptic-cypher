from kryptic_cypher.cypher.base import CypherWithKey, ValidationResult


def encode_letter(letter: str) -> str:
    """Takes letter and returns a 5 bit value as a string pattern based on the bacon table.

    **Parameters**
    - letter (str): The letter to encode

    **Returns**
    - str: The binary pattern
    """
    upper = letter.upper()
    if not upper.isalpha():
        return upper


def encode_pattern(pattern: str, key: str) -> str:
    """Takes in the pattern for the full string i.e. 01101 010010 10011 01011, and key i.e. keys and returns a string where it repeats the key matching the casing that it sees.

    **Parameters**
    - pattern (str): The binary string pattern that will be the encoded message
    - key (str): The string the binary pattern will be applied to.

    **Returns**
    - str: Encoded message
    """
    """Example:
        '10010 10101 3 10101 101010!', 'key'
        '100 101 010 1 3 10 101 101 010!'
        'Key KeY kEy K 3 Ey KeY KeY kEy!'
    """
    partial = ""
    aggregates = []
    for i in pattern:
        if i in "01":
            if partial:
                pass
            partial += i
            if partial == len(key):
                aggregates.append(partial)
                partial = ""
        else:
            aggregates.append(partial)
            partial = ""

    return key


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
    |    Z   | 10111 |     24     |

    **Examples**

    'Hello World', 'Jared' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> 'jaRED jaRed jArEd jArEd jAReD JaRed jAReD Jared jArEd jarED'
    'Hello World', 'sm' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> 'sm SM Sm sM sm sM sM'
    'Hello World', 'supercoolkeythatwillbeawesome' -> '00111 00100 01010 01010 01101 10100 01101 10000 01010 00011' -> ''
    """

    def validate_key(self, key: str) -> ValidationResult:
        pass

    def encode(self, text: str) -> str:
        pass

    def decode(self, text: str, key: str) -> str:
        pass|
