from colored import stylize, fg
from dotenv import load_dotenv
import os
import praw
import queue
import threading
import time

from message_processor import checkForIgnoreCommand, hasBotReplied, extractReply

REPLY_SLEEP_TIME_SEC = 60
MAX_QUEUE_SIZE = 100

load_dotenv()

class ReplyItem:
    def __init__(self, commentId, reply):
        self.commentId = commentId
        self.reply = reply

def login():
    return praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        username=os.getenv('REDDIT_USER'),
        password=os.getenv('REDDIT_PASS'),
        user_agent="Meesa Jar Jar Binks"
    )

def producer(queue):
    reddit=login()
    for comment in reddit.subreddit(os.getenv('SUBREDDIT')).stream.comments(skip_existing=True):

        ## If Queue is pull (we are producing faster than we consume), drop items from the queue
        # TODO - Might be smarter to use Redis to have items expire than this max queue length, but
        # at least this might prevent out-of-memory exceptions.
        while queue.full():
            item = queue.get()
            print(stylize(f"Queue is too long! Dropping old entry: {item.commentId}!", fg('red')))

        print(stylize(f"({comment.permalink} by {comment.author}): {comment.body}", fg('dark_gray')))
        reply = extractReply(comment)
        if reply:
            print(stylize(f"Pushed item ${comment.id}", fg('yellow')))
            queue.put(ReplyItem(comment.id, reply), False)

def consumer(queue):
    reddit=login()
    while True:
        item = queue.get()
        print(stylize(f"Pulled item ${item.commentId}", fg('sky_blue_2')))

        # Get the comment and double-check we haven't replied to it.
        comment = reddit.comment(id=item.commentId)
        if hasBotReplied(comment):
            print(stylize(f"Bot has already replied to: ${item.commentId}", fg('red')))
            continue

        comment.reply(item.reply)

        print(stylize(f"Replied (${item.commentId}) with: ${item.reply}", fg('green')))

        time.sleep(REPLY_SLEEP_TIME_SEC)

q = queue.Queue(MAX_QUEUE_SIZE)

listenThread = threading.Thread(target=producer, args=(q,))
listenThread.daemon = True
listenThread.start()

replyThread = threading.Thread(target=consumer, args=(q,))
replyThread.daemon = True
replyThread.start()

# Using daemons and a while loop to allow ctrl-c termination.
while True:
    time.sleep(1)