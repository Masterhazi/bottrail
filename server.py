from flask import Flask
import json
import os


app = Flask(__name__)

with open("quiz_bank.json", "r") as f:
    questions = json.load(f)

STATE_FILE = "state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"index": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


@app.route("/startquiz")
def startquiz():
    state = load_state()
    if state["index"] >= len(questions):
        state["index"] = 0
    q = questions[state["index"]]

    message = f"{q['question']} | {q['A']} | {q['B']} | {q['C']} | {q['D']}"

    save_state(state)
    return message


@app.route("/endquiz")
def endquiz():
    state = load_state()
    if state["index"] >= len(questions):
        state["index"] = 0

    q = questions[state["index"]]

    message = (
        f"{q['motivation']}\n"
        "Learn Python with us: https://www.youtube.com/playlist?list=PLYoPEqHJItwzvdpNwxCThQ1I0aj0uklp9"
    )

    state["index"] = (state["index"] + 1) % len(questions)
    save_state(state)

    return message



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)

