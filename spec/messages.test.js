require('dotenv').config();
const messages = require('../messages');

describe('messages and responses', () => {

    it('should not reply twice', () => {
        let comment = {
            body: `it's over jar jar, i have the high ground!`,
            author: {
                name: 'user_123456789'
            },
            replies: [{
                body: 'My reply!',
                author: {
                    name: process.env.REDDIT_USER
                }
            }]
        };

        let message = messages.extractReply(comment);
        expect(message).toBeNull();
    })

    it('should return null if no matches', () => {
        let comment = {
            body: 'This is not a quote from the prequels.',
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);
        expect(message).toBeNull();
    });

    it('should return a message if there are matches', () => {
        let comment = {
            body: `it's over jar jar, i have the high ground!`,
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
    });

    it('should not care about case sensitivity', () => {
        let comment = {
            body: `IT'S OVER JAR JAR, I HAVE THE HIGH GROUND!`,
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
    });

    it('should contain the username if the match contains a $username keyword', () => {
        let comment = {
            body: 'Hi, Jar Jar.',
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
        expect(message).toContain(comment.author.name);
    });

    it('should reply to keyword of Jar Jar', () => {
        let comment = {
            body: 'Jar Jar',
            author: {
                name: 'user_12334545'
            }
        };
        let prevCommentIds = [comment.parent_id];

        let message = messages.extractReply(comment, prevCommentIds);
        expect(message).not.toBeNull();
    });

    it('should not reply to itself', () => {
        let comment = {
            body: `It's over Jar Jar, I have the high ground!`,
            author: {
                name: process.env.REDDIT_USER
            }
        };

        let message = messages.extractReply(comment);

        expect(message).toBeNull();
    });
});