import unittest
from sokoban_game import SokobanGame


class SokobanGameTestCase(unittest.TestCase):
    def test_load_level(self):
        s = SokobanGame()
        current_level = s.load_levels('boxban_levels.txt')
        self.assertEqual(0, current_level)
        self.assertEqual(60, len(s.levels))


if __name__ == '__main__':
    unittest.main()
