require('dotenv').config();

const fs = require('fs');
const Snoowrap = require('snoowrap');
const Snoostorm = require('snoostorm');
const messages = require('./messages');

const IGNORE_FILE = 'ignore-list.txt';

const reddit = new Snoowrap({
    userAgent: process.env.REDDIT_USER_AGENT,
    clientId: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRET,
    username: process.env.REDDIT_USER,
    password: process.env.REDDIT_PASS
});

const client = new Snoostorm(reddit);

const stream = client.CommentStream({
    subreddit: process.env.SUBREDDIT,
    results: 100
});

const ignoredUsers = fs.readFileSync(IGNORE_FILE).toString().split('\n');
ignoredUsers.forEach(u => console.log(u));

stream.on('comment', comment => {
    console.log('process comment');

    if (ignoredUsers.includes(comment.author.name)) {
        return null;
    }

    if (messages.checkIfIgnoreCommand(comment, reddit)) {
        ignoredUsers.push(comment.author.name);
        fs.appendFile(IGNORE_FILE, comment.author.name, function (err) { if (err) console.error("Could not write the ignore!")});
    }

    const reply = messages.extractReply(comment);

    if (!reply) {
        return;
    }

    console.log(`Found message: ${comment.body}`);
    console.log(`Responding with: ${reply}`);

    // comment.reply(reply)
    //     .then(resp => {
    //         console.log(`Responded to message.`);

    //         //Add the comment id to the array, we'll use it to
    //         //check if a user has replied to one of our comments.
    //         commentIds.push('t1_' + resp.id);
    //     })
    //     .catch(err => {
    //         console.error(err);
    //     });
});