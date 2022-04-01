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
    
    def test_correctly_responds_to_hobbit_prompt(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Frodo is my favourite hobbit. So great.',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_correctly_responds_baggins(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Hey there baggins so great to see you',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_correctly_responds_to_smeagal(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'The ability to speak does not Smeagal you intelligent.',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        self.assertIsNotNone(extractReply(comment))

    def test_correctly_responds_ring(self):
        comment = CommentStub(**{
            'author': SimpleNamespace(**{ 'name': 'user123' }),
            'body': 'Lord of the rings is great.',
            'replies':
                RepliesStub(**{
                    '_replies': []
                })
        })

        print(extractReply(comment))
        self.assertIsNotNone(extractReply(comment))


if __name__ == '__main__':
    unittest.main()