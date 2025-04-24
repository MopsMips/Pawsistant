import os
import discord
from discord.ext import commands
from utils.role_utils import add_role_if_not_exists, remove_role_if_exists

reaction_message_ids = []
reaction_roles = {
    "✅": "Verified",  # Emoji : Role Name
}


def setup(bot: commands.Bot):
    global reaction_message_ids
    raw_ids = os.getenv("DISCORD_RULES_MESSAGE_ID", "")
    reaction_message_ids = [
        int(mid) for mid in raw_ids.split("/") if mid.strip().isdigit()
    ]

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.message_id not in reaction_message_ids:
            return

        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_name = reaction_roles.get(str(payload.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)
            if role and member:
                await add_role_if_not_exists(member, role)

    @bot.event
    async def on_raw_reaction_remove(payload):
        if payload.message_id not in reaction_message_ids:
            return

        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_name = reaction_roles.get(str(payload.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)
            if role and member:
                await remove_role_if_exists(member, role)
