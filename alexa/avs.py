#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from hyper import HTTP20Connection
import json
import threading
from creds import *
import time
import re

class Avs:
    ENDPOINT = 'avs-alexa-na.amazon.com'

    def __init__(self, player):
        self.access_token = None
        self.stop = False
        self.player = player

        def create_connection():
            self.connection = HTTP20Connection(host=self.ENDPOINT, secure=True, force_proto='h2', enable_push=True)
            print("[STATE:AVS] init Connection created.")


        def establish_downstream():
            header = {"Authorization": "Bearer %s" % (self.gettoken())}
            self.downstream_id = self.connection.request(method="GET", url=self.__interface("directives"), headers=header)
            stream = self.connection.get_response(self.downstream_id)
            if stream.status != 200:
                raise NameError("Bad downstream response %s" % (stream.status))
            self.downstream_boundary = self.get_boundary(stream)
            print("[STATE:AVS] init downstream established. bounday=%s" % (self.downstream_boundary))


        def synchronize():
            boundary_name = 'synchronization-term'
            header = self.__header(boundary_name)
            stream_id = self.connection.request(method="POST", url=self.__interface("events"), headers=header, body=self.__synchronize_message(boundary_name))
            res = self.connection.get_response(stream_id)
            if res.status != 204:
                raise NameError("Bad synchronize response %s" % (res.status))
            print("[STATE:AVS] init synchronize to AVS succeeded.")


        create_connection()
        establish_downstream()
        synchronize()

        th = threading.Thread(target=self.downstream_polling)
        th.start()


    def get_boundary(self, response):
        content = response.headers.pop('content-type')[0]
        print(content)
        b_start = content.find(b'boundary=')
        b_end = content[b_start:].find(b';')
        if b_end == -1:
            boundary = content[b_start+9:]
        else:
            boundary = content[b_start+9:b_start+b_end]
        print(boundary)
        return boundary


    def downstream_polling(self):
        while self.stop == False:
            try:
                response = self.connection.get_response(self.downstream_id)
                if response:
                    print(response)
                    data = response.read(decode_content=False)
                    print(data)
            except Exception as e:
                ee = "not impl"
                #print(e)
            time.sleep(0.05)
            #print("[AVS:STATE] checking downstream")


    def send(self, customer_voice):

        boundary_name = 'recognize-term'
        header = self.__header(boundary_name)

        def recognize_first_message():
            message = {
                  "header": {
                      "namespace": "SpeechRecognizer",
                      "name": "Recognize",
                      "messageId": "1",
                      "dialogRequestId": "1"
                  },
                  "payload": {
                      "profile": "NEAR_FIELD",
                      "format": "AUDIO_L16_RATE_16000_CHANNELS_1"
                  }
            }
            return message

        first_part_header = self.__message_header_first(boundary_name)
        first_part_body = self.__message_body_first([], recognize_first_message())
        second_part_header = self.__message_header_second(boundary_name)
        second_part_body = self.__message_body_second(customer_voice)

        body = first_part_header + '\n' + json.dumps(first_part_body) + '\n' + second_part_header + '\n' + second_part_body + self.__end_boundary(boundary_name)
        stream_id = self.connection.request(method="GET", url=self.__interface("events"), headers=header, body=body)
        res = self.connection.get_response(stream_id)
        if res.status != 200 and res.status != 204:
            print(res.read())
            print("[ERROR:AVS] Bad recognize response %s" % (res.status))
            self.expect_speech = False
            audio = None

        if res.status == 204:
            print("[STATE:AVS] recognize no content")
            print(res.headers)
            print(res.read())
            audio = None
        else:
            print("[STATE:AVS] recognize audio response present")
            boundary = self.get_boundary(res)
            response_data = res.read()
            ar = self.analyze_response(boundary, response_data)
            audio = ar['audio']

        self.player.play(audio)


    def analyze_response(self, boundary, data):
        def analyze(chunk):
            if chunk[0].startswith('Content-Type: application/json'):
                directive = json.loads(chunk[1])
            elif chunk[0].startswith('Content-ID'):
                directive = ""
            print("[STATE:AVS] directive")
            print(directive)
            return directive

        ret = {}
        tmp = data.split('--' + boundary)
        chunks = [p for p in tmp if p != b'--' and p != b'--\r\n' and len(p) != 0 and p != '\r\n']
        tmp1 = [x.split('\r\n\r\n') for x in chunks]
        tmp2 = [[y.replace('\r\n','') for y in x] for x in tmp1]
        directives = [analyze(x) for x in tmp2]
        audio = chunks[len(chunks)-1].split('\r\n\r\n')[1].rstrip('\r\n')
        ret['directives'] = directives
        ret['audio'] = audio
        return ret


    def close(self):
        self.stop = True
        self.connection.close()


    def gettoken(self):
        if self.access_token is None or (time.mktime(time.gmtime()) - self.token_refreshed_time) > 3570:
            payload = {"client_id": Client_ID, "client_secret": Client_Secret, "refresh_token": refresh_token, "grant_type": "refresh_token", }
            url = "https://api.amazon.com/auth/o2/token"
            r = requests.post(url, data=payload)
            resp = json.loads(r.text)
            self.access_token = resp['access_token']
            self.token_refreshed_time = time.mktime(time.gmtime())
            return resp['access_token']
        else:
            self.access_token


    def __synchronize_message(self, name):
        header = self.__message_header_first(name)
        events = {
          "header": {
            "namespace": "System",
            "name": "SynchronizeState",
            "messageId": "1"
          },
          "payload": {
          }
        }
        body = self.__message_body_first([], events)
        message = header + '\n\n' + json.dumps(body) + '\n\n' + self.__end_boundary(name)
        return message


    def __interface(self, name):
        return "/v20160207/%s" % (name)


    def __header(self, boundary):
        bearer = "Bearer %s" % (self.gettoken())
        content_type = "multipart/form-data; boundary=%s" % (boundary)
        header = {"Authorization": bearer, "content-type": content_type}
        return header


    def __message_header_first(self, name):
        message = ''
        message += self.__begin_boundary(name)
        message += 'Content-Disposition: form-data; name="metadata"\n'
        message += 'Content-Type: application/json; charset=UTF-8\n'
        return message


    def __message_body_first(self, contexts, event):
        message = {}
        message["context"] = contexts
        message["event"] = event
        return message


    def __message_header_second(self, name):
        message = ''
        message += self.__begin_boundary(name)
        message += 'Content-Disposition: form-data; name="audio"\n'
        message += 'Content-Type: application/octet-stream\n'
        return message


    def __message_body_second(self, data):
        return data


    def __begin_boundary(self, name):
        return '\n--' + name + '\n'


    def __end_boundary(self, name):
        return '\n--' + name + '--' + '\n'
