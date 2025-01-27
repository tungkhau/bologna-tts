from flask import Flask, request, send_file, jsonify
import requests
import io

app = Flask(__name__)
TTS_API_URL = "100.116.142.84"

class TTSClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def synthesize(self, endpoint, text):
        payload = {'input': text}
        response = requests.post(f"{self.api_url}/{endpoint}", json=payload)

        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            raise Exception(f"Error: {response.status_code}, {response.json()}")

client = TTSClient("http://"+TTS_API_URL +":5000")

@app.route('/<endpoint>', methods=['POST'])
def synthesize(endpoint):
    data = request.get_json()
    text = data.get('input')
    if not text:
        return jsonify({"error": "Text input is required"}), 400

    try:
        audio_file = client.synthesize(endpoint, text)
        return send_file(audio_file, as_attachment=True, download_name="output.wav", mimetype='audio/wav')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)