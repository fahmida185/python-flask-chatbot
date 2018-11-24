#from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer

#For getting the spreadsheets
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import logging
logging.basicConfig(level=logging.INFO)

##Try to download the spreadsheet from Google to retrain from
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('googleapi.json', scope)

gc = gspread.authorize(credentials)

worksheet = gc.open("ChatBot Knowledge Base").sheet1

all_cells = worksheet.get_all_values()

with open('data/trainingdata.yml', 'w') as f:
    f.write("categories:\r\n")
    f.write("- Conversations")
    f.write("\r\nconversations:")
    for i in range(len(all_cells)):
        if i != 0:
            f.write("\r\n- - " + all_cells[i][0])
            f.write("\r\n  - " + all_cells[i][1])
            #print("- - " + all_cells[i][0])
            #print("  - " + all_cells[i][1])

print("I have successfully imported " + str(len(all_cells)) + " rows of data and will now retrain...")

bot = ChatBot(
    "Sherlock Holmes",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I don\'t have a response for that. What else can we talk about?'
        }
    ],
    response_selection_method=get_random_response, #Comment this out if you want best response
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="sherlockholmes.sqlite3"
)

bot.read_only=True #Comment this out if you want the bot to learn based on experience
print("Bot Learn Read Only:" + str(bot.read_only))

#You can comment these out for production later since you won't be training everytime:
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("data/trainingdata.yml")

print("I am all trained up and ready to chat!")
