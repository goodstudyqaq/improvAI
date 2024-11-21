from flask import Flask
from flask import request
from flask import jsonify
from gpt import impro_gpt

app = Flask(__name__)


@app.route("/api/generate", methods=["POST"])
def generate():
    req = request.get_json()
    info_type = req["info_type"]
    character = req["character"]
    print(info_type, character)

    res = "No content found."
    if info_type == "Action":
        res = impro_gpt.query_action()
    elif info_type == "Environment":
        res = impro_gpt.query_environment()
    elif info_type == "Dialogue":
        res = impro_gpt.query_dialogue(character)
    return jsonify({"content": res})


@app.route("/api/generateRole", methods=["POST"])
def generateRole():
    # log the request
    # get the request data from body
    req = request.get_json()
    name = req["name"]
    personality = req["personality"]
    print(name, personality)
    impro_gpt.add_character(name, personality)
    return jsonify({"success": True})


@app.route("/api/updateInfo", methods=["POST"])
def updateInfo():
    req = request.get_json()
    contents = req["content"]
    info_type = req["info_type"]
    print(contents, info_type)
    if info_type == "Action":
        impro_gpt.add_action(contents)
    elif info_type == "Environment":
        impro_gpt.add_environment(contents)
    elif info_type == "Dialogue":
        character = req["character"]
        impro_gpt.add_dialogue(character, contents)
    return jsonify({"success": True})
