from dotenv import load_dotenv
from types import SimpleNamespace
import unittest

from message_processor import checkForIgnoreCommand, hasBotReplied, extractReply

load_dotenv()

class CommentStub(SimpleNamespace):
    def parent(self):
        return CommentStub(**self._parent)

class RepliesStub(SimpleNamespace):
    def list(self):
        return self._replies

class TestMessageProcessor(unittest.TestCase):
    def test_correctly_find_ignore_command(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': '!ignore',
            '_parent': {
                'author': SimpleNamespace(**{ 'name': 'jarjar_bot' })
            }
        })

        self.assertTrue(checkForIgnoreCommand(comment))

    def test_dismiss_ignore_command_for_other_bot(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': '!ignore',
            '_parent': {
                'author': SimpleNamespace(**{ 'name': 'a_different_bot' })
            }
        })

        self.assertFalse(checkForIgnoreCommand(comment))

    def test_dismiss_non_ignore_command(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Good bot',
            '_parent': {
                'author': SimpleNamespace(**{ 'name': 'jarjar_bot' })
            }
        })

        self.assertFalse(checkForIgnoreCommand(comment))

    def test_correctly_find_when_already_replied(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'hi hi',
            'replies':
                RepliesStub(**{
                    '_replies': [CommentStub(**{
                        'author': SimpleNamespace(**{'name': 'jarjar_bot'}),
                        'body': 'Meesa your humble servant!'
                    })]
                })
        })

        self.assertTrue(hasBotReplied(comment))

    def test_correctly_find_when_not_replied(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'hi hi',
            'replies':
                RepliesStub(**{
                    '_replies': [CommentStub(**{
                        'author': SimpleNamespace(**{'name': 'other_bot'}),
                        'body': 'Meesa your humble servant!'
                    })]
                })
        })

        self.assertFalse(hasBotReplied(comment))

    def test_replies_to_jar_jar(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Jar Jar',
            'replies':
                RepliesStub(**{
                    '_replies': [CommentStub(**{
                        'author': SimpleNamespace(**{'name': 'user123'}),
                        'body': 'Meesa your humble servant!'
                    })]
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_replies_to_jar_jar_without_case_sensitivity(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'JAR JAR',
            'replies':
                RepliesStub(**{
                    '_replies': [CommentStub(**{
                        'author': SimpleNamespace(**{'name': 'user123'}),
                        'body': 'Meesa your humble servant!'
                    })]
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_replies_to_jarjar(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'jarjar',
            'replies':
                RepliesStub(**{
                    '_replies': [CommentStub(**{
                        'author': SimpleNamespace(**{'name': 'user123'}),
                        'body': 'Meesa your humble servant!'
                    })]
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_does_not_reply_to_random_comment(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Hello world',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        self.assertIsNone(extractReply(comment))

    def test_should_contain_username_if_match_contains_the_keyword(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Hi, Jar Jar.',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        reply = extractReply(comment)
        self.assertIsNotNone(reply)
        self.assertTrue('u/user123' in reply)

    def test_should_not_reply_to_self(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'jarjar_bot' }),
            'body': 'Meesa Jar Jar.',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        self.assertIsNone(extractReply(comment))


if __name__ == '__main__':
    unittest.main()