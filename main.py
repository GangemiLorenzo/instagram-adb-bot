import json
import random
from time import sleep

from consolemenu import *
from consolemenu.items import *

from script import instagramBot as igbot


def runRoutine():
    try:
        with open("config.json") as json_data_file:
            data = json.load(json_data_file)
        tags = data['tags']
        random.shuffle(tags)
        bot = igbot.InstagramBot()
        bot.likeTags(tags, data['like_per_tag'])
        bot.closeInstagram()
        bot.openInstagram()
        bot.likesTrain(50)
    except:
        print('Something happen and the program had a stroke.')
        print('Make sure your android device is connected.')
        input('Press ENTER')

def printInstruction():
    print('Here you could read the instructions, if there were any...')
    input('Press ENTER')

menu = ConsoleMenu("Instagram ADB bot", "Link to repo:")
instruction = FunctionItem("Instruction", printInstruction)
run = FunctionItem("Run bot", runRoutine)

menu.append_item(instruction)
menu.append_item(run)

# Finally, we call show to show the menu and allow the user to interact
menu.show()
