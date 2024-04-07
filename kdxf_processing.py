import os
import subprocess
from AudioKDXFClient import KDXFClient


def kdxf_transcribe_audio(file):
    file_root, _ = os.path.splitext(file)

    mp3_file = file_root + ".mp3"
    pcm_file = file_root + ".pcm"
    command = ["ffmpeg", "-i", file, mp3_file]
    subprocess.run(command, check=True)
    print(mp3_file)  # mp3_file is xxxx.mp3

    command = [
        "ffmpeg",
        "-y",
        "-i",
        mp3_file,
        "-acodec",
        "pcm_s16le",
        "-f",
        "s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        pcm_file,
    ]
    subprocess.run(command, check=True)
    print(pcm_file)
    app_id = ""
    api_key = ""

    client = KDXFClient(app_id_v=app_id, api_key_v=api_key)
    client.send(pcm_file)
    print(client.total_string)
    return client.total_string
