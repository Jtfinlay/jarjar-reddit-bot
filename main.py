import os
import praw
import redis
import threading
import time

REPLY_SLEEP_TIME_SEC = 60

def login():
    return praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        username=os.getenv('REDDIT_USER'),
        password=os.getenv('REDDIT_PASS'),
        user_agent="Meesa Jar Jar Binks"
    )

def reader():
    reddit = login()
    for comment in reddit.subreddit(os.getenv('SUBREDDIT')).stream.comments(skip_existing=True):
        print(f"({comment.permalink} by {comment.author}): {comment.body}")

def responder():
    reddit = login();
    while True:
        print('loop 2')
        time.sleep(REPLY_SLEEP_TIME_SEC)

listenThread = threading.Thread(target=reader)
listenThread.start()

replyThread = threading.Thread(target=responder)
replyThread.start()