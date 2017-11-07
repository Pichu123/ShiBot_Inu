import discord
import asyncio
import time
from discord.ext.commands import Bot
# from discord.ext import commands
# File: bot.py
# description = "Test"

#Client=discord.Client()
# client = commands.Bot(description=description, command_prefix='!')
client =  Bot(command_prefix="!")
#bot_prefix= "!"
#client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    print('Logged in')
    print('Name : {}'.format(client.user.name))
    print('ID: {}'.format(client.user.id))
    print(discord.__version__)

@client.event
async def on_message(message):
    # if message.content.startswith('!ping'):
    #     await client.send_message(message.channel, 'Pong!')
    await client.process_commands(message)

@client.command(pass_context=True)
async def ping(ctx):
    # await client.send_message(ctx.message.channel, 'Pong!')
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = time.time() - pingtime
    await client.edit_message(pingms, "The ping time is `%.01f seconds`" % ping)


@client.command(pass_context=True)
async def clear(ctx, number):
    msg = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    if not(1<=number<=100):
        await client.send_message(ctx.message.channel, 'The # of messages to be deleted has a lower limit of 1 and upper limit of 100. This upper limit is placed because of possible server request overloading.')
        await asyncio.sleep(10)
        async for x in client.logs_from(ctx.message.channel, limit = 2):
            await client.delete_message(x)
    else:
        if(number==1):
            async for x in client.logs_from(ctx.message.channel, limit = 2):
                msg.append(x)
            await client.delete_messages(msg)
        elif(2<=number<=99):
            async for x in client.logs_from(ctx.message.channel, limit = number+1):
                msg.append(x)
            await client.delete_messages(msg)
        else:
            async for x in client.logs_from(ctx.message.channel, limit = 100):
                msg.append(x)
            await client.delete_messages(msg)
            async for x in client.logs_from(ctx.message.channel, limit = 1):
                await client.delete_message(x)


@client.command(pass_context=True)
async def move(ctx, member:discord.Member=None, *, channel=None):
    try:
        member = ctx.message.mentions[0]
        server = ctx.message.server
        # channel = discord.utils.find(lambda c: c.name == channel and c.type == 'voice', ctx.message.server.channels)
        channel = discord.utils.get(client.get_all_channels(), server__name=str(server), name=channel)
        print("The member name is {0} and the server name is {1}".format(member, server))
        await client.move_member(member, channel)
        await client.send_message(ctx.message.channel, "{0} has been moved to {1}.".format(member, channel))
        print("{0} has been moved to {1}.".format(member, channel))
    except:
        if member is None:
              return await client.send_message(ctx.message.channel, "You need to mention someone to move first!")
        elif channel is None:
              return await client.send_message(ctx.message.channel, "You need to specify a channel first!")


@client.command(pass_context=True)
async def kick(ctx, member:discord.Member=None):
    try:
        await client.create_channel(ctx.message.server, 'Dumpster', type=discord.ChannelType.voice)
        await asyncio.sleep(.5)
        member = ctx.message.mentions[0]
        server = ctx.message.server
        channel = discord.utils.get(client.get_all_channels(), server__name=str(server), name='Dumpster')
        await client.move_member(member, channel)
        await asyncio.sleep(.5)
        await client.send_message(ctx.message.channel, "Time to take out the trash! :mask: ")
        await asyncio.sleep(.5)
        await client.delete_channel(channel)
        msg = []
        async for x in client.logs_from(ctx.message.channel, limit = 2):
            msg.append(x)
        await asyncio.sleep(3)
        await client.delete_messages(msg)
    except:
        print("There was a client response error")
        await client.send_message(ctx.message.channel, "Client Response Error")
        msg = []
        async for x in client.logs_from(ctx.message.channel, limit = 5):
            msg.append(x)
        await asyncio.sleep(2)
        await client.delete_messages(msg)
        await asyncio.sleep(1)
        channel = discord.utils.get(client.get_all_channels(), server__name=str(server), name='Dumpster')
        await client.delete_channel(channel)

# @move.error
# async def move_error(ctx, error):
#     if isinstance(error, commands.BadArgument):
#         await client.send_message(ctx.message.channel, "Either mistyped someone's name/the channel name or it doesn't exist.")


#ShiBot_Inu
#client.run('bot token')

# #ShiBot_Inu_2
client.run('bot token')
