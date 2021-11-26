from dotenv import load_dotenv
import os
import praw
import queue
import threading
import time

REPLY_SLEEP_TIME_SEC = 60

load_dotenv()

def login():
    return praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        username=os.getenv('REDDIT_USER'),
        password=os.getenv('REDDIT_PASS'),
        user_agent="Meesa Jar Jar Binks"
    )

def producer(reddit, queue):
    for comment in reddit.subreddit(os.getenv('SUBREDDIT')).stream.comments(skip_existing=True):
        print(f"({comment.permalink} by {comment.author}): {comment.body}")

def consumer(reddit, queue):
    while True:
        print('loop 2')
        time.sleep(REPLY_SLEEP_TIME_SEC)

reddit=login()
q = queue.Queue()

listenThread = threading.Thread(target=producer, args=(reddit,q,))
listenThread.daemon = True
listenThread.start()

replyThread = threading.Thread(target=consumer, args=(reddit, q,))
replyThread.daemon = True
replyThread.start()

# Using daemons and a while loop to allow ctrl-c termination.
while True:
    time.sleep(1)