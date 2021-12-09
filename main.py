import pygame
import random
from settings import *

pygame.init()
pygame.display.set_caption('Greedy Crab')


class Main:
    def __init__(self):
        self.crab = Crab()
        self.board = Board()
        self.menus = Menus()
        self.manager = Manager()
        self.jellyfish_1 = Enemy(1)
        self.jellyfish_2 = Enemy(2)
        self.stingray_1 = Enemy(3)
        self.stingray_2 = Enemy(4)
        self.urchin_1 = Enemy(5)
        self.urchin_2 = Enemy(6)
        self.fish_1 = Enemy(7)
        self.fish_2 = Enemy(8)

        self.enemies = [self.jellyfish_1, self.jellyfish_2, self.stingray_1, self.stingray_2, self.urchin_1,
                        self.urchin_2, self.fish_1, self.fish_2, ]

        self.mm = True
        self.htp = False
        self.dead = False

        self.route = []
        self.gr = False

        self.waited = False

    def setup(self):
        self.board.setup_board()

    def game_loop(self):
        if self.mm:
            self.menus.main_menu()
            self.menus.mouse_manager()
            self.menus.hover_manager()
            self.menus.click_manager()
        elif self.htp:
            self.menus.htp()
        elif self.dead:
            self.menus.game_over()
        else:
            self.board.draw()
            self.crab.draw()
            self.crab.border()
            self.crab.get_coin()
            for enemy in self.enemies:
                enemy.draw_move()
                enemy.generate_wait_steps()
            self.manager.drawer()
            self.manager.collision_manager()
            self.manager.display_score()
            self.manager.increase_difficulty()


class Crab:
    def __init__(self):
        self.crab_r = pygame.image.load('data/img/crab.png').convert_alpha()
        self.crab_l = pygame.transform.flip(self.crab_r, True, False)
        self.crab = self.crab_r
        self.pos = [322, 285]
        self.jump_speed = 0
        self.speed = 0
        self.score = 0

    def draw(self):
        if self.speed > 0:
            self.crab = self.crab_r
        elif self.speed < 0:
            self.crab = self.crab_l

        screen.blit(self.crab, self.pos)

    def move(self, direction):
        if self._can_move(direction):
            if direction == 'up':
                self.pos[1] -= main.board.tile_size
            if direction == 'right':
                self.pos[0] += main.board.tile_size
            if direction == 'down':
                self.pos[1] += main.board.tile_size
            if direction == 'left':
                self.crab = pygame.transform.flip(self.crab, True, False)
                self.pos[0] -= main.board.tile_size

    def _can_move(self, direction):
        if direction == 'up':
            vector = [0, -1]
        if direction == 'right':
            vector = [1, 0]
        if direction == 'down':
            vector = [0, 1]
        if direction == 'left':
            vector = [-1, 0]

        tile = round(self.pos[0] / main.board.tile_size), round(self.pos[1] / main.board.tile_size)
        next_tile = (tile[0] + vector[0], tile[1] + vector[1])

        try:
            n_tile_type = board[next_tile[1]][next_tile[0]]
        except:
            return False

        if n_tile_type == 1:
            return False
        else:
            return True

    def border(self):
        if self.pos[0] > 560:
            self.pos[0] = 560
        if self.pos[0] <= 0:
            self.pos[0] = 0

        if self.pos[1] > 565:
            self.pos[1] = 565
        if self.pos[1] < 40:
            self.pos[1] = 40

    def get_coin(self):
        a = True if self.pos[0] == main.manager.pos[0] and self.pos[1] == main.manager.pos[1] + 1 else False
        b = True if self.pos[0] == main.manager.pos[0] - 2 and self.pos[1] == main.manager.pos[1] + 1 else False

        if a or b:
            board[main.board.row][main.board.col] = 0
            self.score += 1
            main.board.generate_coin_pos()


