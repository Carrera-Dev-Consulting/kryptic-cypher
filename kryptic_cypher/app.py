"""
Module that contains the click entrypoint for our cli interface.

Currently this only contains code to run the game form the cli but this will be extended 
to also run this as a web app including a built in server with react spa app.
"""

import base64
from enum import Enum
import functools
from io import BytesIO
import shutil
from typing import IO, Callable
import click
from .cypher import Cypher, CypherWithKey, registered_cyphers


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


def resolve_cypher(
    cypher: str,
    text: str,
    input: str,
    key: str,
) -> Cypher | CypherWithKey:
    if not text and not input:
        raise click.ClickException("You must specify either -t or -i")

    cypher_instance = registered_cyphers[cypher]
    if isinstance(cypher_instance, CypherWithKey):
        if not key:
            raise click.ClickException("You must specify -k")
        result = cypher_instance.validate_key(key)
        if not result.success:
            raise click.ClickException("\n".join(result.messages))

    return cypher_instance


def process_output(output: str | None, encoded_text: IO):
    if output:
        flags = "wb" if getattr(encoded_text, "mode", None) == "b" else "w"
        with open(output, flags) as f:
            shutil.copyfileobj(encoded_text, f)
    else:
        if getattr(encoded_text, "mode", None) == "b":
            full_value = encoded_text.read()
            binary_string = base64.b64encode(full_value).decode("utf-8")
            click.echo(binary_string)
        else:
            click.echo(encoded_text.read())


@main.command("encode")
@click.option(
    "-c",
    "--cypher",
    help="The cypher to use",
    required=True,
    type=click.Choice(list(registered_cyphers.keys())),
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
        encoded_text = cypher_instance.encode(text, key)
    else:
        encoded_text = cypher_instance.encode(text)

    process_output(output, encoded_text)


@main.command("decode")
@click.option(
    "-c",
    "--cypher",
    help="The cypher to use",
    required=True,
    type=click.Choice(list(registered_cyphers.keys())),
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
