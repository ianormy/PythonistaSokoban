import copy

CELLTYPE_PLAYER = '@'
CELLTYPE_PLAYER_ON_STORAGE = '+'
CELLTYPE_BOX = '$'
CELLTYPE_BOX_ON_STORAGE = '*'
CELLTYPE_STORAGE = '.'
CELLTYPE_WALL = '#'
CELLTYPE_EMPTY = ' '


class SokobanGame:
    def __init__(self):
        """initialise the class"""
        self.levels = []
        self.current_level = -1
        self.level = []

    def load_levels(self, file_path):
        """load levels from a deepmind boxban format file.

        :param file_path: path to the file containing the levels
        :return: 0 if levels loaded successfully, otherwise -1
        """
        self.levels = []  # cleardown the current levels
        self.level = []
        self.current_level = -1
        level_num = -1  # not currently used
        with open(file_path, 'r') as f:
            level = []
            for line in f:
                if len(line) > 0:
                    if line[0] == ';':
                        #  start of a new level
                        level_num = int(line[1:])
                        if len(level) > 0:
                            self.levels.append(level)
                        level = []
                    else:
                        #  add the line to this level
                        level.append(list(line.rstrip()))
        if len(self.levels) > 0:
            self.current_level = 0
        return self.current_level

    def load_level(self):
        """Load the current level

        If the current level has changed, it will reset it back to it's beginning state.
        """
        self.level = copy.deepcopy(self.levels[self.current_level])

    def move_next_level(self):
        """Move to the next level.

        If the user moves past the end of the levels, go back to the beginning.
        """
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.current_level = 0

    def move_previous_level(self):
        """Move to the previous level.

        If the user moves before the beginning of the levels, go back to the end.
        """
        self.current_level -= 1
        if self.current_level < 0:
            self.current_level = len(self.levels) - 1

    def do_move(self, dx: int, dy: int):
        """Do a move if possible.

        :param dx: change in x
        :param dy: change in y
        :returns changed, complete: changed is True if a change has been made.
                                    complete is True if the level is completed.
        """
        player_x = -1
        player_y = -1
        for test_y, row in enumerate(self.level):
            for test_x, cell in enumerate(row):
                if cell == CELLTYPE_PLAYER or cell == CELLTYPE_PLAYER_ON_STORAGE:
                    player_x = test_x
                    player_y = test_y
        current = self.level[player_y][player_x]
        adjacent = self.level[player_y + dy][player_x + dx]
        beyond = ''
        if (
                0 <= player_y + dy + dy < len(self.level)
                and 0 <= player_x + dx + dx < len(self.level[player_y + dy + dy])
        ):
            beyond = self.level[player_y + dy + dy][player_x + dx + dx]

        next_adjacent = {
            CELLTYPE_EMPTY: CELLTYPE_PLAYER,
            CELLTYPE_STORAGE: CELLTYPE_PLAYER_ON_STORAGE,
        }
        next_current = {
            CELLTYPE_PLAYER: CELLTYPE_EMPTY,
            CELLTYPE_PLAYER_ON_STORAGE: CELLTYPE_STORAGE,
        }
        next_beyond = {
            CELLTYPE_EMPTY: CELLTYPE_BOX,
            CELLTYPE_STORAGE: CELLTYPE_BOX_ON_STORAGE,
        }
        next_adjacent_push = {
            CELLTYPE_BOX: CELLTYPE_PLAYER,
            CELLTYPE_BOX_ON_STORAGE: CELLTYPE_PLAYER_ON_STORAGE,
        }

        changed = False
        if adjacent in next_adjacent:
            self.level[player_y][player_x] = next_current[current]
            self.level[player_y + dy][player_x + dx] = next_adjacent[adjacent]
            changed = True

        elif beyond in next_beyond and adjacent in next_adjacent_push:
            self.level[player_y][player_x] = next_current[current]
            self.level[player_y + dy][player_x + dx] = next_adjacent_push[adjacent]
            self.level[player_y + dy + dy][player_x + dx + dx] = next_beyond[beyond]
            changed = True

        complete = True

        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell == CELLTYPE_BOX:
                    complete = False
        if complete:
            self.move_next_level()

        return changed, complete
