# LEAVE the /n in the python file
import discord
from datetime import datetime
from datetime import date

today = date.today()


# Grab Info
info = open('info.txt')
info_data = info.read()
info_parsed = info_data.splitlines()
token_parsed = info_parsed[0]
token_parsed = token_parsed.strip('/n')
TOKEN = token_parsed.strip('token=')
print("Using token:", TOKEN)
server_name_parsed = info_parsed[1]
server_name_parsed = server_name_parsed.strip('/n')
GUILD = server_name_parsed.strip('servername=')
print("\nAttempting to connect to '" + GUILD + "'...\n\n")

current_date = ("\n[LOG BEGINS:" + str(datetime.today()) + "]")

client = discord.Client()

logfile = open('log.txt', 'a')
logfile.write(current_date)
logfile.close()

swear_filter = True # Filter swearing...
swear_dict = ["nebula"]

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    await client.change_presence(activity=discord.Streaming(name="Minecraft Hardcore Playthrough - #41", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    print(
        f'{client.user} is connected to '
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}')
    print("\nStarting Log...\n")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
      logfile = open('log.txt', 'a')
      now = datetime.now()
      msg_contents = "\n" + "{" + now.strftime("%d/%m/%Y %H:%M:%S") + "}" + "[" + str(message.author) + "] " + message.content
      print(msg_contents)
      logfile.write(msg_contents)
      logfile.close()

    # CATCH AND REMOVE SWEARING
    lowercase = message.content
    lowercase = lowercase.lower()
    for i in swear_dict:
        if i in lowercase:
          print('\n- BOT CAUGHT', message.author, "SWEARING. -\n")
          message.delete
          response = "Hey **" + str(message.author) + "**! Swearing is bad. Don't say *'~~" + str(i) + "'~~* ever again!"
          print(response)
          await message.channel.send(response)
          msg_contents = "\nBOT CAUGHT " + str(message.author) + " SWEARING: " + response
          logfile = open('log.txt', 'a')
          logfile.write(msg_contents)
          logfile.close()
    
    if message.content == '!help' or message.content == '!checkactive' or message.content == '!savedt' or message.content == '!readcurrentdata' or message.content == '!clearfile':
      if discord.utils.get(message.author.roles, name="MEE5Control") is None:
        response = "You don't have the necessary **MEE5Control** role to tell me what to do..."
        await message.channel.send(response)
      else:
        if message.content == '!help':
            response = ":sunglasses: ***| |*** **STAFFCOMMANDS** ***| |*** :sunglasses:\n" \
                       "*!help*                       | Get list of commands.\n*!checkactive*         " \
                       "| Check if the bot is active.\n*!savedt*                   " \
                       "| Save the conversation data...\n*!readcurrentdata* | " \
                       "Get a copy of the current logs...\n*!clearfile*                 | Clear the log file..."
            await message.channel.send(response)

        if message.content == '!checkactive':
            response = "I'm currently active and recording today's communications!"
            await message.channel.send(response)

        if message.content == '!savedt':
            response = "Saving data file..."
            await message.channel.send(response)
            logfile = open('log.txt', 'a')
            logfile.write(current_date)
            logfile.close()

        if message.content == '!readcurrentdata':
            response = "Loading the current log..."
            await message.channel.send(response)
            log = open('log.txt', 'r')
            for i in log:
                response = "`" + i + "`"
                print(response)
                await message.channel.send(response)
            log.close()
        
        if message.content == '!clearfile':
            response = "Clearing log file..."
            await message.channel.send(response)
            logfile = open('log.txt', 'w')
            logfile.write(("[LOG BEGINS:" + str(datetime.today()) + "]"))
            logfile.close()

client.run(TOKEN)
