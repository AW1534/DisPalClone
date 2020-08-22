import discord
from discord.ext import commands, tasks
import requests
from requests.exceptions import RequestException
import json

def get_prefix(Bot, message):
    with open ('prefixes.json','r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix= '_') #get_prefix
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} {bot.user.id}')
    print(f'Going online for {len(bot.guilds)} guilds')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f'Parting with {len(bot.guilds)} servers'))

@bot.event
async def on_guild_join(guild):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@commands.has_guild_permissions(manage_guild=True)
@bot.command(case_insensitive= True)
async def prefix(ctx, prefix='-'):
    

    with open ('prefixes.json', 'r') as f:

        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(title= 'Prefix changed!', description=f"your server's new and improved prefix is **{prefix}** !", color=0x00FF00)
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)


    await ctx.send(embed=embed)

@prefix.error
async def prefix_handler(self, ctx, error):
  if isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title= '**Not Authorized!**', description= 'You need the following command to execute this command: Manage Server', color=0xff0000)
            embed.add_field(name='**Technical**', value=f'Terminal returned error `{error}`')

            await ctx.send(embed=embed)

@bot.command(case_insensitive= True)
async def inspire(ctx):

    try:
        url = 'http://inspirobot.me/api?generate=true'
        params = {'generate' : 'true'}
        response = requests.get(url, params, timeout=10)
        image = response.text
        await ctx.send(image)
        
    except RequestException:
        
        await ctx.send('Inspirobot is broken, we have no reason to live.')

@bot.command(case_insensitive= True)
async def info(ctx):
    embed = discord.Embed(title='congrats on finding this little easter egg i have hidden!', description='Here is a little info that you may want to know about the bot', color=0x00FF00)
    embed.add_field(name='**Author:**', value='By Andrew Wiltshire')
    embed.add_field(name='**Server count:**', value=f'{len(bot.guilds)}')
    embed.add_field(name='**Invite:**', value='https://discord.com/oauth2/authorize?client_id=741295925196095548&scope=bot&permissions=1544027351')
    embed.add_field(name= '**credits:**', value= f'\nFelipe\nRahul')
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)



@bot.command(case_insensitive= True)
async def help(ctx):
    embed = discord.Embed(title='help**', description='a bot that can only really use the inspirobot api ' +
                                                    'atm but is hoping to expand', color=0x00FF00)
    embed.add_field(name='**-inspire**', value='Returns an AI generated, usually crappy' + 
                    ' inspirational poster generated from inspirobot.me', inline=False)
    embed.add_field(name='**-clear**', value='clears the specified amount of messages')
    embed.add_field(name='**-embed**', value='allows you to create your own embeds!')
    embed.add_field(name='**-prefix**', value= 'allows you to choose your own prefix!')
    embed.add_field(name='Thats literally it i havent developed this bot completely yet', value= '`Insert trello page here`')
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)
    
@bot.command(case_insensitive= True)
async def clear(ctx, purgeamount=0):
    if purgeamount == 0:
        embed = discord.Embed(title= 'Invalid command!', description='You must spcify an amount of messages to delete! (1-250)', color=0xff0000)
        embed.add_field(name='example:', value='-clear 50')
        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    elif purgeamount > 250:
        embed = discord.Embed(title= 'Invalid command!', description='250 is the max ammount of messages you can delete!', color=0xff0000)
        embed.add_field(name='example:', value='-clear 50')
        embed.add_field(name='however,', value='feel free to chain this command if you need to go higher!')
        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=purgeamount)

@bot.command(case_insensitive= True)
async def invite(ctx):
    embed = discord.Embed(title= 'Invite Link', description='Here is an invite link so you can invite this bot to your own servers', color=0x00FF00)
    embed.add_field(name='This bot is in a pre-alpha state so make sure to report any bugs you find!', value='https://discord.com/oauth2/authorize?client_id=741295925196095548&scope=bot&permissions=1544027351')
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def _Debug_Log_(ctx, DebugMessage='No value specified'): 
    await ctx.send(f'sent {DebugMessage} to console')
    print(f'a user has sent a message to console: {DebugMessage}')

@bot.command(case_insensitive= True)

async def embed(ctx, title='not specified', description='not specified', fieldName='not specified', fieldValue='not specified'):
    embed = discord.Embed(title= title, description= description, color= 0x7289da)
    embed.add_field(name= fieldName, value= fieldValue)
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command(case_insensitive= True)
async def announce(ctx, channel= 'b6e67l67l67e7del6p67673he67n35656eisb76ae8787', message= 'b6e67l67l67e7del6p67673he67n35656eisb76ae8787', recipients= "@everyone"):
    if channel == 'b6e67l67l67e7del6p67673he67n35656eisb76ae8787':
        embed = discord.Embed(title= 'Invalid command!', description= 'You must specify the channel to send this message to!', color=0xff0000)
        embed.add_field(name='example:', value='`-announce 123456789105 "this is a test message lmao" @everyone @here @dispal"`')
        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    elif message  == 'b6e67l67l67e7del6p67673he67n35656eisb76ae8787':
        embed = discord.Embed(title= 'Invalid command!', description='you must specify a message to send!', color=0xff0000)
        embed.add_field(name='example:', value='`-announce 123456789105 "this is a test message lmao" @everyone @here @dispal"`')
        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    else:
        channel = bot.get_channel(channel)
        await channel.send(f'{ctx.Author} wanted to announce to {recipients}: \n {message}')
        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)

bot.run('NzQxMjk1OTI1MTk2MDk1NTQ4.Xy1foQ.hoNa8HwWsluJbVEnOoF0alo6cnw')