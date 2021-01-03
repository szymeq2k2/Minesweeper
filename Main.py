import arcade
import Grid.Field as F
from random import randint

# window data
SCREEN_WIDTH = 425
SCREEN_HEIGHT = 425
SCREEN_TITLE = "Minesweeper"

# arcade game class
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.field_src = "Grid/Field.png"
        self.field_empty_src = "Grid/Field_Empty.png"
        self.bomb_src = "Grid/Bomb.png"
        self.flag_src = "Grid/Flag.png"
        self.field_1_src = "Grid/Field_1.png"
        self.field_2_src = "Grid/Field_2.png"
        self.field_3_src = "Grid/Field_3.png"
        self.field_4_src = "Grid/Field_4.png"
        self.field_5_src = "Grid/Field_5.png"
        self.field_6_src = "Grid/Field_6.png"
        self.field_7_src = "Grid/Field_7.png"
        self.field_8_src = "Grid/Field_8.png"
        self.field_list = None
        self.bomb_list = None
        self.field_list_sprite = arcade.SpriteList()
        self.bomb_list_sprite = arcade.SpriteList()
        self.bombs_count = None
        self.fields_count = None
        self.end = None
        self.empty_list = None

    # setup used for starting and restarting game
    def setup(self):
        self.end = False
        self.end_text = ""
        self.empty_list = list()
        self.field_list = list()
        self.bomb_list = list()
        self.flags = 0
        self.bombs_count = 35
        self.fields_count = 195
        i = 0
        while(i<self.bombs_count):
            temp = randint(0, 194)
            if self.bomb_list.count(temp) == False:
                self.bomb_list.append(temp)
                i += 1
        i = 0
        for x in range(50, 400, 25):
            for y in range(25, 375, 25):
                field = arcade.Sprite(self.field_src, 1)
                field.center_x = x
                field.center_y = y
                if self.bomb_list.count(i):
                    self.field_list.append(F.field(x, y, "bomb"))
                else:
                    self.field_list.append(F.field(x, y, "field"))
                i += 1
                self.field_list_sprite.append(field)

    # method that restarts game after pressing R
    def on_key_release(self, key, modifiers):
        if key == arcade.key.R:
            self.setup()

    # uncovers field or flags it
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.end == False:
            if _button == arcade.MOUSE_BUTTON_LEFT:
                for field in self.field_list:
                    if field.x - 12 <= _x and field.y - 12 <= _y:
                        if field.x + 12 >= _x and field.y + 12 >= _y:
                            if field.flagged == False:
                                if field.fieldType == "bomb":
                                    self.end = True
                                    self.end_text = "Game Over"
                                    self.uncovered_bombs()
                                else:
                                    field.fieldType = "uncovered"
                                    if self.setNumber(field) != 0:
                                        self.uncover(field)
                                    else:
                                        self.uncover_adjanced(field)
                                        for y in self.empty_list:
                                            for x in self.field_list:
                                                if y.x == x.x  - 25:
                                                    if y.y == x.y:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y - 25:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y + 25:
                                                        x.fieldType = "uncovered"
                                                elif y.x == x.x + 25:
                                                    if y.y == x.y:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y - 25:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y + 25:
                                                        x.fieldType = "uncovered"
                                                elif y.x == x.x:
                                                    if y.y == x.y:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y - 25:
                                                        x.fieldType = "uncovered"
                                                    elif y.y == x.y + 25:
                                                        x.fieldType = "uncovered"
                                                if y.uncovered == False:
                                                    self.uncover_adjanced(y)
                                        self.uncover(field)
                                    self.victory()
            elif _button == arcade.MOUSE_BUTTON_RIGHT:
                if self.flags < self.bombs_count:
                    for field in self.field_list:
                        if field.x - 12 <= _x and field.y - 12 <= _y:
                            if field.x + 12 >= _x and field.y + 12 >= _y:
                                if field.fieldType != "uncovered":
                                    if field.flagged == True:
                                        self.flags -= 1
                                        field.flagged = False
                                    else:
                                        self.flags += 1
                                        field.flagged = True
                                    self.uncover(field)

    # draws sprites
    def on_draw(self):
        arcade.start_render()
        self.field_list_sprite.draw()
        flag_text = f"Flags: {self.flags} / {self.bombs_count}"
        arcade.draw_text(flag_text, 10, 400, arcade.csscolor.BLACK, 18)
        arcade.draw_text(self.end_text, 165, 400, arcade.csscolor.BLACK, 18)

    #checks if all field without bomb are uncovered
    def victory(self):
        i = 0
        for field in self.field_list:
            if field.fieldType == "uncovered":
                i += 1
        i -= 1
        if i == self.fields_count - self.bombs_count:
            self.end_text = "Victory!"
            self.end = True

    # uncovers adjanced fields
    def uncover_adjanced(self, field):
        field.uncovered = True
        for x in self.field_list:
            if field.x == x.x  - 25:
                if field.y == x.y:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y - 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y + 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
            elif field.x == x.x + 25:
                if field.y == x.y:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y - 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y + 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
            elif field.x == x.x:
                if field.y == x.y:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y - 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
                elif field.y == x.y + 25:
                    x.fieldType = "uncovered"
                    if x.flagged == True:
                        self.flags -= 1
                        x.flagged = False
            if x.fieldType == "uncovered":
                if self.setNumber(x) == 0:
                    self.empty_list.append(x)             

    # uncover field
    def uncover(self, field):
        self.field_list_sprite = None
        self.field_list_sprite = arcade.SpriteList()
        for field in self.field_list:
            if field.fieldType == "field" or field.fieldType == "bomb":
                if field.flagged:
                    uncovered_field = arcade.Sprite(self.flag_src, 1)
                else:
                    uncovered_field = arcade.Sprite(self.field_src, 1)
                uncovered_field.center_x = field.x
                uncovered_field.center_y = field.y
                self.field_list_sprite.append(uncovered_field)
            elif field.fieldType == "uncovered":
                uncovered_field = arcade.Sprite(self.switch_demo(self.setNumber(field)), 1)
                uncovered_field.center_x = field.x
                uncovered_field.center_y = field.y
                self.field_list_sprite.append(uncovered_field)

    # returns amount of bombs in adjanced fields
    def setNumber(self, field):
        i = 0
        for x in self.field_list:
            if field.x == x.x  - 25:
                if field.y == x.y:
                    if x.fieldType == "bomb":
                        i += 1
                elif field.y == x.y - 25:
                    if x.fieldType == "bomb":
                        i += 1                
                elif field.y == x.y + 25:
                    if x.fieldType == "bomb":
                        i += 1
            elif field.x == x.x + 25:
                if field.y == x.y:
                    if x.fieldType == "bomb":
                        i += 1
                elif field.y == x.y - 25:
                    if x.fieldType == "bomb":
                        i += 1                
                elif field.y == x.y + 25:
                    if x.fieldType == "bomb":
                        i += 1
            elif field.x == x.x:
                if field.y == x.y:
                    if x.fieldType == "bomb":
                        i += 1
                elif field.y == x.y - 25:
                    if x.fieldType == "bomb":
                        i += 1                
                elif field.y == x.y + 25:
                    if x.fieldType == "bomb":
                        i += 1
        return i

    # returns path to sprite
    def switch_demo(self, number):
        switcher = {
            0: self.field_empty_src,
            1: self.field_1_src,
            2: self.field_2_src,
            3: self.field_3_src,
            4: self.field_4_src,
            5: self.field_5_src,
            6: self.field_6_src,
            7: self.field_7_src,
            8: self.field_8_src
        }
        return switcher.get(number)

    # after clicking bomb uncover all bombs
    def uncovered_bombs(self):
        self.field_list_sprite = None
        self.field_list_sprite = arcade.SpriteList()
        for field in self.field_list:
            if field.fieldType == "bomb":
                uncovered_field = arcade.Sprite(self.bomb_src, 1)
            elif field.fieldType == "uncovered":
                uncovered_field = arcade.Sprite(self.switch_demo(self.setNumber(field)), 1)
            else:
                if field.flagged:
                    uncovered_field = arcade.Sprite(self.flag_src, 1)
                else:
                    uncovered_field = arcade.Sprite(self.field_src, 1)
            uncovered_field.center_x = field.x
            uncovered_field.center_y = field.y
            self.field_list_sprite.append(uncovered_field)             

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()