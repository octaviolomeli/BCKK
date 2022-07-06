import discord
import os
from discord.ext import commands
from everlasting import everlasting

client = commands.Bot(command_prefix='bckk!')

client.remove_command('help')


# Types in console when bot is online.
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game('Use bckk!help to see commands'))
    print('Bot is ready.')

  
# Sends a message to users saying the command they attempted does not exist
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('No such command.')
    else:
        print(error)


# Function for loading cogs
@client.command()
async def load(ctx, extension):
  client.load_extension('cogs.{}'.format(extension))

  
# Function for unloading cogs
@client.command()
async def unload(ctx, extension):
  client.unload_extension('cogs.{}'.format(extension))


# Sends users a list of commands and explains their parameters if any
@client.command()
async def help(ctx):
  covid = "COVID-19 Commands\n`bckk!covid` - sends number of cases for a state (Ex. bckk!covid Virginia)\n`bckk!ccm` - lists states with # of cases more than input (Ex. bckk!ccm 500000)\n`bckk!cdm` - lists states with # of deaths more than input (Ex. bos!cdm 17000)\n\n"
  buildon = "buildOn Commands\n`bckk!stats` - sends the stats of a member (Ex. bckk!stats Octavio Castro)\n`bckk!btop` - sends the stats of top 3 members with highest hours\n`bckk!battended` - sends the # of services a member attended (Ex. bckk!battended Octavio Castro)\n\n"
  cs = "CS Club Commands\n`bckk!projects` - show a list of projects\n`bckk!events` - show a list of planned events, like hackathons or game jams\n`bckk!month` - show the month's schedule\n`bckk!pfp` - change the bot's pfp\n\n"
  kc = "Key Club Commands\n`bckk!kcstats` - sends the stats of a member (Ex. bckk!kcstats Octavio Castro)\n`bckk!kctop` - sends the stats of top 3 members with highest hours\n`bckk!kcattended` - sends the # of services a member attended (Ex. bckk!kcattended Octavio Castro)\n\n"
  k = "KIWIN's Commands\n`bckk!khours` - sends the hours of a member (Ex. bckk!khours Octavio Castro)\n`bckk!ktop` - sends the stats of top 3 members with highest hours\n`bckk!kattended` - sends the # of services a member attended (Ex. bckk!kattended Octavio Castro)"
  emb = discord.Embed(title="Commands", description=(covid+buildon+cs+kc+k), color=2123412)
  await ctx.channel.send(embed=emb)


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

# Everlasting allows the bot to be online for an extended amount of time
everlasting()
token = os.environ['KEY']
client.run(token)