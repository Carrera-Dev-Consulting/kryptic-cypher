"""
Module that contains the click entrypoint for our cli interface.

This is currently only for encoding and decoding data using the encode and decode commands.
"""

import base64
from io import BytesIO
from logging import basicConfig
import os
import click
from kryptic_cypher.cypher.base import CypherResult
from .cypher import Cypher, CypherWithKey, register_all_cyphers, registered_cyphers


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
    basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
    register_all_cyphers()


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


def _run_cypher(
    action: str,
    cypher: str,
    text: str,
    input: str,
    key: str,
    output: str | None,
    binary: bool,
):
    """Shared runner for encode/decode click commands.

    action must be either 'encode' or 'decode'.
    """
    action = action.lower()
    if action not in ("encode", "decode"):
        raise click.ClickException("action must be 'encode' or 'decode'")

    cypher_instance = resolve_cypher(cypher, text, input, key)

    if input:
        with open(input, "rb" if binary else "r") as f:
            text = f.read()

    # Resolve the bound method (`encode` or `decode`) and call it.
    method = getattr(cypher_instance, action)
    if isinstance(cypher_instance, CypherWithKey):
        result = method(text, key)
    else:
        result = method(text)

    process_output(output, result)


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
    _run_cypher(
        "encode",
        cypher=cypher,
        text=text,
        input=input,
        key=key,
        output=output,
        binary=binary,
    )


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
    _run_cypher(
        "decode",
        cypher=cypher,
        text=text,
        input=input,
        key=key,
        output=output,
        binary=binary,
    )


@main.command("list")
def list_cyphers():
    for cypher in sorted(registered_cyphers.keys()):
        click.echo(
            f"{cypher}: {'keyless' if isinstance(registered_cyphers[cypher], Cypher) else 'keyed'}"
        )


@main.command("cypher")
@click.argument("cypher")
@click.argument("action", type=click.Choice(["encode", "decode"]))
@click.argument("text")
@click.option(
    "-k",
    "--key",
    help="The key to use for the cypher",
    required=False,
)
@click.option(
    "--binary",
    "-b",
    is_flag=True,
    help="Whether or not input is binary...",
)
@click.option(
    "-o",
    "--output",
    help="The output file to write text to",
    required=False,
    default=None,
)
def cypher(
    cypher: str,
    action: str,
    text: str,
    key: str,
    binary: bool,
    output: str | None,
):
    if os.path.exists(text):
        _run_cypher(action, cypher, None, text, key, output, binary)
    else:
        _run_cypher(action, cypher, text, None, key, output, binary)


try:
    from kryptic_cypher.bot import run

    @main.command("bot")
    @click.option(
        "--env-file",
        type=click.Path(
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    )
    def run_bot(env_file: str = None):
        click.echo("Executing Discord Bot...")
        run(env_file=env_file)

except ImportError:
    pass
