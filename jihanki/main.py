import pyxel

class App:
    def __init__(self) -> None:
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load("jihanki_resource.pyxres")
        # コイン
        self.y_init = 60
        self.x_init = 80
        self.init_coin()
        # 自販機
        self.j_x = 0
        self.j_y = 10
        self.j_vx = 1
        # ラベル
        self.lb_x = 0
        self.lb_y = 0

        self.input_money = 0
        pyxel.run(self.update, self.draw)

    def init_coin(self):
        self.x = self.x_init
        self.y = self.y_init
        self.state = "Waiting" # "Pulled", "Fired"
        self.vx = 0
        self.vy = 0

    def update(self):
        # 自販機
        self.j_x += self.j_vx
        if self.j_x < 0 or pyxel.width - 16 < self.j_x:
            self.j_vx = -self.j_vx

        # コイン
        match self.state:
            case "Waiting":
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and \
                    self.check_hit_rect_point(self.x, self.y, 16, 16, pyxel.mouse_x, pyxel.mouse_y):
                    self.state = "Pulled"
                    self.y = pyxel.mouse_x - 8
                    self.y = pyxel.mouse_y - 8
            case "Pulled":
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and \
                    self.check_hit_rect_point(self.x, self.y, 16, 16, pyxel.mouse_x, pyxel.mouse_y):
                    self.x = pyxel.mouse_x -8
                    self.y = pyxel.mouse_y - 8
                else:
                    self.state = "Fired"
                    self.vx = (self.x - self.x_init) / 6.0
                    self.vy = (self.y - self.y_init) / 3.5
            case "Fired":
                self.vy -= 0.5
                self.x -= self.vx
                self.y -= self.vy
                if self.y < -100 or pyxel.height < self.y:
                    self.init_coin()
                if  -8.0 < self.vy < 3.5:
                    if self.check_hit_rect_point(self.j_x, self.j_y, 16, 16, self.x+8, self.y+8):
                        self.input_money += 100
                        self.state = "Hiddening"
                        self.lb_x = self.j_x
                        self.lb_y = self.j_y + 3
                        self.y = 0
            case "Hiddening":
                self.lb_y -= 0.4
                if self.lb_y < self.j_y - 5:
                    self.init_coin()


    def draw(self):
        pyxel.cls(0)
        pyxel.text(100, 5, "Input: $" + str(self.input_money), 1)
        
        if self.state == "Pulled":
            pyxel.line(self.x_init, self.y_init, self.x+8, self.y+8, 6)

        pyxel.blt(self.j_x, self.j_y,
                  0,
                  0, 16,
                  16, 16,
                  0)
        
        if self.state == "Hiddening":
            pyxel.text(self.lb_x, self.lb_y, "100", 7)
        else:
            pyxel.blt(self.x, self.y,
                  0,
                  16, 16,
                  16, 16,
                  0)


    def check_hit_rect_point(self, x1, y1, w, h, x2, y2):
        if x1 <= x2 and x2 <= x1 + w and y1 <= y2 and y2 <= y1 + h:
            return True
        return False
            

App()

