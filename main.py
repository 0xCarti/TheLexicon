# https://discord.com/api/oauth2/authorize?client_id=991190510783955026&permissions=275616361472&scope=bot

import datetime
import os
import re
from datetime import datetime

import _pickle as pickle
import discord
from dotenv import load_dotenv
from discord.ext import commands

from docket import Docket
from lexicon import Lexicon

bot_id = ''
definitions = []
lexicon = Lexicon()
docket = Docket()
intents = discord.Intents(message_content=True, messages=True, guilds=True)
bot = commands.Bot(command_prefix='!', description='The Lexicon', intents=intents)


def save_data(file_name: str, data):
    with open(file_name + '.pkl', 'wb') as file:
        pickle.dump(data, file, -1)
        file.close()


def load_data(file_name: str):
    with open(file_name + '.pkl', 'rb') as file:
        return pickle.load(file)


@bot.command(name='watch')
async def command(ctx, index: int = 0):
    if len(docket.links) == 0:
        return await ctx.reply('The docket is currently empty.')
    if index > len(list(docket.links)):
        return await ctx.reply('Please specify and appropriate index.')
    videos = list(docket.links)
    video = videos[index-1]
    link = docket.links.pop(video)
    await ctx.reply(f'Up next is `{video} - {link}`.')



@bot.command(name='define')
async def command(ctx, word: str = None):
    if word is None:
        return await ctx.reply('Please specify a word and definition.')
    if word.lower not in lexicon.definitions:
        return await ctx.reply('I could not find that word.')
    else:
        await ctx.reply(f'{word.lower()} - {lexicon.definitions[word.lower()]}')


@bot.command(name='lexicon')
async def command(ctx, option: str = None, word: str = None, definition: str = None):
    if option is None and word is None and definition is None:
        return await ctx.reply('Please specify an option or use **!help lexicon** for command help.')

    option = option.lower()
    if option == 'add':
        if word is None or definition is None:
            return await ctx.reply('Please specify an word and definition to add.')
        else:
            word = word.lower()
            lexicon.definitions[word] = definition
            await ctx.reply(f'Added `{word} - {definition}` to the lexicon.')
            save_data('lexicon', lexicon)
    elif option == 'remove':
        if word is None:
            return await ctx.reply('Please specify an word to remove.')
        else:
            word = word.lower()
            definition = lexicon.definitions.pop(word)
            await ctx.reply(f'Removed `{word} - {definition}` from the lexicon.')
            save_data('lexicon', lexicon)
    elif option == 'list':
        if len(lexicon.definitions) == 0:
            return await ctx.reply('The lexicon is empty.')
        output = '```'
        for definition in lexicon.definitions:
            output = output + f'{definition} - {lexicon.definitions[definition]}\n'
        output = output + '```'
        await ctx.reply(output)
    else:
        return await ctx.reply(f'Unknown lexicon command: {option}')


@bot.command(name='docket')
async def command(ctx, option: str = None, video_title: str = None, link: str = None):
    if option is None and video_title is None and link is None:
        return await ctx.reply('Please specify an option or use **!help lexicon** for command help.')

    option = option.lower()
    if option == 'add':
        if video_title is None or link is None:
            return await ctx.reply('Please specify an word and definition to add.')
        else:
            video_title = video_title.lower()
            docket.links[video_title] = link
            await ctx.reply(f'Added `{video_title} - {link}` to the docket.')
            save_data('docket', docket)
    elif option == 'remove':
        if video_title is None:
            return await ctx.reply('Please specify an video link to remove.')
        else:
            video_title = video_title.lower()
            link = docket.links.pop(video_title)
            await ctx.reply(f'Removed `{video_title} - {link}` from the docket.')
            save_data('docket', docket)
    elif option == 'list':
        if len(docket.links) == 0:
            return await ctx.reply('The docket is empty.')
        output = '```'
        for video in docket.links:
            output = output + f'{list(docket.links).index(video)+1}: {video} - {docket.links[video]}\n'
        output = output + '```'
        await ctx.reply(output)
    else:
        return await ctx.reply(f'Unknown docket command: {option}')


@bot.event
async def on_ready():
    global lexicon, docket

    try:
        lexicon = load_data('lexicon')
    except FileNotFoundError:
        lexicon = Lexicon()
        save_data('lexicon', lexicon)
    print(f'Loaded {len(lexicon.definitions)} definitions into the lexicon.')

    try:
        docket = load_data('docket')
    except FileNotFoundError:
        docket = Docket()
        save_data('docket', docket)
    print(f'Loaded {len(docket.links)} links into the docket.')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print('The Lexicon is Online!')
    for guild in bot.guilds:
        print('Connected to server: {}'.format(guild.name))


@bot.event
async def on_guild_join(guild):
    print('Bot has connected to {} @ {}'.format(guild.name, datetime.now()))


@bot.event
async def on_message(message):
    regex = re.compile(r'/[(http(s)?)://(www.)?a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/')
    if not message.author.bot:
        if '/f' in message.content:
            await message.delete()
            msg = message.content.replace('/f', '').strip()
            msg = '```{}\n-{}```'.format(msg, message.author.display_name)
        elif regex.search(message.content):
            await message.delete()
            msg = '```{}```'.format(message.content)
        else:
            return await bot.process_commands(message)

        webhook = None
        hooks = await message.channel.webhooks()
        for hook in hooks:
            if hook.user == bot.user:
                webhook = hook
        if webhook is None:
            webhook = await message.channel.create_webhook(name=message.author.display_name)
        avatar = message.author.guild_avatar
        if avatar is None:
            url = message.author.avatar.url
        else:
            url = avatar
        await webhook.send(content=msg, avatar_url=url, username=message.author.display_name)


load_dotenv('.env')
bot.run(os.getenv('TOKEN'))
