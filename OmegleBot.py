import pyautogui
import discord
from geolite2 import geolite2
import pynput
import socket, subprocess
import os
import time

"""

Code in charge of setting up connections based on user Settings

"""
# Function in charge of prompting user for TOKEN
def gettoken():
    file = open("Settings.txt", "r")
    sets = file.readlines()
    ky = input("Bot token: ")
    newsets = ""
    for p in sets:
        if "Token" in p:
            newsets += "Token:" + ky + "\n"
        else:
            newsets += p

    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    TOKEN = ky
    print("\n")
    return TOKEN


#Function in charge of prompting user to input Wireshark directory
def getdir():
    dr = input("Directory of Wireshark folder (folder inclusive): ")
    file = open("Settings.txt", "r")
    sets = file.readlines()
    newsets = ""
    for p in sets:
        if "Directory" in p:
            newsets += "Directory:" + dr + " \n"
        else:
            newsets += p
    file.close()
    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")
    sets[2] = "Directory:" + dr.strip() + "\n"
    return dr

#Function to display the available networks and asks the user to choose one, then write the network number into settings
def getnetwork():
    networkProcess = subprocess.Popen(networkList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    numLines = 0
    for line in iter(networkProcess.stdout.readline, b""):
        print(str(line)[2::])
        numLines += 1
    networkNum = 0
    while (networkNum == 0):
        try:
            networkNum = int(input("Please select the number of the network that recieves internet traffic: "))
            if networkNum < 1 or networkNum > numLines:
                raise Exception
            print("Network number selected: " + str(networkNum))
        except:
            print("Enter a valid number")
            networkNum = 0
    file = open("Settings.txt", "r")
    sets = file.readlines()
    newsets = ""
    for p in sets:
        if "Input:" in p:
            newsets += "Input:" + str(networkNum) + "\n"
        else:
            newsets += p
    file.close()
    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")
    return str(networkNum)

def on_click(x, y, button, pressed):
    if pressed:
        print("X = " + str(x) + "\nY = " + str(y))
        return False

def giveBounds(x,y):
    file = open("Settings.txt", "r")
    sets = file.readlines()
    newsets = ""
    for p in sets:
        if "Bounds:" in p:
            newsets += "Bounds:" + "x = " + str(x)  + " y = " + str(y) + "\n"
        else:
            newsets += p
    file.close()
    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")

# Checks for a Discord bot token
file = open("Settings.txt", "r")
sets = file.readlines()
file.close()
if len(sets[1]) <= 7:
    print("You haven't specified a bot token. Either look up how to make a Discord bot or ask a friend for their token.")
    TOKEN = gettoken()
    sets[1] = "Token:" + TOKEN.strip() + "\n"
else:
    TOKEN = sets[1][6::]
    file.close()

# Checks if a file directory is specified for Wireshark
if len(sets[2]) <= 11:
    print("Click into the Wireshark folder, and copy the location")
    sets[2] = "Directory:" + getdir().strip() + "\n"
    networkList = networkList = sets[2][10::].strip() + "\\tshark -D"
else:
    networkList = sets[2][10::].strip() + "\\tshark -D"

# Keeps on trying to connect to Wireshark until user inputs valid directory
proc = True
tries = 0
while proc:
    try:
        networkProcess = subprocess.Popen(networkList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc = False
    except:
        tries += 1
        if tries > 4:
            print("It looks like this isn't working. You're free to try again, but there may be an issue with your Wireshark setup.")
        else:
            print("Couldn't connect to Wireshark.")
            print("Make sure that you click into the Wireshark folder (likely found in Program Files), and then click 'Copy Address' ")
        sets[2] = "Directory:" + getdir().strip() + "\n"
        networkList = sets[2][10::].strip() + "\\tshark -D"


# Decides what network the code will pull UDP packets from (default is Wi-Fi, but some people may use Ethernet)
if len(sets[3]) <= 7:
    networkNum = 0
    for line in iter(networkProcess.stdout.readline, b""):
        if "Wi-Fi" in str(line):
            networkNum = int(line[0:1:])
    newsets = ""
    for p in sets:
        if "Input" in p:
            newsets += "Input:" + str(networkNum) + "\n"
        else:
            newsets += p

    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")
    sets[3] = "Input:" + str(networkNum).strip() + "\n"

# Asks for a UserID, but there's no way to confirm a correct ID or reset incorrect ID
if len(sets[5]) <= 8:
    print("Input your Discord user ID ('#' included) Ex. DiscordUser#0001")
    print("WARNING! If you input the wrong ID you will be forced to manually reset it through the Settings folder")
    eyedee = input("Discord ID: ")
    confirmed = False
    while not confirmed:
        confirmationInput = input("Press enter twice to confirm UserID, enter anything else to try again.")
        if confirmationInput.lower() == "":
            confirmed = True
        else:
            eyedee = input("Discord ID: ")
    sets[5] = "UserID:" + eyedee.strip() + "\n"
    newsets = ""
    for p in sets:
        if "UserID:" in p:
            newsets += "UserID:" + eyedee + "\n"
        else:
            newsets += p
    file.close()
    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")


#write function
def write(typin):
    current = pyautogui.position()
    if "std" in sets[4][6::]:
        size = str(pyautogui.size())
        x = int(size[11:15:])
        y = int(size[24:28:])
        x = int(x / 2)
        y = int(14 * y / 15)
    else:
        xandy = sets[4][7::]
        x = int(xandy[3:(xandy.find("Y") - 1):].strip())
        y = int(xandy[(xandy.find("Y") + 4):(len(xandy) - 1):])
    pyautogui.click(x,y)
    pyautogui.typewrite(typin)
    pyautogui.typewrite(['enter'])
    pyautogui.moveTo(current[0], current[1])
"""

Code in charge of Geo-location

"""


def get_ip_location(ip):
    reader = geolite2.reader()
    location = reader.get(ip)

    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"

    return country, subdivision, city

def user_location():
    cmd = r"" + sets[2][10::].strip() + "\\tshark -i " + sets[3][6::].strip()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    myIp = socket.gethostbyname(socket.gethostname())
    arrow = "\\xe2\\x86\\x92"
    print(
        "If you see this message for a long period of time, and don't observe internet traffic, there is likely an issue with the network you selected.")
    print("Use \".setup network\" without quotation to set the network to the one that recievs internet traffic.")

    i = 0
    attemptedLoc = ""
    m = 0
    for line in iter(process.stdout.readline, b""):
        columns = str(line).split(" ")
        if arrow in columns and "UDP" in columns:
            srcIp = columns[columns.index(arrow) - 1]

            if srcIp == myIp:
                continue

            try:
                country, subdivision, city = get_ip_location(srcIp)
                location = str(country +", "+ subdivision +", "+ city)
                print(">>> " + srcIp, end="\t")
                print(location)
                if city != "Unknown":
                    if i == 0:
                        attemptedLoc = location
                    if location == attemptedLoc:
                        m += 1
            except:
                print("Error")

            if i == 50:
                if m > 20:
                    return attemptedLoc
                else:
                    i = -1
                    m = 0
            i += 1

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    authenticatedUser = str(sets[5][7::]).strip()

    if message.author == client.user:
        return

    if message.content.lower().startswith('.help'):
        await message.channel.send(".msg \"message\": Send a single message\n")
        await message.channel.send(".spam \"message\": Send a message 5 times")
        await message.channel.send(".spam # \"message\": Send a message # amount of times(Limit of 20)")
        await message.channel.send(".printloc: Prints location of other Omegle user to the user")
        await message.channel.send(".discloc: Prints location of other Omegle user to Discord ONLY")
        await message.channel.send(".skip: Skips")
        await message.channel.send(".quit: Quits program(Authenticated User Only)")
        await message.channel.send(".setup help: List of available setup commands(Authenticated User Only)")
    if message.content.lower().startswith('.msg'):
        words = str(message.content)
        write(words[5::])
    if message.content.lower().startswith('.spam'):
        noDigits = False
        words = str(message.content)
        j = 0
        runs = True
        num = ""
        while runs:
            if words[j + 6].isdigit():
                num += words[j + 6]
            else:
                runs = False
            j += 1

        if num == "":
            i = 5
            noDigits = True
        else:
            i = int(num)

        w = 0
        if i <= 20:
            while w < i:
                if noDigits:
                    write(words[j + 5::])
                else:
                    write(words[j + 6::])
                w += 1
        else:
            await message.channel.send("Spam function has a limit of 20.")

        time.sleep(3)

    if message.content.lower().startswith(".printloc"):
        try:
            location = user_location()
        except(FileNotFoundError):
            print("There is an issue with wireshark directory. Use .setup wireshark location to correct the issue.")

        write(location)
    if message.content.lower().startswith(".discloc"):
        try:
            location = user_location()
            await message.channel.send(location)
        except(FileNotFoundError):
            print("There is an issue with wireshark directory. Use .setup wireshark location to correct the issue.")
    if message.content.lower().startswith(".skip"):
        pyautogui.typewrite(['esc'])
        pyautogui.typewrite(['esc'])
    if message.content.lower().startswith(".quit"):
        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "User accessed this command, reference command line to issue changes.")
            await client.close()
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in ")
    if message.content.lower().startswith(".setup help"):

        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "User accessed this command, reference command line to issue changes.")
            await message.channel.send(".setup token")
            await message.channel.send(".setup wireshark location")
            await message.channel.send(".setup network")
            await message.channel.send(".setup clicker location")
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in "
                                       "settings.txt")
    if message.content.lower().startswith(".setup token"):
        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "User accessed this command, reference command line to issue changes.")
            TOKEN = gettoken()
            sets[1] = "Token:" + TOKEN.strip() + "\n"
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in "
                                       "settings.txt")
    if message.content.lower().startswith(".setup wireshark location"):
        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "User accessed this command, reference command line to issue changes.")
            sets[2] = "Directory:" + getdir().strip() + "\n"
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in "
                                       "settings.txt")
    if message.content.lower().startswith(".setup network"):
        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "user accessed this command, reference command line to issue changes.")
            sets[3] = "Input:" + getnetwork().strip() + "\n"
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in "
                                       "settings.txt")
    if message.content.lower().startswith(".setup clicker location"):
        if str(message.author) == authenticatedUser:
            await message.channel.send("Authenticated "
                                       "user accessed this command, reference command line to issue changes.")
            print("Click on the location of the text box.(Where the program will auto click)")
            clickin = True
            while clickin:
                with pynput.mouse.Listener(on_click=on_click) as listener:
                    listener.join()
                heylisten = pyautogui.position()
                confirmationInput = input("Press enter twice to confirm location, enter anything else to try again.")
                if confirmationInput.lower() == "":
                    giveBounds(heylisten[0], heylisten[1])
                    sets[4] = "Bounds:" + "X = " + str(heylisten[0]) + " Y = " + str(heylisten[1]) + "\n"
                    print(sets[4])
                    clickin = False
                else:
                    print("Click on the location of the text box.(Where the program will auto click)")
        else:
            await message.channel.send("Unauthenticated user attempted to access a command."
                                       " If you are the host, ensure your Discord UserID is set up correctly in "
                                       "settings.txt")



try:
    client.run(TOKEN)
    os._exit(0)
except:
    file = open("Settings.txt", "r")
    sets = file.readlines()
    newsets = ""
    for p in sets:
        if "Token" in p:
            newsets += "Token:" + "\n"
        else:
            newsets += p

    file = open("Settings.txt", "w")
    file.write(newsets)
    file.close()
    print("\n")
    print("The token is not valid.")
    print("The program will now close, please input a valid token when you run the program again.")
    print("Closing in...")
    curtim = 10
    while curtim >= 0:
        time.sleep(1)
        print(curtim)
        curtim -= 1
    os._exit(0)
