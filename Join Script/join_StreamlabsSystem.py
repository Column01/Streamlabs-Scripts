# ---------------------------------------
# Import Libraries
# ---------------------------------------
import sys
import clr
import datetime
import time

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# ---------------------------------------
# Set Variables
# ---------------------------------------
command = "!join"

# ---------------------------------------
# [Required] Script Information
# ---------------------------------------
# You can edit these variables as long as formatting stays the same (If it is an INT, leave it as an INT and same thing
# with strings.)

reward = 5000
currency = "C-Coins"
cooldown = 3600

# It's rude to take credit for other people's work, so please do not change the rest of this section.
ScriptName = "Join"
Website = "www.twitch.tv/column01"
Description = "!join will give the user {} currency and put them on cooldown".format(reward)
Creator = "Colin Andress"
Version = "2.0"
cooldowns = []


# ---------------------------------------
# [Required] Initialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global ScriptName, command, cooldown, currency
    return


# ---------------------------------------
# [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global cooldowns
    if data.IsChatMessage():
        userid = data.User
        username = data.UserName
        success_message = "{} typed !join and received {} {}! Type !coins to see your new balance.".format(username, reward, currency)

        if data.GetParam(0).lower() == command and Parent.IsOnUserCooldown(ScriptName, command, userid):
            cooldown_remainder = Parent.GetUserCooldownDuration(ScriptName, command, userid)
            cooldown_minutes, cooldown_seconds = divmod(cooldown_remainder, 60)
            cooldown_response = "Sorry, {}, you are on cooldown and cannot use this command for " \
                                "{} minutes and {} seconds!".format(username, cooldown_minutes, cooldown_seconds)
            Parent.SendTwitchMessage(cooldown_response)

        if data.GetParam(0).lower() == command and not Parent.IsOnUserCooldown(ScriptName, command, userid):
            Parent.SendTwitchMessage(success_message)
            Parent.AddPoints(userid, username, reward)
            Parent.AddUserCooldown(ScriptName, command, userid, cooldown)
            cooldowns.append([userid, time.time() + cooldown])
    return

# ---------------------------------------
# [Required] Tick Function
# ---------------------------------------


def Tick():
    global cooldowns

    current_time = time.time()

    for item in cooldowns:
        if current_time > item[1]:
            Parent.SendTwitchMessage('Hey, ' + item[0] + ', you can use the join command again!')
            cooldowns.remove(item)

    return


def Unload():
    # Triggers when the bot closes / script is reloaded return
    return
