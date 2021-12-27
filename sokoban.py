from sokoban_game import *
# noinspection PyUnresolvedReferences
from scene import SpriteNode, Scene, ui, ShapeNode, LabelNode, run
# noinspection PyUnresolvedReferences
from sound import play_effect

border = 32
cell_size = 36
colors = {
    CELLTYPE_PLAYER: '#A787FF',
    CELLTYPE_PLAYER_ON_STORAGE: '#9E77FF',
    CELLTYPE_BOX: '#FFC97E',
    CELLTYPE_BOX_ON_STORAGE: '#96FF7F',
    CELLTYPE_STORAGE: '#9CE5FF',
    CELLTYPE_WALL: '#FF93D1',
}
button_font = ('Avenir Next', 48)
title_font = ('Avenir Next', 20)


class ButtonNode:
    def __init__(self, text, pos, deltas=None, action=None):
        self.node = LabelNode(text, position=pos, font=button_font, anchor_point=(0.5, 0.5))
        self.deltas = deltas
        self.action = action


class SokobanGameScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)
        self.box_cells = []
        self.buttons = []
        self.update_required = False
        self.background_color = '#FFFFBE'
        self.num_moves = 0
        self.title_node = LabelNode()
        self.sokoban_game = SokobanGame()

    def refresh_level(self):
        """Refresh the current level"""
        # first delete all the current cells
        for box_cell in self.box_cells:
            box_cell.remove_from_parent()
        self.box_cells = []
        self.title_node.remove_from_parent()
        title = 'LEVEL: {} MOVES: {}'.format(self.sokoban_game.current_level+1, self.num_moves)
        self.title_node = LabelNode(position=(120, self.size.h-20), text=title, font=title_font, color='black')
        self.add_child(self.title_node)
        border_y = 50
        for y, row in enumerate(self.sokoban_game.level):
            for x, cell in enumerate(row):
                if cell != CELLTYPE_EMPTY:
                    pos = (border + x * cell_size, self.size.h - border_y - y * cell_size)
                    path = ui.Path.rect(0, 0, cell_size, cell_size)
                    box_cell = ShapeNode(position=pos, path=path, fill_color=colors[cell])
                    self.add_child(box_cell)
                    self.box_cells.append(box_cell)
                    cell_label = LabelNode(position=pos, text=cell, anchor_point=(0.5, 0.5))
                    self.add_child(cell_label)
                    self.box_cells.append(cell_label)

    def define_buttons(self):
        """Define the movement buttons"""
        left_btn = ButtonNode(pos=(32, 32), text='⬅️', deltas=(-1, 0))
        self.add_child(left_btn.node)
        right_btn = ButtonNode(pos=(206, 32), text='➡️', deltas=(1, 0))
        self.add_child(right_btn.node)
        up_btn = ButtonNode(pos=(90, 32), text='⬆️', deltas=(0, -1))
        self.add_child(up_btn.node)
        down_btn = ButtonNode(pos=(148, 32), text='⬇️', deltas=(0, 1))
        self.add_child(down_btn.node)
        refresh_btn = ButtonNode(pos=(264, 32), text='🔄', action=self.reload_and_refresh)
        self.add_child(refresh_btn.node)
        previous_level_btn = ButtonNode(pos=(322, 32), text='⏪', action=self.previous_level_and_refresh)
        self.add_child(previous_level_btn.node)
        next_level_btn = ButtonNode(pos=(380, 32), text='⏩', action=self.next_level_and_refresh)
        self.add_child(next_level_btn.node)
        self.buttons = [left_btn, right_btn, up_btn, down_btn, refresh_btn, previous_level_btn, next_level_btn]

    def setup(self):
        """Setup the scene.

        This gets called once, just before the scene is presented to the screen.
        """
        self.box_cells = []
        self.title_node = LabelNode()
        self.sokoban_game.load_levels('boxban_levels.txt')
        self.sokoban_game.load_level()
        self.refresh_level()
        self.define_buttons()

    def next_level_and_refresh(self):
        """Move to the next level and refresh the scene"""
        self.sokoban_game.move_next_level()
        self.sokoban_game.load_level()
        self.num_moves = 0
        self.refresh_level()
        
    def previous_level_and_refresh(self):
        """Move to the previous level and refresh the scene"""
        self.sokoban_game.move_previous_level()
        self.sokoban_game.load_level()
        self.num_moves = 0
        self.refresh_level()
        
    def reload_and_refresh(self):
        """Reload the current level and refresh the scene"""
        self.sokoban_game.load_level()
        self.num_moves = 0
        self.refresh_level()

    def touch_began(self, touch):
        """Called at the start of a touch event"""
        touch_loc = self.point_from_scene(touch.location)
        for btn in self.buttons:
            if touch_loc in btn.node.frame:
                play_effect('8ve:8ve-tap-resonant')

    def touch_ended(self, touch):
        """Called at the end of a touch event"""
        touch_loc = self.point_from_scene(touch.location)
        for btn in self.buttons:
            if touch_loc in btn.node.frame:
                if btn.deltas is None:
                    btn.action()
                    self.update_required = True
                else:
                    dx, dy = btn.deltas
                    changed, completed = self.sokoban_game.do_move(dx, dy)
                    if completed:
                        self.sokoban_game.load_level()
                        self.num_moves = 0
                    elif changed:
                        self.num_moves += 1
                    if changed or completed:
                        self.refresh_level()


run(SokobanGameScene())
