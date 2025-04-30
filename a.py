import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finder")

RED = (255, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (126, 126, 126)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return False

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = RED

    def draw(self, win):
        if self.color != WHITE:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, ends):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = min([h(start.get_pos(), end.get_pos()) for end in ends])

    open_set_hash = {start}
    end_set = set(ends)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current in end_set:
            reconstruct_path(came_from, current, draw)
            return current

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + min([h(neighbor.get_pos(), end.get_pos()) for end in ends])
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        draw()

    return None


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, background=None):
    if background:
        win.blit(background, (0, 0))

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 100
    grid = make_grid(ROWS, width)

    bg_image = pygame.image.load("Walmart-layout.png").convert()
    bg_image = pygame.transform.scale(bg_image, (width, width))
    bg_image.set_alpha(60)

    start = None
    original_start = None
    endpoints = []

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width, background=bg_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot not in endpoints:
                    start = spot
                    original_start = spot
                    start.make_start()
                elif spot != start and spot not in endpoints:
                    spot.make_end()
                    endpoints.append(spot)

            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot in endpoints:
                    endpoints.remove(spot)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and start and endpoints:
                    started = True
                    while endpoints:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        target = algorithm(lambda: draw(win, grid, ROWS, width, background=bg_image), grid, start, endpoints)
                        if target is None:
                            break
                        start = target
                        start.make_start()
                        endpoints.remove(target)

                    # Return to original start at the end
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width, background=bg_image), grid, start, [original_start])
                    original_start.make_end()

    pygame.quit()


main(WIN, WIDTH)
