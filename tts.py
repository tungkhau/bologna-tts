import re

from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
from waitress import serve

app = Flask(__name__)
child_inclusion_female = TTS(model_path="child_inclusion_female/best_model_30996.pth", config_path="child_inclusion_female/config.json").to("cuda")
child_inclusion_male = TTS(model_path="child_inclusion_male/best_model_128646.pth", config_path="child_inclusion_male/config.json").to("cuda")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

@app.route('/child_inclusion_female', methods=['POST'])
def child_inclusion_female():
    get_audio("child_inclusion_female.mp3")
    return send_file("output.wav", as_attachment=True)

@app.route('/child_inclusion_male', methods=['POST'])
def child_inclusion_male():
    get_audio("child_inclusion_male.mp3")
    return send_file("output.wav", as_attachment=True)

@app.route('/preadolescent_inclusion_male', methods=['POST'])
def preadolescent_inclusion_male():
    get_audio("preadolescent_inclusion_male.mp3")
    return send_file("output.wav", as_attachment=True)

@app.route('/preadolescent_inclusion_female', methods=['POST'])
def preadolescent_inclusion_female():
    get_audio("preadolescent_inclusion_female.mp3")
    return send_file("output.wav", as_attachment=True)

def get_audio(speaker):
    data = request.json
    text = data.get('input')

    if not text:
        return {"error": "Text is required"}, 400
    text = re.sub(r'[,.?!]', ',', text)
    tts.tts_to_file(text=text, file_path="output.wav", language="it", speaker_wav=speaker)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)




# @app.route('/child_inclusion_male', methods=['POST'])
# def male():
#     data = request.json
#     text = data.get('input')
#
#     if not text:
#         return {"error": "Text is required"}, 400
#     text = re.sub(r'[,.?!]', ',', text)
#     child_inclusion_male.tts_to_file(text=text, file_path="output.wav")
#     return send_file("output.wav", as_attachment=True)