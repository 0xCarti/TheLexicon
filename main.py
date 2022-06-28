import datetime
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

definitions = []
bot = commands.Bot(command_prefix='-', description='The Lexicon')


def save_lexicon(output=True):
    with open('lexicon.txt', 'w+') as file:
        for definition in definitions:
            file.write(definition + '\n')
        file.close()
        if output:
            print('Saved Lexicon! [{}]'.format(len(definitions)))


def load_lexicon():
    try:
        with open('lexicon.txt', 'r+') as file:
            global definitions
            definitions = file.readlines()
            file.close()
            print('Loaded Lexicon!\n{}'.format(definitions))
    except FileNotFoundError:
        save_lexicon(False)
        load_lexicon()


@bot.command(name='add')
async def command(ctx, *args):
    word = args[0]
    definition = ' '.join(args[1:])
    definitions.append('{} - {}'.format(word, definition))
    save_lexicon(False)
    print('Saved ``{}`` to the Lexicon!'.format('{} - {}'.format(word, definition)))
    await ctx.send('Added ``{} - {}`` to the Lexicon.'.format(word, definition))


@bot.command(name='define')
async def command(ctx, word):
    for definition in definitions:
        definition = definition.replace('[', '').replace(']', '').replace('\\n', '')
        if word.casefold() in definition.split(' - ')[0].casefold():
            return await ctx.send('``{}``'.format(definition))
    return await ctx.send('Definition not found.')


@bot.command(name='lexicon')
async def command(ctx):
    reply = '``'
    for definition in definitions:
        reply = reply + definition + '\n'
    reply = reply + '``'
    await ctx.send(reply)


@bot.command(name='delete')
async def command(ctx, word):
    for definition in definitions:
        if word.casefold() == definition.split(' - ')[0].casefold():
            definitions.remove(definition)
            save_lexicon(True)
            return await ctx.send('Removed ``{}`` from the Lexicon.')
    return await ctx.send('Definition not found.')


@bot.event
async def on_ready():
    print('The Lexicon is Online!')
    for guild in bot.guilds:
        print('Connected to server: {}'.format(guild.name))


@bot.event
async def on_guild_join(guild):
    print('Bot has connected to {} @ {}'.format(guild.name, datetime.now()))


load_lexicon()
load_dotenv('.env')
bot.run(os.getenv('TOKEN'))
