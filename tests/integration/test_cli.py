import os
from tempfile import TemporaryDirectory, tempdir
import pytest

from click.testing import CliRunner, Result

from kryptic_cypher.app import main


@pytest.fixture
def runner():
    return CliRunner()


def run_game_with_input(
    runner: CliRunner,
    args: str | list[str],
    cli_input: str = "",
) -> Result:
    return runner.invoke(main, args=args, input=cli_input)


def test_cli_encode__when_input_is_provided_and_no_output_file_set__prints_out_to_stdout(
    runner: CliRunner,
):
    output = "hello world"
    args = ["encode", "--cypher", "TestCypherNoKey", "--text", output]
    result = run_game_with_input(
        runner,
        args,
    )

    assert result.exit_code == 0
    assert output in result.output


def test_cli_encode__when_input_and_output_file_provided__writes_to_file(
    runner: CliRunner,
):
    output = "hello world"
    with TemporaryDirectory() as tempdir:
        args = [
            "encode",
            "--cypher",
            "TestCypherNoKey",
            "--text",
            "hello world",
            "--output",
            os.path.join(tempdir, "output.txt"),
        ]
        result = run_game_with_input(
            runner,
            args,
        )
        assert result.exit_code == 0
        with open(os.path.join(tempdir, "output.txt")) as f:
            assert f.read() == output


def test_cli_encode__when_input_with_cypher_with_key_and_no_output_file_provided__prints_out_to_stdout(
    runner: CliRunner,
):
    output = "hello worldkey"
    args = [
        "encode",
        "--cypher",
        "TestCypherWithKey",
        "--text",
        "hello world",
        "--key",
        "key",
    ]
    result = run_game_with_input(
        runner,
        args,
    )

    assert result.exit_code == 0
    assert output in result.output


def test_cli_encode__when_input_with_cypher_with_key_and_output_file_provided__writes_to_file(
    runner: CliRunner,
):
    output = "hello worldkey"
    with TemporaryDirectory() as tempdir:
        args = [
            "encode",
            "--cypher",
            "TestCypherWithKey",
            "--text",
            "hello world",
            "--key",
            "key",
            "--output",
            os.path.join(tempdir, "output.txt"),
        ]
        result = run_game_with_input(
            runner,
            args,
        )
        assert result.exit_code == 0
        with open(os.path.join(tempdir, "output.txt")) as f:
            assert f.read() == output


def test_cli_decode__when_input_is_provided_and_no_output_file_set__prints_out_to_stdout(
    runner: CliRunner,
):
    output = "hello world"
    args = ["decode", "--cypher", "TestCypherNoKey", "--text", output]
    result = run_game_with_input(
        runner,
        args,
    )

    assert result.exit_code == 0
    assert output in result.output


def test_cli_decode__when_input_and_output_file_provided__writes_to_file(
    runner: CliRunner,
):
    output = "hello world"
    with TemporaryDirectory() as tempdir:
        args = [
            "decode",
            "--cypher",
            "TestCypherNoKey",
            "--text",
            "hello world",
            "--output",
            os.path.join(tempdir, "output.txt"),
        ]
        result = run_game_with_input(
            runner,
            args,
        )
        assert result.exit_code == 0
        with open(os.path.join(tempdir, "output.txt")) as f:
            assert f.read() == output


def test_cli_decode__when_input_with_cypher_with_key_and_no_output_file_provided__prints_out_to_stdout(
    runner: CliRunner,
):
    output = "hello worldkey"
    args = [
        "decode",
        "--cypher",
        "TestCypherWithKey",
        "--text",
        "hello world",
        "--key",
        "key",
    ]
    result = run_game_with_input(
        runner,
        args,
    )

    assert result.exit_code == 0
    assert output in result.output


def test_cli_decode__when_input_with_cypher_with_key_and_output_file_provided__writes_to_file(
    runner: CliRunner,
):
    output = "hello worldkey"
    with TemporaryDirectory() as tempdir:
        args = [
            "decode",
            "--cypher",
            "TestCypherWithKey",
            "--text",
            "hello world",
            "--key",
            "key",
            "--output",
            os.path.join(tempdir, "output.txt"),
        ]
        result = run_game_with_input(
            runner,
            args,
        )
        assert result.exit_code == 0
        with open(os.path.join(tempdir, "output.txt")) as f:
            assert f.read() == output


def test_cli_list__prints_registered_cyphers(runner: CliRunner):
    result = run_game_with_input(runner, ["list"])

    assert result.exit_code == 0
    assert "TestCypherNoKey: keyless" in result.output
    assert "TestCypherWithKey: keyed" in result.output
    assert result.output.index("TestCypherNoKey") < result.output.index(
        "TestCypherWithKey"
    )


def test_cli_cypher__when_text_is_provided__encodes_with_cypher(runner: CliRunner):
    result = run_game_with_input(
        runner,
        ["cypher", "TestCypherNoKey", "encode", "hello world"],
    )

    assert result.exit_code == 0
    assert "hello world" in result.output


def test_cli_cypher__when_text_is_a_file__decodes_with_cypher(runner: CliRunner):
    with TemporaryDirectory() as tempdir:
        text_file = os.path.join(tempdir, "input.txt")
        with open(text_file, "w") as f:
            f.write("hello world")

        result = run_game_with_input(
            runner,
            ["cypher", "TestCypherWithKey", "decode", text_file, "--key", "key"],
        )

    assert result.exit_code == 0
    assert "hello worldkey" in result.output
