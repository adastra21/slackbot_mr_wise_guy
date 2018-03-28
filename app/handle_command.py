import os
import re

import credentials as creds
import questions as ques
import converse as convo

from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(creds.SLACK_BOT_TOKEN)

# constants
GREETING = "hello"
HELP = "help"
WHO = "whois "
GET = "getme "

# handle commands
def handle_command(command, channel):

    # handle greeting
    if command.startswith(GREETING):
        response = "Hi, I'm Mr Wise Guy. You probably saw me in Goodfellas or Mean Streets or the street. I consider myself semi-retired so am doing this for entertainment. AMA!"

    # handle help
    elif command.startswith(HELP):
        response = ">*#TheWisecrack*: a guide to getting wiser with me\n>- Always address me with `@mr_wise_guy`\n>- *GETME*: If you want me to give you contact information for someone, use 'getme' while talking to me e.g. `@mr_wise_guy getme number for Ray Rehman`\n>- *WHOIS*: If you want me to lookup someone, use 'whois' while talking to me e.g. `@mr_wise_guy whois brian yoon?`\n>- If you are bored and want my excellent company, just call my name `@mr_wise_guy` and type whatever your heart desires (PG only please)"

    # handle questions
    elif command.startswith(WHO):
        response = ques.handle_question(command)

    elif command.startswith(GET):
        response = ques.handle_question(command)

    # handles small talk
    else:
        response = convo.handle_convo(command)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)