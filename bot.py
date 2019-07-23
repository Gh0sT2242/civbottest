from __future__ import print_function
#from googletrans import Translator


import discord
import asyncio
import codecs
import random
import os
import shutil
import psutil
import time 
import datetime
import pytz
import sqlite3

from threading import Timer
import sys
import socket 
import random

import subprocess

import operator
from sortedcontainers import SortedDict
from collections import OrderedDict

import math

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def portIsAvailable(port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.bind(("127.0.0.1", port))
	except socket.error as e:
		#if e.errno == 98:
			#print("Port is already in use")
		#else:
			# something else raised the socket.error exception
			#print("Error: " + e)
		s.close()
		return False
	else:
		s.close()
		return True

	s.close()	  
	return False

#translator = Translator()

client = discord.Client()

protips = ["test one", "test2"]


#nextWhitelistGenerationTime = -1

def remove_prefix(text, prefix):
    if text.startswith(prefix): # only modify the text if it starts with the prefix
         text = text.replace(prefix, "", 1) # remove one instance of prefix
    return text
	

def my_message(msg):
    return msg.author == client.user

def search_players(ckey):
	if ckey in open('/home/1713/civ13-rp/SQL/playerlogs.txt').read():
		return ckey
	else:
		return "None"



@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	#client.loop.create_task(counting(client))


@client.event
@asyncio.coroutine
def on_message(message):

	if str(message.channel) == 'hosting' or str(message.channel) == 'website':
		return 
	elif message.content.startswith('!s '):
		message.content = remove_prefix(message.content, '!s ')
		if message.content.lower().startswith('insult'):
			split_message = message.content.split("insult ")
			if len(split_message) > 1 and len(split_message[1]) > 0:
				ckey = split_message[1]
				insults = open('insult.txt').read().splitlines()
				insult = random.choice(insults)
				yield from client.send_message(message.channel, "{}, {}".format(ckey,insult))

		elif message.content.lower().startswith('approveme'):
			split_message = message.content.split("approveme ")
			if len(split_message) > 1 and len(split_message[1]) > 0:
				ckey = split_message[1]
				accepted = False
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Consul" or role.name == "Captain" or role.name == "Senator" or role.name == "Private" or role.name == "Plebian" or role.name == "Veteran" or role.name == "Patrician" or role.name == "Sergeant" or role.name == "Legatus" or role.name == "Slave" or role.name == "Cadet":
					accepted = True 
					break
			if not accepted:
				return 
				
			split_message = message.content.split("approveme ")
			ckey = search_players(str(split_message[1]))
			if ckey.lower() in open('/home/1713/civ13-rp/SQL/approved.txt').read():
				result = "You have already been approved!"
			elif (ckey == "None"):
				result = "Invalid Ckey! Our logs show that you haven't played in the server before, or the introduced ckey has spaces and upper case letters."
			else:
				with open("/home/1713/civ13-rp/SQL/approved.txt", "a") as myfile:
					myfile.write(ckey.lower()+"="+str(message.author))
					myfile.write("\n")
				with open("/home/1713/civ13-tdm/SQL/approved.txt", "a") as myfile2:
					myfile2.write(ckey.lower()+"="+str(message.author))
					myfile2.write("\n")
				result = "You have been approved!"
				soldier = discord.utils.get(message.server.roles, name="Private")
				oldrole = discord.utils.get(message.server.roles, name="Cadet")
				yield from client.add_roles(message.author, soldier)
				yield from client.remove_roles(message.author, oldrole)
			yield from client.send_message(message.channel, result)

		elif message.content.startswith('cpu'):
			CPU_Pct= str(psutil.cpu_percent())
			yield from client.send_message(message.channel, 'CPU Usage: ' + CPU_Pct +"%")
		elif message.content.startswith('serverstatus'):
			_1715 = not portIsAvailable(1715)
			_9999 = not portIsAvailable(9999)
			server_is_up = (_1715) or (_9999)
			if not server_is_up:
				embed = discord.Embed(color=0x00ff00)
				embed.add_field(name="Server Status",value="Offline", inline=False)
				yield from client.send_message(message.channel, embed=embed)
				return
			else:
				data = None;
				if _1715:
					if os.path.isfile('/home/1713/civ13-rp/serverdata.txt') == True:
						data = codecs.open('/home/1713/civ13-rp/serverdata.txt', encoding='utf-8').read()
				else:
					embed = discord.Embed(color=0x00ff00)
					embed.add_field(name="Server Status",value="Offline", inline=False)
					yield from client.send_message(message.channel, embed=embed)
					return 
		
				data = data.replace('<b>Server Status</b>: ','')
				data = data.replace('<b>Address</b>: ', '')
				data = data.replace('<b>Map</b>: ', '')
				data = data.replace('<b>Gamemode</b>: ', '')
				data = data.replace('<b>Players</b>:','')
				data = data.replace('</b>','')
				data = data.replace('<b>','')
				data = data.replace('Whitelist: ','')
				data = data.split(";")
				#embed = discord.Embed(title="**Civ13 Bot**", color=0x00ff00)
				embed = discord.Embed(color=0x00ff00)
				embed.add_field(name="Server Status", value=data[0], inline=False)
				embed.add_field(name="Address", value='<'+data[1]+'>', inline=False)
				embed.add_field(name="Map", value=data[2], inline=False)
				embed.add_field(name="Gamemode", value=data[3], inline=False)
				embed.add_field(name="Players", value=data[4], inline=False)

			
				yield from client.send_message(message.channel, embed=embed)

		elif message.content.startswith('chinaman'):
			yield from client.send_message(message.channel, 'http://3.bp.blogspot.com/-9gpXlHPZjJo/Uab937-SZeI/AAAAAAAA6Lg/FAMDO5ecV50/s1600/DSC05808.jpg')
		elif message.content.startswith('sopademacaco'):
			yield from client.send_message(message.channel, 'https://i.kym-cdn.com/photos/images/original/001/278/910/42e.jpg')
		elif message.content.startswith('help'):
			yield from client.send_message(message.channel, '**List of Commands**: serverstatus, chinaman, sopademacaco, insult, cpu, ping, approveme, (un)whitelistme. **Staff only**: updateserver, rebuildbinaries, hostciv, killciv, restartciv, mapswap.')

		# whitelist 
		elif message.content.startswith('whitelistme'):
			split_message = message.content.split("whitelistme ")
			if len(split_message) > 1 and len(split_message[1]) > 0:
				ckey = split_message[1]
				accepted = False
				for role in message.author.roles:
					if role.name == "Admiral" or role.name == "Captain" or role.name == "Lieutenant" or role.name == "Veteran" or role.name == "Sergeant":
						accepted = True 
				if accepted:
				
					whitelist = "/home/1713/civ13-rp/SQL/whitelist.txt"
					
					open(whitelist, "a").close()
					
					with open(whitelist, "r") as search:
						for line in search:
							line = line.rstrip()  # remove '\n' at end of line
							if line == ckey+"="+str(message.author):
								yield from client.send_message(message.channel, "{} is already in the whitelist, soyboy.".format(ckey))
								return
							elif str(message.author) in line:
								yield from client.send_message(message.channel, "Woah there, {}, you already whitelisted one key! Remove the old one first.".format(str(message.author).split("#")[0]))
								return 
								
						search.close()
								
					somefile = open(whitelist, "a")
					somefile.write(ckey+"="+str(message.author))
					somefile.write("\n")
					somefile.close()
					somefile2 = open("/home/1713/civ13-tdm/SQL/whitelist.txt", "a")
					somefile2.write(ckey+"="+str(message.author))
					somefile2.write("\n")
					somefile2.close()
					
					yield from client.send_message(message.channel, "{} has been added to the whitelist.".format(ckey))
				else:
					yield from client.send_message(message.channel, "Rejected! You need to have at least the [Veteran] rank.")
			else:
				yield from client.send_message(message.channel, "Wrong format. Please try '!s whitelistme [ckey].'")
				
		elif message.content.startswith("unwhitelistme"):
			
			accepted = False
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Captain" or role.name == "Lieutenant" or role.name == "Private" or role.name == "Veteran" or role.name == "Sergeant":
					accepted = True 
					break
			if accepted:
			
				removed = "N/A"
			
				list = "/home/1713/civ13-rp/SQL/whitelist.txt"
				
				open(list, "a").close()
				
				f = open(list, "r")
				lines = f.readlines()
				f.close()
				f = open(list, "w")
				for line in lines:
					if not str(message.author) in line:
						f.write(line)
					else:
						removed = line.split("=")[0]
							
				f.close()
				list2 = "/home/1713/civ13-tdm/SQL/whitelist.txt"
				
				open(list2, "a").close()
				
				f2 = open(list2, "r")
				lines2 = f2.readlines()
				f2.close()
				f2 = open(list2, "w")
				for line2 in lines2:
					if not str(message.author) in line2:
						f2.write(line2)
					else:
						removed = line2.split("=")[0]
							
				f2.close()
				
				yield from client.send_message(message.channel, "Ckey {} has been removed from the whitelist.".format(removed))
			else:
				yield from client.send_message(message.channel, "Rejected! You need to have at least the [Veteran] rank.")
		
			
		elif message.content.startswith("updateserver"):
			accepted = False 
			for role in message.author.roles:
				if role.name == "Captain" or role.name == "Admiral":
					accepted = True 
					break 
			if accepted:
			
				yield from client.send_message(message.channel, "Now updating the server to the latest git build...")
				os.system('sudo python3 /home/1713/civ13-rp/scripts/updateserverabspaths.py')
				yield from client.send_message(message.channel, "Finished updating the server to the latest git build.")
					
				for channel in message.server.channels:
					if channel.name.lower() == "github_updates":
						yield from client.send_message(channel, "The server has been updated. Update triggered by {}. See https://github.com/civ13-SS13/civ13-rp/pulse or development channels for recent changes.".format(message.author.name))

			else:
				yield from client.send_message(message.channel, "Piss off soyboy :soyboy:")
				
		elif message.content.startswith("rebuildbinaries"):
			accepted = False 
			for role in message.author.roles:
				if role.name == "Captain" or role.name == "Admiral":
					accepted = True 
					break 
			if accepted:
			
				yield from client.send_message(message.channel, "Now updating & rebuilding server binaries to the latest git build...")
				os.system('sudo python3 /home/1713/civ13-rp/scripts/updateserverabspaths.py')
				yield from client.send_message(message.channel, "Finished updating & rebuilding server binaries to the latest git build.")

			else:
				yield from client.send_message(message.channel, "Piss off soyboy!")
		
		elif message.content.startswith("hostciv"):
		
			private = False 
			if "private" in message.content.split("hostciv")[1]:
				private = True
		
			accepted = False 
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Captain":
					accepted = True 
					break 
			if accepted:
				yield from client.send_message(message.channel, "Please wait, updating the code...")
				os.system('sudo python3 /home/1713/civ13-rp/scripts/updateserverabspaths.py')
				yield from client.send_message(message.channel, "Updated the code.")
				os.system('sudo rm -f /home/1713/civ13-rp/serverdata.txt')
				os.system('sudo DreamDaemon /home/1713/civ13-rp/civ13.dmb 1715 -trusted -webclient -logself &')
				yield from client.send_message(message.channel, "Attempted to bring up Civilization 13 (Main Server)")
				time.sleep(10) # ditto
				os.system('sudo python3 /home/1713/civ13-rp/scripts/killsudos.py')
			else:
				yield from client.send_message(message.channel, "Piss off soyboy!")
		
		elif message.content.startswith("killciv"):
		
			private = False 
			if "private" in message.content.split("killciv")[1]:
				private = True
		
			accepted = False 
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Captain":
					accepted = True 
					break 
					
			if accepted:
				os.system('sudo python3 /home/1713/civ13-rp/scripts/killciv13.py')
				yield from client.send_message(message.channel, "Attempted to kill Civilization 13 Server.")
			else:
				yield from client.send_message(message.channel, "Piss off soyboy!")
		
		elif message.content.startswith("mapswap"):
		
			private = False 
			if "private" in message.content.split("mapswap")[1]:
				private = True
		
			accepted = False 
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Captain" or role.name == "Sergeant":
					accepted = True 
					break 
					
			if accepted:
				split_message = message.content.split("mapswap ")
				if len(split_message) > 1 and len(split_message[1]) > 0:
					mapto = split_message[1]
					mapto = mapto.upper()
				if mapto == "NOMADS" or mapto == "NOMADS_DESERT" or mapto == "NOMADS_JUNGLE" or mapto == "NOMADS_PANGEA" or mapto == "NOMADS_CONTINENTAL" or mapto == "NOMADS_ICE_AGE" or mapto == "NOMADS_DIVIDE":
					yield from client.send_message(message.channel, "Swapping map to {}.".format(mapto))
					os.system('sudo python3 /home/1713/civ13-rp/scripts/mapswap.py {}'.format(mapto))
				else:	
					yield from client.send_message(message.channel, "Whoah there! I don't think that map exists!")
			else:
				yield from client.send_message(message.channel, "Piss off soyboy!")
		
				
		elif message.content.startswith("restartciv"):
		
			private = False 
			if "private" in message.content.split("restartciv")[1]:
				private = True
		
			accepted = False
			for role in message.author.roles:
				if role.name == "Admiral" or role.name == "Captain":
					accepted = True 
					break 
					
			if accepted:
				os.system('sudo python3 /home/1713/civ13-rp/scripts/restartciv13.py')
				yield from client.send_message(message.channel, "Attempted to restart Civilization 13 Server.")
			else:
				yield from client.send_message(message.channel, "Piss off soyboy!")
		
			
client.run('NDcxNDAwMTY4OTczOTI2NDMw.Dmoy9A.NTionAjYw_Y1il7QIYKhtDW8tYY')
