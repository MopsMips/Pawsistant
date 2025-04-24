import discord

# Rules - Reaction Role
# This file contains the functions to add or remove roles based on the reaction of the user.


# Rules acepted
async def add_role_if_not_exists(member: discord.Member, role: discord.Role):
    if role not in member.roles:
        await member.add_roles(role)
        print(f"✅ Rolle {role.name} zu {member.display_name} hinzugefügt.")


# Rules not accepted
async def remove_role_if_exists(member: discord.Member, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
        print(f"❌ Rolle {role.name} von {member.display_name} entfernt.")
