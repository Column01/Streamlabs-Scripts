import os
import sys
import random
import time
import clr
import json
import codecs
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# ---------------------------
#   Script Information/ Variables
# ---------------------------
ScriptName = "Colin's Slots"
Website = "https://www.twitch.tv/column01"
Description = "Uses twitch Emotes for a slot machine"
Creator = "Colin Andress"
Version = "1.0"
cooldowns = []
configFile = "config.json"
path = os.path.dirname(__file__)
Settings = {}
# You can change these variables however you see fit!


def Init():
    global command, currency, cooldown, ScriptName, Settings, cost, cooldown, currency, Reel, Jackpot, Triple, Double

    with open(os.path.join(path, configFile), 'r') as f:
        Settings = json.load(f)
    cost = Settings["cost"]
    cooldown = Settings["cooldown"]
    currency = Settings["currency"]
    command = Settings["command"]
    Reel = Settings["reel"]
    Jackpot = Settings["jackpot_reward"]
    Triple = Settings["triple_reward"]
    Double = Settings["double_reward"]
    return


def Execute(data):
    global cooldowns
    userid = data.User
    username = data.UserName
    #   Check if the proper command is used, the command is not on cooldown
    if data.IsChatMessage() and data.GetParam(0).lower() == command and not Parent.IsOnUserCooldown(ScriptName, command, userid):
        double_message = '{} has gotten 2 of the same emote and won {} {}!'.format(username, Double, currency)
        triple_message = '{} has gotten 3 of the same emote and won {} {}!'.format(username, Triple, currency)
        jackpot_message = '{} has hit the jackpot! You win {} {}!'.format(username, Jackpot, currency)
        # Takes away the amount the game costs and starts the slots. Also adds the user to a cooldown
        Parent.RemovePoints(userid, username, cost)
        slots()
        # Checks to see if all of the slots are not the same. If they are all not the same, the player loses the roll
        if slot1 == slot2 and slot2 == slot3 and slot1 == "KappaPride":  # Jackpot
            Parent.SendStreamMessage(jackpot_message)
            Parent.AddPoints(userid, username, Jackpot)
        # Checks if the first slot is the jackpot emote or not
        elif slot1 == slot2 and slot2 == slot3 and slot1 != "KappaPride":  # 1 and 2 and 3 not jackpot
            Parent.SendStreamMessage(triple_message)
            Parent.AddPoints(userid, username, Triple)
        elif slot1 == slot2 and slot2 != slot3:  # 1 2
            Parent.SendStreamMessage(double_message)
            Parent.AddPoints(userid, username, Double)
        elif slot2 == slot3 and slot2 != slot1:  # 2 3
            Parent.SendStreamMessage(double_message)
            Parent.AddPoints(userid, username, Double)
        elif slot1 == slot3 and slot1 != slot2:  # 3 1
            Parent.SendStreamMessage(double_message)
            Parent.AddPoints(userid, username, Double)
        elif slot1 != slot2 and slot1 != slot3 and slot3 != slot2:
            lost_message = "I'm sorry, {}, but you lost!".format(username)
            Parent.SendStreamMessage(lost_message)
        # Puts the user on cooldown and adds their name to the cooldowns list
        Parent.AddUserCooldown(ScriptName, command, userid, cooldown)
        cooldowns.append([userid, time.time() + cooldown])
    # Checks if the proper command is used, and if the user is on cooldown. If they are on cooldown, it will send a chat
    # message alerting the user and tells them how long until they can use the command again.
    elif data.IsChatMessage() and data.GetParam(0).lower() == command and Parent.IsOnUserCooldown(ScriptName, command, userid):
        # Grabs cooldown remainder and sends a chat message telling the user when they can use the command again
        cooldown_remainder = Parent.GetUserCooldownDuration(ScriptName, command, userid)
        cooldown_minutes, cooldown_seconds = divmod(cooldown_remainder, 60)
        cooldown_message = 'Sorry, {}! You are on cooldown for ' \
                           '{} minutes and {} seconds!'.format(username, cooldown_minutes, cooldown_seconds)
        Parent.SendStreamMessage(cooldown_message)
    return


def slots():
    global slot1, slot2, slot3
    slot1 = random.choice(Reel)
    slot2 = random.choice(Reel)
    slot3 = random.choice(Reel)
    roll_message = 'The slot reel has started spinning... {} ... {} ... {} ...'.format(slot1, slot2, slot3)
    Parent.SendStreamMessage(roll_message)


# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    global cooldowns

    current_time = time.time()
    # Constantly checks if any cooldowns have expired. If they have, then it will message the user to tell them they are
    # off cooldown
    for item in cooldowns:
        if current_time > item[1]:
            whisper = 'Hey, {}, you can use the slots again!'.format(item[0])
            Parent.SendStreamWhisper(item[0], whisper)
            cooldowns.remove(item)

    return


# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------
def Unload():
    global cooldowns
    cooldowns = ['']
    return
