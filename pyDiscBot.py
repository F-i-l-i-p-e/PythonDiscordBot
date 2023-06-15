import os             
import discord           # API
from dotenv import load_dotenv  
from datetime import datetime   # Dates and times
import csv               # CSV file

load_dotenv()            # Load variables
TOKEN = os.getenv("DISCORD_TOKEN")  # Bot token
GUILD = os.getenv("DISCORD_GUILD")  # Get name of server
fname = "memberLogon.csv"           #  CSV file name from assignment requirement - not custom

intents = discord.Intents.default()  
intents.members = True               # Enable member trakcing

client = discord.Client(intents=intents) 

@client.event
async def on_ready():     # Event when bot is ready
    print(f'{client.user} has connected to Discord!')

    # Check log fle if exist or not and create
    if not os.path.isfile(fname):
        with open(fname, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Username", "Join Date"])

    for member in client.guilds[0].members:
        with open(fname, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{member.name}", f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"])


@client.event
async def on_member_join(member):  # Member join
    with open(fname, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f"{member.name}", f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"])
    print(f"{member.name} added to the list")


@client.event
async def on_member_remove(member):  # Member leave
    lines = []
    with open(fname, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != member.name:
                lines.append(row)

    with open(fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
    print(f"{member.name} removed from the list")

client.run(TOKEN)  # Start bot
