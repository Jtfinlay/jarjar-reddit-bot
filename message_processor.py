from colored import stylize, fg
from dotenv import load_dotenv
import json
import os
import re
from types import SimpleNamespace


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
        print(stylize(f"\n'{author}' has been ignored by '{comment.author.name}'.", fg('cyan')))
        return author == os.getenv('REDDIT_USER')
    return False

#
# Check whether our bot has already replied to the comment.
#
def hasBotReplied(comment):
    # First, check redis on whether we've replied or not.
    # TODO

    # Otherwise, look through the replies to find our bot's name.
    for comment in comment.replies.list():
        if comment.author.name == os.getenv('REDDIT_USER'):
            return True

    return False


#
# Look for a reply to this comment
#
def extractReply(comment):
    if comment.author.name == os.getenv('REDDIT_USER'):
        return
    
    if hasBotReplied(comment):
        return
    
