"""
Module that contains the code for cyphers in our system.

Defines both the interfaces as well as a registery decorator to register classes as cyphers.

```python
from kryptic_cypher.cypher import register_cypher, Cypher, CypherWithKey

@register_cypher
class MyCypher(Cypher):
    def encode(self, text: str) -> str:
        # Do my encryption here 
        return text
        
    def decode(self, text: str) -> str:
        # Do my decryption here
        return text


@register_cypher
class MyCypherWithKey(CypherWithKey):
    def encode(self, text: str, key: str) -> str:
        # Do my encryption here 
        return text
        
    def decode(self, text: str, key: str) -> str:
        # Do my decryption here
        return text
```

You can use this if you want to import and leverage any existing cyphers that have been registered with us.
"""

from abc import ABC, abstractmethod
from logging import getLogger
from typing import IO


logger = getLogger(__name__)


class ValidationResult:
    def __init__(self, success: bool, messages: list[str]) -> None:
        self.success = success
        self.messages = messages

    @classmethod
    def ok(cls):
        return cls(True, [])

    @classmethod
    def fail(cls, messages: list[str]):
        return cls(False, messages)


class Cypher(ABC):
    """A Cypher that does not require a key to encode/decode."""

    @abstractmethod
    def encode(self, text: str) -> IO:  # pragma: no cover
        """Encode the given text using the given key.

        **Parameters**
        - text (str): The text to encode

        **Returns**
        - IO: The encoded text
        """
        pass

    @abstractmethod
    def decode(self, text: str) -> IO:  # pragma: no cover
        """Decode the given text using the given key.

        **Parameters**
        - text (str): The text to decode

        **Returns**
        - IO: The decoded text
        """
        pass


class CypherWithKey(ABC):
    """A Cypher that requires a key to encode/decode."""

    @classmethod
    @abstractmethod
    def validate_key(cls, key: str) -> ValidationResult:  # pragma: no cover
        """
        Validate the key for the Cypher. If the key is invalid, it should return a ValidationResult
        with a message explaining why the key is invalid.

        **Parameters**
        - key (str): The key to validate

        **Returns**
        - ValidationResult: ValidationResult indicating if the key is valid or not
        """
        pass

    @abstractmethod
    def encode(self, text: str, key: str) -> IO:  # pragma: no cover
        """Encode the given text using the given key.

        **Parameters**
        - text (str): The text to encode
        - key (str): The key to use

        **Returns**
        - IO: The encoded text
        """
        pass

    @abstractmethod
    def decode(self, text: str, key: str) -> IO:  #  pragma: no cover
        """Decode the given text using the given key.

        **Parameters**
        - text (str): The text to decode
        - key (str): The key to use

        **Returns**
        - IO: The decoded text
        """
        pass


registered_cyphers: dict[str, Cypher | CypherWithKey] = {}


def register_cypher(cypher: type) -> None:
    """Class Decorator to register type as cypher.
    Must Implment Cypher or CypherWithKey and must have a constructor that takes no args.

    **Parameters**
    - cypher (type): Type that implements Cypher or CypherWithKey

    **Raises**
    - ValueError: If cypher does not implement Cypher or CypherWithKey
    """
    if not issubclass(cypher, Cypher) and not issubclass(cypher, CypherWithKey):
        raise ValueError(f"Invalid cypher Class: {cypher}")
    name = cypher.__name__
    if name in registered_cyphers:
        logger.warning(f"Duplicate cypher: {name}")
        return
    registered_cyphers[name] = cypher()
    logger.debug(f"Registered cypher: {name}")
