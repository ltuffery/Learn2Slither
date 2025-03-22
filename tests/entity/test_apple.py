import unittest
from engine.entity.apple import Apple, AppleType


class TestApple(unittest.TestCase):
    def test_is_green_type(self):
        apple = Apple(AppleType.GREEN)

        self.assertTrue(apple.is_green())
        self.assertFalse(apple.is_red())

    def test_is_red_type(self):
        apple = Apple(AppleType.RED)

        self.assertFalse(apple.is_green())
        self.assertTrue(apple.is_red())


if __name__ == '__main__':
    unittest.main()
