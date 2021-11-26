from colored import stylize, fg
from dotenv import load_dotenv
import json
import os
import random
import re
from types import SimpleNamespace

BOT_RESPONSE_CHANCE = 0.1
IGNORE_PATTERN = "^!ignore$"
KNOWN_BOTS = ["Obiwan-Kenobi-Bot", "sheev-bot", "Anakin_Skywalker_Bot"]

load_dotenv()

# load responses file into a simple object
with open("responses.json") as fh:
    string = fh.read()
responses = json.loads(string, object_hook=lambda d: SimpleNamespace(**d))

#
# Check if the comment is the '!ignore' command.
#
def checkForIgnoreCommand(comment):
    if re.search(IGNORE_PATTERN, comment.body, re.IGNORECASE):
        author = comment.parent().author.name
        print(stylize(
            f"\n'{author}' has been ignored by '{comment.author.name}'.", fg('cyan')))
        return author == os.getenv('REDDIT_USER')
    return False

#
# Check whether our bot has already replied to the comment.
#
def hasBotReplied(comment):
    # Look through the replies to find our bot's name.
    for comment in comment.replies.list():
        if comment.author.name == os.getenv('REDDIT_USER'):
            return True

    return False


def matchReply(comment, message):
    text = comment.body.strip()

    if re.search(message.pattern, text, re.IGNORECASE):
        reply = random.choice(message.responses)

        # TODO - Check for group matches where we could include parts of the message in the response.

        if comment.author.name in KNOWN_BOTS:
            reply = reply.replace('$username', 'Your Highness')
        reply = reply.replace('$username', comment.author.name)

        return reply


def findReply(comment):
    for message in responses.messages:
        reply = matchReply(comment, message)

        if reply:
            if comment.author.name in KNOWN_BOTS and random.randint(0, 1) < 1 - BOT_RESPONSE_CHANCE:
                continue

            if random.randint(0, 1) < 1 - message.chance:
                continue

            return reply

#
# Look for a reply to this comment
#
def extractReply(comment):
    if comment.author.name == os.getenv('REDDIT_USER'):
        return

    if hasBotReplied(comment):
        return

    return findReply(comment)
