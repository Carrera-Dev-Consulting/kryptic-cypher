"""
Module that contains the click entrypoint for our cli interface.

This is currently only for encoding and decoding data using the encode and decode commands.
"""

import base64
from io import BytesIO
import click
from kryptic_cypher.cypher.base import CypherResult
from .cypher import Cypher, CypherWithKey, registered_cyphers, register_cypher

import importlib
import inspect
import pkgutil
from typing import Type


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


@click.group()
@click.pass_context
def main(ctx: click.Context):
    """
    main group that represents the top-level: ***zombie-nomnom***

    This will be used to decorate sub-commands for zombie-nomnom.

    ***Example Usage:***
    ```python
    @main.command("sub-command")
    def sub_command():
        # do actual meaningful work.
        pass
    ```
    """
    all_to_register = find_subclasses_recursively(
        "kryptic_cypher.cypher", Cypher
    ) + find_subclasses_recursively("kryptic_cypher.cypher", CypherWithKey)

    for cypher in all_to_register:
        register_cypher(cypher)


def resolve_cypher(
    cypher: str,
    text: str,
    input: str,
    key: str,
) -> Cypher | CypherWithKey:
    if not text and not input:
        raise click.ClickException("You must specify either -t or -i")

    cypher_instance = registered_cyphers.get(cypher, None)

    if not cypher_instance:
        raise click.ClickException(
            f"Invalid cypher: {cypher}, {', '.join(registered_cyphers.keys())}"
        )

    if isinstance(cypher_instance, CypherWithKey):
        if not key:
            raise click.ClickException("You must specify -k")
        result = cypher_instance.validate_key(key)
        if not result.success:
            raise click.ClickException("\n".join(result.messages))

    return cypher_instance


def process_output(
    output: str | None,
    result: CypherResult,
):
    if not result.success:
        raise click.ClickException(result.error)

    if output:
        flags = "w" if isinstance(result.new_text, str) else "wb"
        with open(output, flags) as f:
            f.write(result.new_text)
    else:
        if isinstance(result.new_text, str):
            click.echo(result.new_text)
        else:
            encoded_text = BytesIO(result.new_text)
            full_value = encoded_text.read()
            binary_string = base64.b64encode(full_value).decode("utf-8")
            click.echo(binary_string)


@main.command("encode")
@click.option(
    "-c",
    "--cypher",
    help="The cypher to use",
    required=True,
)
@click.option("-t", "--text", help="The text to encode", required=False)
@click.option("-k", "--key", help="The input file to read text from", required=False)
@click.option("-i", "--input", help="The input file to read text from", required=False)
@click.option(
    "-o",
    "--output",
    help="The output file to write text to",
    required=False,
    type=click.Path(writable=True, dir_okay=False),
)
@click.option(
    "-b",
    "--binary",
    help="The output file to write text to",
    required=False,
    is_flag=True,
)
def encode(
    cypher: str,
    text: str,
    input: str,
    binary: bool,
    key: str,
    output: str | None,
):
    """
    CLI command to encode text using a cypher in our system that will check to make sure the usage is valid i.e. input is given and key is valid if key is required.
    """
    cypher_instance = resolve_cypher(cypher, text, input, key)

    if input:
        with open(input, "rb" if binary else "r") as f:
            text = f.read()

    if isinstance(cypher_instance, CypherWithKey):
        result = cypher_instance.encode(text, key)
    else:
        result = cypher_instance.encode(text)

    process_output(output, result)


@main.command("decode")
@click.option(
    "-c",
    "--cypher",
    help="The cypher to use",
    required=True,
)
@click.option("-t", "--text", help="The text to encode", required=False)
@click.option("-i", "--input", help="The input file to read text from", required=False)
@click.option("-k", "--key", help="The input file to read text from", required=False)
@click.option(
    "-o",
    "--output",
    help="The output file to write text to",
    required=False,
    type=click.Path(writable=True, dir_okay=False),
)
@click.option(
    "-b",
    "--binary",
    help="The output file to write text to",
    required=False,
    is_flag=True,
)
def decode(
    cypher: str,
    text: str,
    input: str,
    key: str,
    output: str,
    binary: bool,
):
    """
    CLI command to decode text using a cypher in our system that will check to make sure the usage is valid i.e. input is given and key is valid if key is required.
    """
    cypher_instance = resolve_cypher(cypher, text, input, key)
    if input:
        with open(input, "rb" if binary else "r") as f:
            text = f.read()

    if isinstance(cypher_instance, CypherWithKey):
        encoded_text = cypher_instance.decode(text, key)
    else:
        encoded_text = cypher_instance.decode(text)

    process_output(output, encoded_text)
