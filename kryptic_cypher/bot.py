import discord
from discord import app_commands
from discord.ext import commands

from pydantic_settings import BaseSettings

from kryptic_cypher.cypher.base import Cypher, CypherWithKey

from .cypher import registered_cyphers

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class DiscordBotConfig(BaseSettings):
    DISCORD_BOT_TOKEN: str


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        # Syncs the tree to Discord so commands appear in the client
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="ping", description="Replies with a pong!")
async def ping(interaction: discord.Interaction):
    # Use interaction.response.send_message instead of ctx.send
    await interaction.response.send_message("🏓 Pong!")


class EncodeModal(discord.ui.Modal, title="Encode Message"):
    message = discord.ui.TextInput(
        label="Message",
        placeholder="Message to encode",
        required=True,
    )
    key = discord.ui.TextInput(label="Key", placeholder="Key to use", required=False)
    cypher = discord.ui.TextInput(
        label="Cypher",
        placeholder="Cypher to use",
        required=True,
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        cypher = self.cypher.value
        message = self.message.value
        key = self.key.value

        if cypher not in registered_cyphers:
            await interaction.response.send_message(
                f"Cypher is unsupported currently... {cypher} please use {', '.join(registered_cyphers.keys())}",
                ephemeral=True,
            )
            return

        cypher_instance = registered_cyphers[cypher]
        if isinstance(cypher_instance, CypherWithKey):
            if not key:
                await interaction.response.send_message(
                    "You must specify a key for this cypher",
                    ephemeral=True,
                )
                return
            key_validation = cypher_instance.validate_key(key)
            if not key_validation.success:
                await interaction.response.send_message(
                    "\n".join(key_validation.messages),
                    ephemeral=True,
                )
                return
            response = cypher_instance.encode(message, key)
        elif isinstance(cypher_instance, Cypher):
            response = cypher_instance.encode(message)
        else:
            await interaction.response.send_message(
                f"Cypher is unsupported currently... {cypher}",
                ephemeral=True,
            )
            return
        if not response.success:
            await interaction.response.send_message(
                f"Failed to encode message: {response.error}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(response.new_text)


@bot.tree.command(
    name="encode",
    description="Writes a message to the discord channel encoded by the specified cypher",
)
async def encode(
    interaction: discord.Interaction,
):
    await interaction.response.send_modal(EncodeModal())


@bot.tree.command(
    name="decode",
    description="Allows you to see an encoded message by decoding it with the specified cypher...",
)
@app_commands.describe(
    cypher="The specific cypher to use for encoding",
    message_id="Link to message to decode",
    message="The message to decode",
    key="The key to use for encoding",
    display="Whether or not to display the decoded message",
)
@app_commands.choices(
    cypher=[
        app_commands.Choice(
            name=cypher,
            value=cypher,
        )
        for cypher in registered_cyphers.keys()
    ]
)
async def decode(
    interaction: discord.Interaction,
    cypher: str,
    message_id: str = None,
    message: str = None,
    key: str = None,
    display: bool = False,
):
    if not message and not message_id:
        await interaction.response.send_message(
            "You must specify a message to decode either by message_id or message text",
            ephemeral=True,
        )
        return
    cypher_instance = registered_cyphers[cypher]

    if message_id:
        if "://discord.com" in message_id:
            message_id = int(message_id.split("/")[-1])
        elif message_id.isnumeric():
            message_id = int(message_id)
        else:
            await interaction.response.send_message(
                "Invalid message_id, please either paste the link to the message or the numeric id",
                ephemeral=True,
            )
            return

        discord_message = await interaction.channel.fetch_message(message_id)
        message = discord_message.content

    if isinstance(cypher_instance, CypherWithKey):
        if not key:
            await interaction.response.send_message(
                "You must specify a key for this cypher",
                ephemeral=True,
            )
        key_validation = cypher_instance.validate_key(key)
        if not key_validation.success:
            await interaction.response.send_message(
                "\n".join(key_validation.messages),
                ephemeral=True,
            )
        response = cypher_instance.decode(message, key)
    elif isinstance(cypher_instance, Cypher):
        response = cypher_instance.decode(message)
    else:
        await interaction.response.send_message(
            f"Cypher is unsupported currently... {cypher}",
            ephemeral=True,
        )
        return

    if not response.success:
        await interaction.response.send_message(
            f"Failed to decode message: {response.error}",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            response.new_text, ephemeral=not display
        )


def run(
    env_file: str = None,
):
    config = DiscordBotConfig(
        _env_file=env_file,
    )
    bot.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    run()
