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

from .base import *


import importlib
import inspect
import pkgutil
from typing import Type

logger = getLogger(__name__)


def find_subclasses_recursively(package_name: str, base_class: Type) -> list[Type]:
    """Recursively walks a package to find all classes implementing base_class."""
    found_classes = []

    try:
        # 1. Load the root package
        root_package = importlib.import_module(package_name)
    except ImportError:
        print(f"Error: Root package '{package_name}' could not be imported.")
        return found_classes

    # 2. Check the root package file itself for classes
    _extract_classes_from_module(root_package, base_class, found_classes)

    # 3. Guard against single-file modules that have no sub-packages
    if not hasattr(root_package, "__path__"):
        return found_classes

    # 4. Recursively walk through all submodules and sub-packages
    for module_info in pkgutil.walk_packages(
        root_package.__path__, root_package.__name__ + "."
    ):
        try:
            # Dynamically import each discovered submodule
            submodule = importlib.import_module(module_info.name)
            _extract_classes_from_module(submodule, base_class, found_classes)
        except ImportError:
            # Skip submodules that fail to import due to missing dependencies
            continue

    return found_classes


def _extract_classes_from_module(module, base_class: Type, target_list: list[Type]):
    """Helper to find matching classes inside a specific module instance."""
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure it is a subclass, isn't the base itself, and was defined in this module
        if issubclass(obj, base_class) and obj is not base_class:
            if obj.__module__ == module.__name__:
                if obj not in target_list:
                    target_list.append(obj)


def register_all_cyphers():
    logger.info("Registering all cyphers...")
    all_to_register = find_subclasses_recursively(
        "kryptic_cypher.cypher", Cypher
    ) + find_subclasses_recursively("kryptic_cypher.cypher", CypherWithKey)

    for cypher in all_to_register:
        register_cypher(cypher)
