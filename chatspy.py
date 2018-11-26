from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
#from chatterbot.trainers import ChatterBotCorpusTrainer

##For the spreadsheet
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
##Try to download the spreadsheet from Google to retrain from
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('googleapi.json', scope)
gc = gspread.authorize(credentials)
worksheet = gc.open("ChatBot Log 1").sheet1

##Logging
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

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
#bot.set_trainer(ChatterBotCorpusTrainer)
#bot.train("data/trainingdata.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    ##Comment the next 2 lines if you no longer want this to go to the spreadsheet
    log_new_line = [userText, botReply]
    worksheet.append_row(log_new_line)
    return botReply
    #return str(bot.get_response(userText))


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=80)
