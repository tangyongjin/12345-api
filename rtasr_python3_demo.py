# -*- encoding:utf-8 -*-
import hashlib
import hmac
import base64

# from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging


class Client:
    def __init__(self, app_id_v, api_key_v):
        base_url = "ws://rtasr.xfyun.cn/v1/ws"
        ts = str(int(time.time()))
        tt = ("94a34f55" + ts).encode("utf-8")
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding="utf-8")

        apiKey = api_key_v.encode("utf-8")
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, "utf-8")
        self.end_tag = '{"end": true}'
        endpointer = (
            base_url + "?appid=" + app_id_v + "&ts=" + ts + "&signa=" + quote(signa)
        )
        self.words = []
        self.total_string = ""

        self.ws = create_connection(endpointer)
        # print(endpointer)
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self, audio_file_path):
        file_object = open(audio_file_path, "rb")
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            file_object.close()

        self.ws.send(bytes(self.end_tag.encode("utf-8")))
        print(self.words)
        self.total_string = "".join(self.words)
        print("🌻🌻🌻🌻🌻🌻send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    self.total_string = "".join(self.words)
                    # print(self.total_string)
                    # print(" 长度为0,可以结束.ReceiveResultEnd")
                    break
                result_dict = json.loads(result)
                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    result_1 = result_dict

                    # print(">>>>>>>>>>>>>>>>>>>>>>>>")
                    # print(result_1)
                    # print("<<<<<<<<<<<<<<<<<<<<<<<")

                    ret_json = json.loads(result_1["data"])
                    word_array = ret_json["cn"]["st"]["rt"][0]["ws"]
                    self.words = []
                    for word_dict in word_array:
                        # print(word_dict["cw"][0]["w"])
                        self.words.append(word_dict["cw"][0]["w"])

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")


if __name__ == "__main__":
    logging.basicConfig()

    app_id = ""
    api_key = ""
    file_path = r"./test.pcm"

    client = Client(app_id_v=app_id, api_key_v=api_key)
    client.send(file_path)
    print(client.total_string)
