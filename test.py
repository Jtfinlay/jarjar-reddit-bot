from dotenv import load_dotenv
from types import SimpleNamespace
import unittest

from message_processor import checkForCommand

load_dotenv()

class CommentStub(SimpleNamespace):
    def parent(self):
        return CommentStub(**self._parent)

class TestMessageProcessor(unittest.TestCase):
    def test_correctly_find_ignore_command(self):
        comment = CommentStub(**{
            'author': 'user123',
            'body': '!ignore',
            '_parent': {
                'author': 'jarjar_bot'
            }
        })

        self.assertTrue(checkForCommand(comment))

    def test_dismiss_ignore_command_for_other_bot(self):
        comment = CommentStub(**{
            'author': 'user123',
            'body': '!ignore',
            '_parent': {
                'author': 'a_different_bot'
            }
        })

        self.assertFalse(checkForCommand(comment))

    def test_dismiss_non_ignore_command(self):
        comment = CommentStub(**{
            'author': 'user123',
            'body': 'Good bot',
            '_parent': {
                'author': 'jarjar_bot'
            }
        })

        self.assertFalse(checkForCommand(comment))


if __name__ == '__main__':
    unittest.main()