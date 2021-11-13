require('dotenv').config();
const messages = require('../messages');

describe('messages and responses', () => {

    it('should not reply twice', () => {
        let comment = {
            body: `it's over anakin, i have the high ground!`,
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
            body: `it's over anakin, i have the high ground!`,
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
    });

    it('should not care about case sensitivity', () => {
        let comment = {
            body: `IT'S OVER ANAKIN, I HAVE THE HIGH GROUND!`,
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
    });

    it('should contain the username if the match contains a $username keyword', () => {
        let comment = {
            body: 'All I want is your love.',
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
        expect(message).toContain(comment.author.name);
    });

    it('should reply to Obiwan-bot', () => {
        let comment = {
            body: 'Test test',
            author: {
                name: 'Obiwan-Kenobi-Bot'
            }
        };
        let prevCommentIds = [comment.parent_id];

        let message = messages.extractReply(comment, prevCommentIds);
        expect(message).not.toBeNull();
    });

    it('should reply to Sheev-bot', () => {
        let comment = {
            body: 'Test test',
            author: {
                name: 'sheev-bot'
            }
        };
        let prevCommentIds = [comment.parent_id];

        let message = messages.extractReply(comment, prevCommentIds);
        expect(message).not.toBeNull();
    });

    it('should not reply to an ignored user', () => {
        let comment = {
            body: 'Anakin',
            author: {
                name: 'example-user'
            }
        };
        let prevCommentIds = [comment.parent_id];

        let message = messages.extractReply(comment, prevCommentIds);
        expect(message).toBeNull();
    });

    it('should reply to keyword of Anakin', () => {
        let comment = {
            body: 'Anakin',
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
            body: `It's over Anakin, I have the high ground!`,
            author: {
                name: process.env.REDDIT_USER
            }
        };

        let message = messages.extractReply(comment);

        expect(message).toBeNull();
    });

    it('should replace group match keywords with text contained in the comment', () => {
        let comment = {
            body: `become the very thing you swore to destroy`,
            author: {
                name: 'user_123456789'
            }
        };

        let message = messages.extractReply(comment);

        expect(message).not.toBeNull();
        expect(message).toContain('lecture');
    });
});