import discord
import asyncio
import random
from urllib.request import urlopen, quote 
from discord.ext.commands import Bot
from bs4 import BeautifulSoup
from google import google

Client = Bot(command_prefix='!')

"""Functions to ease processes"""
def bs(url):
	response = urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, "lxml")
	return soup

@Client.event
async def on_ready():
	print('Logged in as')
	print(Client.user.name)
	print(Client.user.id)
	print('-----------------------')
	await Client.change_presence(game = discord.Game(name="Type !help"))

#Add message to delete on prompt

to_delete_messages = [";;play", ";;stop", ";;skip", ";;restart", ";;replay"] 

@Client.event	
async def on_message(message):
	if message.content.startswith("$hello"):
		await Client.send_message(message.channel, 'Hi, {}!'.format(message.author))			

	if message.content.startswith("$list"):
		await Client.send_message(message.channel, "Words to delete on prompt: {}".format(to_delete_messages))

	r = [m for m in message.content.partition(' ') if m.lower() in to_delete_messages]

	if r:				
		await asyncio.sleep(1)
		await Client.delete_message(message)	

	await Client.process_commands(message)

@Client.command(pass_context=True)	
async def clear(ctx, number: int):
	mgs=[]	
	tmp= await Client.say("Working!!!")
	async for x in Client.logs_from(ctx.message.channel, limit=number):
		mgs.append(x)
	await Client.delete_messages(mgs)	
		
@Client.command(pass_context=True)
async def purge(ctx, number: int):
	tmp= await Client.say("Starting purge...")
	async for x in Client.logs_from(ctx.message.channel, limit=number):
		if x:
 			await Client.delete_message(x)

@Client.command()
async def flipcoin(number : int):	
	await Client.say(random.choice(["Heads!", "Tails!"]))

@Client.command(pass_context=True)
async def add_list(ctx, word : str):

	member = ctx.message.author	
	channel = ctx.message.channel

	if member.permissions_in(channel).administrator:
		if word.lower() not in to_delete_messages:
			to_delete_messages.append(word.lower())
			tmp = await Client.say("{} has been added to the list".format(word))
		else: 
			await Client.say("{} is already in list".format(word))	

@Client.command (pass_context=True)
async def del_list(ctx, word : str):

	member = ctx.message.author
	channel = ctx.message.channel

	if member.permissions_in(channel).administrator:

		if word.lower() in to_delete_messages:
			to_delete_messages.remove(word)
			tmp = await Client.say("{} has been deleted from the list.".format(word))

		else:
			await Client.say("Word not in list.")

@Client.command(pass_context=True)
async def search(ctx, engine : str, message):
	result = {} #Google results 	 
	link_list = [] #Youtube url results		

	if engine == 'google':
		text_to_search = ctx.message.content.replace('!search' , '').replace('google', '')
		query = quote(text_to_search)

		print ('Searching %s for:%s' % (engine, text_to_search))

		for idx, result in enumerate(google.search(text_to_search, 1), start=1):
			if idx == 6:
				break

			mes = "```{}.{} :\n {} \n``` {} \n ".format(idx, result.name, result.description, result.link) + "=" * 93
			await Client.send_message(ctx.message.channel, mes)			
	
	elif engine == 'youtube':
		text_to_search = ctx.message.content.replace('!search' , '').replace('youtube', '') 
		query = quote(text_to_search)
		
		print ('Searching %s for:%s' % (engine, text_to_search))

		url = "https://www.youtube.com/results?search_query=" + query

		soup = bs(url)		

		for vid in soup.find_all(class_='yt-uix-tile-link')[0:5]:			
			link_list.append('https://www.youtube.com' + vid['href'])

		for i in range(5):			
			await Client.send_message(ctx.message.channel, link_list[i])

""""@Client.event
async def on_error(event):
	r = '!clear + #mgs\n!purge + #mgs'
	await Client.send_message(message.channel,'Command not found.\nCommands: {}'.format(r))"""
 		
Client.run("MzE5Mjc3OTczNTQwNzAwMTcx.DA-niw.pWRWqQalc_oaq5AqkmbfJRLqNuo")
