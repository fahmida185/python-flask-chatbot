from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

english_bot = ChatBot(
    "Harry Potter",
    readonly=True,
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I\'m sorry. I don\'t have a response for that. What else can we talk about?'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter'
        }
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter"
)

#english_bot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")

english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("data/harrypotter.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=80)

