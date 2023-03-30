#! /usr/bin/env python3
import os
import time
import sys
from dotenv import load_dotenv

from flask import Flask, request
from pymessenger.bot import Bot
import logging

import database.db_test_scripts as db
from prompt.prompt_design import gen_response

# Initialize app
app = Flask(__name__)

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv('EAAKRPuiWsiQBAPVb8espYYrZAdAQtnwphoivd32RQ3j7bOfZCYc7Gia0y24cT2vxJfwqKDFXRxucfSY2gKtUN0b2ZC8papf3MYtVkZAPpb5tJ69glquDHlLvKzbVmls8rDDZBZCjvDJ3nPkZCaltW02AIBf2N94Yrnd6Iw2jj2k6LDdIw54G24p')
VERIFY_TOKEN = os.getenv('PLEASE_ACCESS')
bot = Bot(ACCESS_TOKEN)

# Add logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():

    # Get verify token to ensure requests are legitimate
    if request.method == 'GET':
        print('get')
        token_sent = request.args.get("hub.verify_token")
        return _verify_fb_token(token_sent)

    # Post request from user when a message is received
    else:

        # Get the message request
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):

                    # Cache metadata and payload
                    member_id = message['sender']['id']
                    rec_message = message['message'].get('text')
                    rec_timestamp = message['timestamp']

                    if rec_message:
                        # Determine if this is the start of a new conversation
                        conversation_start = _get_recent_conversation(member_id)

                        # Save rec in database
                        db.add_message(rec_message, member_id, rec_timestamp, 'received', conversation_start)

                        # Add user to database
                        db.add_user(member_id)

                        # Generate a response
                        response_sent_text = _get_message(rec_message, conversation_start, member_id)
                        _send_message(member_id, response_sent_text)

                    # If user sends us a GIF, photo,video, or any other non-text item
                    elif message['message'].get('attachments'):

                        _send_message(member_id, "My brain is not yet big enough to deal with attachments! You'll need to settle with messages for now", True)

    return "Message Processed"


def _get_recent_conversation(member_id):
    recent_msg_timestamp = db.most_recent_message_timestamp(member_id)
    current_time = int(time.time() * 1000)

    try:
        time_difference = current_time - int(recent_msg_timestamp)
    except TypeError:
        time_difference = 300001

    if time_difference <= 300000:
        conversation_start = 0

    else:
        conversation_start = 1

    return conversation_start


def _verify_fb_token(token_sent):

    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")

    else:
        return 'Invalid verification token'


def _get_message(rec_message, conversation_start, member_id):
    response_text = gen_response(rec_message, conversation_start, member_id)

    return response_text


def _send_message(member_id, response, attachment=False):

    if not attachment:
        sent_timestamp = int(time.time() * 1000)

        bot.send_text_message(member_id, response)

        # Save sent message in database
        db.add_message(response, member_id, sent_timestamp, 'sent', 0)

        return "success - message had attachments"

    else:
        bot.send_text_message(member_id, response)

        return "success - message had attachments"


if __name__ == "__main__":
    app.debug = True
    app.run()
