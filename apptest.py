from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

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
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="sherlockholmes.sqlite3"
)



#english_bot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("data/sherlock.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=80)
