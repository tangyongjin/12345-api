import tempfile
from ask_gpt_handler import ask_gpt
from ask_ollama_handler import ask_ollama
from gpt_processing import transcribe_audio
from kdxf_processing import kdxf_transcribe_audio


from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)


@app.route("/transcribe_kdxf", methods=["POST"])
def transcribe_kdxf():
    audio_file = request.files.get("audio")
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
            audio_file.save(temp.name)
            temp.flush()
            question = kdxf_transcribe_audio(temp.name)
            answer = ask_ollama(question)
            return jsonify({"transcription": question, "answer": answer})

    return jsonify({"error": "No audio file received"})


@app.route("/transcribe_gpt", methods=["POST"])
def transcribe_gpt():
    audio_file = request.files.get("audio")
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
            audio_file.save(temp.name)
            temp.flush()
            transcription = transcribe_audio(temp.name)
            question = transcription.text
            summary_obj = ask_gpt(question)
            answer = summary_obj.choices[0].text.strip()
            return jsonify({"transcription": question, "answer": answer})

    return jsonify({"error": "No audio file received"})


if __name__ == "__main__":
    app.run(debug=True)
