const responses = require('./responses.json');

const STRIP_FROM_MESSAGES = [" ^comment ^!ignore ^to ^mute ^me"];
const IGNORE_PATTERN = "^!ignore$";
const KNOWN_BOTS = ["Obiwan-Kenobi-Bot", "sheev-bot", "Anakin_Skywalker_Bot"];
const groupMatchRegex = /\$(\d*)/gi;

const BOT_RESPONSE_CHANCE = 0.1;

function extractMessage(comment, resp) {
    let regex = new RegExp(resp.pattern, 'gi');
    let text = comment.body;
    STRIP_FROM_MESSAGES.forEach(msg => text = text.replace(msg, ""));
    text = text.trim();

    let matches = regex.exec(text);
    let message = null;

    if (matches && matches.length > 0) {
        //if we get to here then we can extract a response. 
        //Pick a random response to send back.
        if (resp.responses) {
            message = getRandomArrayItem(resp.responses);
        } else {
            message = resp.response;
        }

        //Check if the message contains a group match keyword, i.e $0, $1 ect.
        //A $ symbol followed by a number indicates the matching group to add to the text.
        let groupMatch = groupMatchRegex.exec(message);

        //Go through each match and extract the group from the original message.
        while (groupMatch != null) {
            let identifier = groupMatch[0];
            let index = parseInt(groupMatch[1]);

            if (Number.isNaN(index))
                break;

            let origGroup = matches[index + 1].trim(); //returns captured group (...) in regex

            message = message.replace(identifier, origGroup);

            groupMatch = groupMatchRegex.exec(message);
        }
    }

    //Check if the message contains any keywords.
    if (message && message.indexOf('$username') > -1) {
        if (KNOWN_BOTS.includes('$username')) {
            message = message.replace('$username', 'Your Highness');
        } else {
            message = message.replace('$username', comment.author.name);
        }
    }

    return message;
}

function getRandomArrayItem(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function findAndExtractMessage(comment, arr) {
    for (let i = 0; i < arr.length; i++) {
        let resp = arr[i];
        let message = extractMessage(comment, resp);

        if (message) {
            // If a bot, only reply once in a while
            if (KNOWN_BOTS.includes(comment.author) && Math.random() < 1 - BOT_RESPONSE_CHANCE) {
                continue;
            }

            // Calculate chance of reply.
            let chance = resp.chance || 1.0;
            if (Math.random() < 1- chance) {
                continue;
            }

            return message;
        }
    }

    return null;
}

function hasReplied(comments) {
    return comments && comments.findIndex(c => c.author.name === process.env.REDDIT_USER) >= 0;
}

module.exports = {

    async checkIfIgnoreCommand(comment, reddit) {
        let regex = new RegExp(IGNORE_PATTERN, 'gi');
        let matches = regex.exec(comment.body);
        if (matches && matches.length > 0) {
            const parentComment = await reddit.getComment(comment.parent_id).fetch();
            const parentAuthor = parentComment.author.name;
            console.log(`Ignore command found for '${comment.author.name}' in response to '${parentAuthor}'`);
            return { ignored: parentAuthor === process.env.REDDIT_USER, comment: comment };
        }

        return Promise.resolve({ ignored: false, comment: comment });
    },

    extractReply(comment) {
        //make sure we're not replying to ourselves.
        if (comment.author.name === process.env.REDDIT_USER) {
            return null;
        }

        if (hasReplied(comment.replies)) {
            console.log('Not answering twice!');
            return null;
        }

        return findAndExtractMessage(comment, responses.messages);
    }

};