class Enemy:
    def __init__(self, num):
        if num == 1:
            self.route = route_1
        elif num == 2:
            self.route = route_2
        elif num == 3:
            self.route = route_3
        elif num == 4:
            self.route = route_4
        elif num == 5:
            self.route = route_5
        elif num == 6:
            self.route = route_6
        elif num == 7:
            self.route = route_7
        elif num == 8:
            self.route = route_8

        self.jellyfish = pygame.image.load('data/img/jellyfish.png').convert_alpha()
        self.stingray = pygame.image.load('data/img/stingray.png').convert_alpha()
        self.urchin = pygame.image.load('data/img/urchin.png').convert_alpha()
        self.fish = pygame.image.load('data/img/fish.png').convert_alpha()

        if num in [1, 2]:
            self.img = self.jellyfish
        elif num in [3, 4]:
            self.img = self.stingray
        elif num in [5, 6]:
            self.img = self.urchin
        elif num in [7, 8]:
            self.img = self.fish

        self.pos_index = 0

        self.step = 0

        self.wait_steps_dif = ((20, 18, 16, 12), (15, 13, 11, 8), (18, 15, 13, 10), (13, 11, 8, 6))
        self.dif_index = 0

        self.num = num
        self.generate_wait_steps()

    def generate_wait_steps(self):
        if self.num in [1, 2]:
            self.wait_steps = self.wait_steps_dif[0][self.dif_index]
        elif self.num in [3, 4]:
            self.wait_steps = self.wait_steps_dif[1][self.dif_index]
        elif self.num in [5, 6]:
            self.wait_steps = self.wait_steps_dif[2][self.dif_index]
        elif self.num in [7, 8]:
            self.wait_steps = self.wait_steps_dif[3][self.dif_index]

    def draw_move(self):
        screen.blit(self.img, tile_to_coordinate(self.route[self.pos_index]))

        if self.step < self.wait_steps:
            self.step += 1
        else:
            self.step = 0

            if self.pos_index < len(self.route) - 1:
                self.pos_index += 1
            else:
                self.pos_index = 0

            # update board
            idx = self.route[self.pos_index]
            prev_idx = self.route[self.pos_index - 1]
            board[idx[1]][idx[0]] = 3
            board[prev_idx[1]][prev_idx[0]] = 0


class Board:
    def __init__(self):
        self.tile_size = 40
        self.tiles_num = (25, 15)
        self.offset = (0, 0)
        self.tiles = []
        self.coin_pos = None
        self.row, self.col = None, None
        self.generate_coin_pos()

    def setup_board(self):
        for y in enumerate(board):
            for x in enumerate(y[1]):
                if board[y[0]][x[0]] != 1:
                    self.tiles.append(
                        pygame.rect.Rect(x[0] * self.tile_size, self.offset[1] + y[0] * self.tile_size, 39.9,
                                         39.9))

    def draw(self):
        for i in range(len(self.tiles)):
            pygame.draw.rect(screen, (0, 150, 200), self.tiles[i])

    def generate_coin_pos(self):
        self.row = random.randint(0, 14)
        self.col = random.randint(0, 14)

        if board[self.row][self.col] != 1:
            board[self.row][self.col] = 2
        elif board[self.row][self.col] == 1:
            self.generate_coin_pos()
            return

        coin_pos = self.col * self.tile_size, self.row * self.tile_size

        self.coin_pos = coin_pos


