from openai import OpenAI
import os
import subprocess

api_key = api_key = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key


def transcribe_audio(file):
    file_root, _ = os.path.splitext(file)

    output_file = file_root + ".mp3"

    command = ["ffmpeg", "-i", file, output_file]
    subprocess.run(command, check=True)
    audio_file = open(output_file, "rb")
    client = OpenAI(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    return transcription
