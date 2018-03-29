# Slackbot: Mr Wise Guy

I built this slackbot to help increase engagement between NY+Acumen volunteers as we raise funds to help fight poverty.

For more on Acumen visit https://acumen.org/. 

To learn about getting involved or supporting the New York chapter, see http://nyplusacumen.org/.


### Features
* Based on Slack [Real Time Messaging API](https://api.slack.com/rtm)
* Integration with [Sheets API](https://developers.google.com/sheets/api/guides/concepts) using [gspread](https://github.com/burnash/gspread)
* Real-time quering and storage on postgresql
* Conversational (responds to "hello", "thank you" etc)


### Installation

This is currently only available in private beta to NY+Acumen.


### Usage

To talk to Mr Wise Guy, ensure that you are in the NY+Acumen workspace and in a channel
in which @Mr Wise Guy is installed. You can ask him two types of questions:

* WHOIS: To learn about a volunteer's life (job, company etc)
e.g. `@mr wise guy whois ray rehman`

* GETME: To get a volunteer's contact information (phone number, email)
e.g. `@mr wise guy getme ray rehman`


### Version history

* v1 (3/29/2018): Responds to requests for bio and contact info


### Resources

[How to Build Your First Slack Bot with Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)


Last updated: 3/29/2018