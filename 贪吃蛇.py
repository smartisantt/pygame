import pygame
from color import Color
import random
from time import sleep,time
import time
import fileManager

window_width = 800
window_height = 600
window_edge = 40
map_width = window_width - 2*window_edge
map_height = window_height - 2*window_edge
file_name = 'max_score.json'
fps = 60

class Snake:

    pixel = 20

    def __init__(self):
        # self.window_width = 800
        # self.window_height = 600

        self.food = [4, 5]
        self.head = [3, 1]
        # self.body[0]是蛇尾
        self.body = [[1, 1], [2, 1]]
        self.moving_direction = 'right'
        self.speed = 20
        # 游戏难度，level[0]最慢
        self.level = [10, 8, 6, 4, 2]
        self.game_started = False
        self.is_stop = False
        self.score = 0
        content = fileManager.read_json_file(file_name)
        for key in content:
            self.max_score_time = key
            self.max_score = content[key]
        print(self.max_score)
        # self.max_score = content.get()

    def move_head(self):
        moves = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
        }
        step = moves[self.moving_direction]
        print(step)
        # 根据方向计算下一步蛇头坐标位置
        self.head[0] += step[0]
        self.head[1] += step[1]

    def generate_food(self):
        while True:
            x = random.randint(1, map_width // Snake.pixel - 1)
            y = random.randint(1, map_height // Snake.pixel - 1)
            if (x, y) != self.head and (x, y) not in self.body:
                self.food = [x, y]
                break


    @classmethod
    def new_draw_rect(cls, window, zb, color):
        pygame.draw.rect(window, color, ((zb[0]) * Snake.pixel + window_edge, (zb[1]) * Snake.pixel  + window_edge, Snake.pixel - 1, Snake.pixel - 1))

    def show_snake_and_food(self, window):
        window.fill(Color.white)
        pygame.draw.rect(window, Color.red, (window_edge, window_edge, map_width, map_height), 2)
        self.new_draw_rect(window, self.food, Color.red)
        self.new_draw_rect(window, self.head, Color.blue)
        for i in self.body:
            self.new_draw_rect(window, i, Color.green)

    def check_status(self):
        # 检测蛇的状态，吃到自己，到边界
        x, y = self.head
        max_x = map_width // Snake.pixel
        max_y = map_height // Snake.pixel
        if 0 <= x < max_x and 0 <= y < max_y and len(self.body) < max_x * max_y and self.head not in self.body:
            return False
        else:
            return True

    def check_direction(self, press_direction):
        if not self.is_stop:
            directions = [['up', 'down'], ['left', 'right']]
            if self.moving_direction in directions[0] and press_direction in directions[1]:
                self.moving_direction = press_direction
            elif self.moving_direction in directions[1] and press_direction in directions[0]:
                self.moving_direction = press_direction


def main():
    direction_dict = {
        pygame.K_DOWN: 'down',
        pygame.K_UP: 'up',
        pygame.K_LEFT: 'left',
        pygame.K_RIGHT: 'right',
        pygame.K_SPACE: 'stop'
    }
    snake = Snake()
    fps_clock = pygame.time.Clock()
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height), 0, 32)
    window.fill(Color.white)
    pygame.display.set_caption('My Snake')
    # ================文字显示部分=================
    title_font = pygame.font.SysFont('arial', 62)
    welcome_words = title_font.render('Welcome to My Snake', True, Color.black, Color.white)

    game_over_words = title_font.render('Game Over', True, Color.black, Color.white)
    win_words = title_font.render('Win', True, Color.black, Color.white)

    tips_font = pygame.font.SysFont('arial', 32)
    start_game_words = tips_font.render('Click to Start Game', True, Color.black, Color.white)
    close_game_words = tips_font.render('Press ESC to Close', True, Color.black, Color.white)
    small_font = pygame.font.SysFont('arial', 22)
    window.blit(welcome_words, (148, 100))
    window.blit(start_game_words, (278, 300))
    window.blit(close_game_words, (278, 350))
    # ==============================================
    pygame.display.flip()
    # 事件响应部分
    # time_count控制蛇移动速断，fps控制的是每秒刷新屏幕多少次
    time_count = 0
    while True:
        time_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_SPACE:
                    snake.is_stop = not snake.is_stop
                elif snake.game_started and event.key in direction_dict:
                    # print(direction_dict[event.key])
                    press_direction = direction_dict[event.key]
                    snake.check_direction(press_direction)

            elif (not snake.game_started) and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if 278 <= x <= 504 and 308 <= y <= 327:
                    snake.game_started = True

        # 游戏运作部分
        if snake.game_started:
            if time_count%snake.level[3] == 0:
                time_count = 0
                if not snake.is_stop:
                    # 不能写成snake.body.append(snake.head)，这样head值变得时候会跟着变
                    snake.body.append(snake.head[:])
                    snake.move_head()
                    if snake.head == snake.food:
                        snake.score += 50
                        snake.generate_food()
                    else:
                        snake.body.pop(0)
            snake.show_snake_and_food(window)
            score_font = small_font.render('score: %d'% snake.score, True, Color.black, Color.white)
            window.blit(score_font, (50, 10))
            max_score = small_font.render('max_score_time:%s      max_score: %d' %(snake.max_score_time, snake.max_score), True, Color.black, Color.white)
            window.blit(max_score, (222, 10))
            if snake.check_status() or len(snake.body) == 400:
                snake.is_stop = True
                last_score_words = tips_font.render('score:%d' % snake.score, True, Color.black, Color.white)
                window.blit(last_score_words, (360, 317))
                if len(snake.body) == 400:
                    window.blit(win_words, (380, 217))
                else:
                    window.blit(game_over_words, (277, 217))
                if snake.score > snake.max_score:
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    write_content = {time_str : snake.score}
                    fileManager.write_json_file(write_content, file_name)
                pygame.display.update()
                sleep(2)
                snake = Snake()
        else:
            window.fill(Color.white)
            window.blit(welcome_words, (148, 100))
            window.blit(start_game_words, (278, 300))
            window.blit(close_game_words, (278, 350))
        fps_clock.tick(fps)
        pygame.display.update()

if __name__ == '__main__':
    main()