class Menus:

    def __init__(self):
        self.coin_big = pygame.image.load('data/img/btc_big.png').convert_alpha()
        self.menu_bg = pygame.image.load('data/img/bg.png').convert_alpha()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (571, 406))
        self.menu_coin_pos = [80, 315]
        self.frame = 0
        self.wait_frames = 40
        self.menu_text = pygame.image.load('data/img/text_logo.png').convert_alpha()

        self.play_button = pygame.rect.Rect(310, 550, 270, 80)
        self.play_text = pygame.image.load('data/img/play_text.png').convert_alpha()

        self.htp_button = pygame.rect.Rect(30, 550, 270, 80)
        self.htp_text = pygame.image.load('data/img/htp_text.png').convert_alpha()

        self.active_color = (40, 40, 40)
        self.hover_color = (60, 60, 60)
        self.play_color = self.active_color
        self.htp_color = self.active_color

        self.htp_instructions = pygame.image.load('data/img/htp.png').convert_alpha()

        self.game_over_logo = pygame.image.load('data/img/game_over_logo.png').convert_alpha()
        self.play_again = pygame.image.load('data/img/play_again.png').convert_alpha()
        self.return_menu_logo = pygame.image.load('data/img/return_menu.png').convert_alpha()

        pygame.mixer.music.load('data/bgm/menu.wav')
        pygame.mixer.music.play(-1)

    def main_menu(self):
        screen.fill((60, 70, 90))
        screen.blit(self.menu_bg, (15, 230))
        screen.blit(self.coin_big, self.menu_coin_pos)

        if self.frame == self.wait_frames:
            if self.menu_coin_pos == [80, 315]:
                self.menu_coin_pos = [80, 300]
                self.frame = 0
            else:
                self.menu_coin_pos = [80, 315]
                self.frame = 0
        self.frame += 1

        screen.blit(self.menu_text, (110, 10))

        pygame.draw.rect(screen, self.play_color, self.play_button)
        screen.blit(self.play_text, (370, 550))

        pygame.draw.rect(screen, self.htp_color, self.htp_button)
        screen.blit(self.htp_text, (35, 565))

    def htp(self):
        screen.fill((60, 70, 90))
        screen.blit(self.htp_instructions, (20, 20))

    def game_over(self):
        main.manager.restore_pos()
        screen.fill((0, 0, 40))
        screen.blit(self.game_over_logo, (70, 40))
        screen.blit(self.play_again, (20, 500))
        screen.blit(self.return_menu_logo, (50, 570))

    def mouse_manager(self):
        if mouse_hover(310, 550, 270, 80):
            return 1
        elif mouse_hover(30, 550, 270, 80):
            return 2
        else:
            return 0

    def hover_manager(self):
        if self.mouse_manager() == 1:
            self.play_color = self.hover_color
        elif self.mouse_manager() == 2:
            self.htp_color = self.hover_color
        else:
            self.play_color = self.active_color
            self.htp_color = self.active_color

    def click_manager(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            if self.mouse_manager() == 1:
                main.mm = False
            elif self.mouse_manager() == 2:
                main.mm = False
                main.htp = True


class Manager:
    def __init__(self):
        self.coin = pygame.image.load('data/img/btc.png').convert_alpha()
        self.pos = [6, 500]

        self.score_font = pygame.font.SysFont('Verdana', 20)

    def drawer(self):
        self.pos = [main.board.coin_pos[0] + 2, main.board.coin_pos[1] + 4]
        screen.blit(self.coin, self.pos)

    def collision_manager(self):
        tile = coordinate_to_tile(main.crab.pos)
        if board[tile[1]][tile[0]] == 3:
            main.dead = True

    def display_score(self):
        self.score_render = self.score_font.render(f'Score: {main.crab.score}', True, (250, 250, 250))
        screen.blit(self.score_render, (20, 5))

    def increase_difficulty(self):
        if main.crab.score in range(15, 25):
            for enemy in main.enemies:
                enemy.dif_index = 1
        elif main.crab.score in range(25, 40):
            for enemy in main.enemies:
                enemy.dif_index = 2
        elif main.crab.score > 40:
            for enemy in main.enemies:
                enemy.dif_index = 3

    def restore_pos(self):
        main.crab.pos = [322, 285]
        main.crab.score = 0
        for enemy in main.enemies:
            enemy.pos_index = 0
            enemy.dif_index = 0

        board = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ]


def tile_to_coordinate(tile):
    return tile[0] * main.board.tile_size, tile[1] * main.board.tile_size


def coordinate_to_tile(coordinate):
    return round(coordinate[0] / main.board.tile_size), round(coordinate[1] / main.board.tile_size)


def no_repeat(mylist):
    return list(dict.fromkeys(mylist))


def mouse_hover(x, y, w, h):
    area_x = range(x, x + w)
    area_y = range(y, y + h)

    if pygame.mouse.get_pos()[0] in area_x:
        if pygame.mouse.get_pos()[1] in area_y:
            return True

    return False


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                main.crab.move('right')
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                main.crab.move('left')
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                main.crab.move('up')
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                main.crab.move('down')
            if event.key == pygame.K_p:
                main.mm = False
                main.dead = False
            if event.key == pygame.K_r and (main.htp or main.dead):
                main.htp = False
                main.mm = True
                main.dead = False


screen = pygame.display.set_mode((600, 650))
main = Main()
main.setup()

while True:
    events()
    screen.fill((0, 30, 60))
    main.game_loop()
    pygame.display.update()
    pygame.time.Clock().tick(60)
