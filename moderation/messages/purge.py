import discord
import asyncio


async def purge(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        valid_count = True
        target = cmd.bot.user
        count = 100
        if message.mentions:
            target = message.mentions[0]
            if len(args) == 2:
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        else:
            if args:
                target = None
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        if not valid_count:
            response = discord.Embed(color=0xBE1931, title=f'❗ {args[0]} is not a valid number.')
        else:
            def author_check(msg):
                return msg.author.id == target.id

            try:
                await message.delete()
            except discord.NotFound:
                pass
            if target:
                deleted = await message.channel.purge(limit=count, check=author_check)
            else:
                deleted = await message.channel.purge(limit=count)
            response = discord.Embed(color=0x77B255, title=f'✅ Deleted {len(deleted)} Messages')
    del_response = await message.channel.send(embed=response)
    await asyncio.sleep(5)
    try:
        await del_response.delete()
    except discord.NotFound:
        pass
