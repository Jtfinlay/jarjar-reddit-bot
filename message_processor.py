from colored import stylize, fg
from dotenv import load_dotenv
import os
import re

load_dotenv()

IGNORE_PATTERN = "^!ignore$"

def checkForCommand(comment):
    if re.search(IGNORE_PATTERN, comment.body, re.IGNORECASE):
        author = comment.parent().author
        print(stylize(f"\n'{author}' has been ignored by '{comment.author}'.", fg('cyan')))
        return author == os.getenv('REDDIT_USER')
    return False