# Jar Jar reddit bot

A reddit bot that responds to movie quotes from comments in [/r/PrequelMemes](https://www.reddit.com/r/PrequelMemes). It uses [**Regular Expressions**](https://en.wikipedia.org/wiki/Regular_expression) to influence the comments to create... Memes.

After setting up your `.env` with the needed credentials,

```
pip install -r requirements.txt

# Tests
python -m unittest

# Run
python main.py
```

### Conditions
In [responses.json](responses.json) defines all of the possible comments to look for and defines arrays of possible responses to said comments. The bot will look for a key phrase using a regular expression and will pick a random response upon finding one.

The process has two threads. This is done to meet subreddit criteria of required timeouts between bot replies.
 - a `producer` thread, which reads replies, and enqueues responses.
 - a `consumer` thread, which pulls from queue at a regular cadence and sends the responses.

### Example
Here is an example regular expression:

```
(did you|have you) ever heard? the (.*) of (.*)\?$
```

To satisfy this condition, a comment will look like this:

>Did you ever hear the ... of ...?

*Note: Almost all of the regular expressions end with `$`, this denotes that the comment must **end with** the phrase. It just ensures that the bot is responding in the right context.*

## Contributing
- Check the project issues for any jobs that need help.
- Feel free to fork the project and make a pull request with some nice new features. We can never have too many comment responses.
- Submit an issue if you have an idea for a comment response and are not sure how to implement it or if you have any other issue with the bot.

## Testing
If you are submitting a pull request, please run the tests first (`npm test`) and ensure that they are all successful. If you are adding a major new feature, please write tests as well.

## License
[MIT](LICENSE)