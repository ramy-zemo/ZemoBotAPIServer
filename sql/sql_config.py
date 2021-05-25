from main import conn_main, cur_main
import discord


async def sql_get_main_channel(ctx) -> discord.TextChannel:
    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT MESSAGE_CHANNEL_ID FROM CONFIG WHERE GUILD_ID=%s", (guild.id,))
    channel_db = cur_main.fetchone()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0]))
        if not channel:
            main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
            sql_change_msg_welcome_channel(guild.id, main_channel.id, main_channel.id)
            return main_channel
        else:
            return channel
    else:
        main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
        sql_change_msg_welcome_channel(guild.id, main_channel.id, main_channel.id)
        return main_channel


async def sql_get_welcome_channel(ctx) -> discord.TextChannel:
    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT WELCOME_CHANNEL_ID FROM CONFIG WHERE GUILD_ID=%s", (guild.id,))
    channel_db = cur_main.fetchall()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0][0]))
        if not channel:
            welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
            sql_change_msg_welcome_channel(guild.id, welcome_channel.id, welcome_channel.id)
            return welcome_channel
        else:
            return channel
    else:
        welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
        sql_change_msg_welcome_channel(guild.id, welcome_channel.id, welcome_channel.id)
        return welcome_channel
