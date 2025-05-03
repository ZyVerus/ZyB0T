import discord
from discord.ext import commands

# Discord IDs
ZY_USER_ID = 252646379703238657 # Host User ID
VOICE_CHANNEL_ID = 1337178246751453336 # Live Studio Voice Channel ID
TEXT_CHANNEL_ID = 1368099196493758526 # Watch Together Text Channel ID

# Channel Name Variables
LIVE_NAME = "🔴Live Studio"
DEFAULT_NAME = "🔒Hidden"
LIVE_TEXT_NAME = "🍿watch-together"
DEFAULT_TEXT_NAME = "🔒hidden"

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.messages = True
intents.message_content = True  #!live and !end commands

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Ready. Logged in as {bot.user}")
    print(f"Beep - Boop. I am...alive.")

# Function to show VC and TC
async def show_channels(guild):
    vc = guild.get_channel(VOICE_CHANNEL_ID)
    tc = guild.get_channel(TEXT_CHANNEL_ID)
    everyone = guild.default_role

    # Show VC - Only change view_channel
    vc_overwrite = vc.overwrites_for(everyone)
    if vc_overwrite.view_channel is not True:
        vc_overwrite.view_channel = True
        await vc.set_permissions(everyone, overwrite=vc_overwrite)

    # Show TC - Only change view_channel
    tc_overwrite = tc.overwrites_for(everyone)
    if tc_overwrite.view_channel is not True:
        tc_overwrite.view_channel = True
        await tc.set_permissions(everyone, overwrite=tc_overwrite)

    # Rename Channel on Live
    if vc.name != LIVE_NAME:
        await vc.edit(name=LIVE_NAME)
    if tc.name != LIVE_TEXT_NAME:
        await tc.edit(name=LIVE_TEXT_NAME)

    print("VC and TC made visible and renamed (live).")

# Function to hide VC and TC
async def hide_channels(guild):
    vc = guild.get_channel(VOICE_CHANNEL_ID)
    tc = guild.get_channel(TEXT_CHANNEL_ID)
    everyone = guild.default_role

    # Hide VC - Only change view_channel
    vc_overwrite = vc.overwrites_for(everyone)
    if vc_overwrite.view_channel is not False:
        vc_overwrite.view_channel = False
        await vc.set_permissions(everyone, overwrite=vc_overwrite)

    # Hide TC - Only change view_channel
    tc_overwrite = tc.overwrites_for(everyone)
    if tc_overwrite.view_channel is not False:
        tc_overwrite.view_channel = False
        await tc.set_permissions(everyone, overwrite=tc_overwrite)

    # Rename Channels on End
    """
    if vc.name != DEFAULT_NAME:
        await vc.edit(name=DEFAULT_NAME)
    if tc.name != DEFAULT_TEXT_NAME:
        await tc.edit(name=DEFAULT_TEXT_NAME)
    """ # Commented out to avoid Discord rate limits.
    # I've still gotta figure out how to work around these 429s.

    # Purge Channel Messages
    try:
        await tc.purge()
        print("Messages deleted from text channel.")
    except discord.Forbidden:
        print("Bot lacks permission to delete messages in the text channel.")
    except discord.HTTPException as e:
        print(f"Failed to purge messages: {e}")

    print("VC and TC hidden and renamed (end).")

# Auto-Trigger Join/Leave Live Studio
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != ZY_USER_ID:
        return
    guild = member.guild
    if after.channel and after.channel.id == VOICE_CHANNEL_ID:
        await show_channels(guild)
    elif before.channel and before.channel.id == VOICE_CHANNEL_ID:
        await hide_channels(guild)

# Manual Trigger: !live
@bot.command()
async def live(ctx):
    if ctx.author.id == ZY_USER_ID:
        await show_channels(ctx.guild)
        await ctx.message.add_reaction("✅")

# Manual Trigger: !end
@bot.command()
async def end(ctx):
    if ctx.author.id == ZY_USER_ID:
        await hide_channels(ctx.guild)
        await ctx.message.add_reaction("✅")

# Initialize Bot
bot.run("<INSERT BOT TOKEN HERE>")