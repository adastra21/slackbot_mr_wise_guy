import os
import time

import questions as ques
import handle_command as handler

from slackclient import SlackClient

# env vars
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
BOT_ID = os.environ["BOT_ID"]

# constants
AT_BOT = "<@" + BOT_ID + ">"
# delay between reading from firehose
READ_WEBSOCKET_DELAY = 0.2

# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

# only run this if the program is run directly
if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("Mr Wise Guy is connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command = handler.handle_command
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack Token or Bot ID?")