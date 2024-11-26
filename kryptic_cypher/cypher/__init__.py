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

If you would like to explore the existing cyphers you can find them as submodules for the `kryptic_cypher.cypher` module.
"""

from .base import register_cypher, Cypher, CypherWithKey, registered_cyphers
