#!/usr/bin/env python3
# Import the os module.
import os
# Import the random module for randomly choosing words
import random
# Import asyncio for dealing with async funcs
import asyncio
# Import csv module for generating the wordlist
import csv
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv

import string

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the tokens from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
#CHANNEL= int(os.getenv("CHANNEL_ID"))
# Imports for the bot
import discord
from discord.ext import tasks, commands
# Create a bot
client = commands.Bot(command_prefix='!')

# Create the wordlist

with open("wordlist.csv", "r") as csvlist :
    wordlist=[]
    csvreader=csv.reader(csvlist)
    for word in csvreader :
        wordlist+= word

nb_words=len(wordlist)

letters = string.ascii_uppercase
letters

black_square=":black_large_square:"
green_square=":green_square:"
yellow_square=":yellow_square:"
skull=":skull:"

games_ongoing = {}
    
# this is a function to add spaces to a word to it looks nice on discord when sending guesses
def parse_for_output(word):
    return f" {word[0]}   {word[1]}    {word[2]}    {word[3]}   {word[4]}\n"

# this is a function to count number of times letter appears in word
def count_letter(letter, word):
    i = 0
    for c in word:
        if c==letter:
            i+=1
    return i

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def help_wordle(ctx):
    await ctx.send("This is just a stupid discord bot only three commands are supported for now :\n\n" \
    +"!start, this command starts a new game\n\n" \
        +"!guess five_letters_word, returns the result with this guess\n\n"\
            +"!stop, stops the current game and tells you the answer")

@client.command()
async def stop(ctx):
    user=ctx.author
    if not user in games_ongoing or games_ongoing[user][0] not in range(6):
        await ctx.send("There is no game to stop, start a game by using !start first")
    else :
        games_ongoing[user][0]=6
        await ctx.send("Game successfully stopped, type !start to start a new one\n" \
            +f"The word was : {games_ongoing[user][1]}")

@client.command()
async def start(ctx):
    user = ctx.author
    if not user in games_ongoing :
        games_ongoing[user]=[0, wordlist[random.randrange(0,nb_words)], set(letters),""]
    elif games_ongoing[user][0] in range(0,6) :
        await ctx.send(f'{user}, you\'re already playing a game !')
        return
    else :
        games_ongoing[user]=[0, wordlist[random.randrange(0,nb_words)], set(letters),""]
    await ctx.send("You can now play a game by inputing five letter words preceded by !guess")

@client.command()
async def guess(ctx, word_guess):
    user=ctx.author
    word_guess=word_guess.upper()
    if games_ongoing[user][0] not in range(0,6):
        await ctx.send(f"{user}, you must start a game before starting to play ! Please run !start")
        return
    if not len(word_guess)==5:
        await ctx.send(f'{user}, the word must be of length 5')
    elif word_guess not in wordlist :
        await ctx.send(f'{user}, this word doesn\'t exist')
    else :
        pattern=f"Guess number {games_ongoing[user][0]}\n"
        occurences={letter : count_letter(letter,games_ongoing[user][1]) for letter in word_guess}
        for i in range(5):
            letter=word_guess[i]
            correct_letter=games_ongoing[user][1][i]
            games_ongoing[user][2]= games_ongoing[user][2]-set(letter)
            if letter==correct_letter :
                pattern+=green_square
                occurences[letter]-=1
            elif letter in games_ongoing[user][1] and occurences[letter]!=0:
                changed = False
                for j in range(i,5):
                    if letter==word_guess[j]:
                        if word_guess[j]==games_ongoing[user][1][j]:
                            pattern+=black_square
                            changed= True
                            break
                if not changed:
                    pattern+=yellow_square
                    occurences[letter]-=1
            else:
                pattern+=black_square
        games_ongoing[user][0]+=1
        pattern=pattern+str(games_ongoing[user][0])+" /6"+"\n"+parse_for_output(word_guess)
        games_ongoing[user][3]+=pattern
        if games_ongoing[user][0]==6:
            if word_guess==games_ongoing[user][1]:
                await ctx.send(games_ongoing[user][3]+f"Congrats {user}, you win !")
            else : 
                await ctx.send(games_ongoing[user][3]+f"{user}, you lost...{skull}\nThe word was {games_ongoing[user][1]}")
        else : 
            if word_guess==games_ongoing[user][1]:
                await ctx.send(games_ongoing[user][3]+f"Congrats {user}, you win !")
                games_ongoing[user][0]=6     
            else :
                await ctx.send(str(user)+":\n"+games_ongoing[user][3] \
                        +"Here are the letters you haven't used yet : "+' ,'.join(sorted(list(games_ongoing[user][2]))))

            
client.run(os.getenv("DISCORD_TOKEN"))
