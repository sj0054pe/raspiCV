# coding: utf-8

import urllib2
import json

def lambda_handler(event, context):

    for ev in event["events"]:

        # メッセージ解析
        message = ev["message"]["text"]
        if message in u"電源入れて":
            t = u"入れました"
        elif message in u"電源切って":
            t = u"切りました"
        else:
            t = u"ごめんなさい。わかりません。"

        # リプライ用APIを叩く
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer {Channel Access Token}"
        }
        body = {
            "replyToken": ev["replyToken"],
            "messages": [
                {
                    "type": "text",
                    "text": t
                }
            ]
        }
        req = urllib2.Request(url, data=json.dumps(body), headers=headers)
        resp = urllib2.urlopen(req)
        print resp.read()
