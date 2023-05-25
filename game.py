import pygame
import random

# Inicialização do Pygame
pygame.init()

# Dimensões da janela do jogo
WIDTH = 800
HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações da mochila
MAX_CAPACITY = 30

# Itens disponíveis
items = [
    {"name": "dark_blue_arkenstone", "value": 5, "image": None},
    {"name": "dark_blue_arkenstone", "value": 5, "image": None},
    {"name": "gold_coins", "value": 5, "image": None},
    {"name": "gold_coins", "value": 5, "image": None},
    #{"name": "Moeda de prata", "weight": 3, "value": 2.5, "image": None},
    #{"name": "Moeda de bronze", "weight": 3, "value": 1, "image": None},
    #{"name": "Diamante", "weight": 5, "value": 10, "image": None},
]

# Inicialização da janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Mochila")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)

selected_items = []
current_weight = 0
current_value = 0

def ramdon_items():
    global items
    

def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_item(item, x, y):
    if item in selected_items:
        color = RED
    else:
        color = GREEN
    screen.blit(item["image"][1], (x, y))
    draw_text(item["name"], color, x + 10, y + 10)
    draw_text("Value: {}".format(item["value"]), color, x + 10, y + 50)


def draw_game():
    screen.fill(BLACK)

    draw_text("Selected items:", WHITE, 10, 10)
    draw_text("Current weight: {}".format(current_weight), WHITE, 10, 40)
    draw_text("Current value: {}".format(current_value), WHITE, 10, 70)

    
    for i, item in enumerate(items):
        draw_item(item, 10, 100 + i * 105)

    pygame.display.flip()


def knapsack():
    global current_weight, current_value

    current_weight = 0
    current_value = 0

    selected_items.clear()

    items.sort(key=lambda x: x["value"] / x["weight"], reverse=True)

    for item in items:
        if current_weight + item["weight"] <= MAX_CAPACITY:
            selected_items.append(item)
            current_weight += item["weight"]
            current_value += item["value"]

def load_image(file):
    image = pygame.image.load(f'images/{file}')
    image = pygame.transform.scale(image, (100, 100))
    image_loc = image.get_rect()
    return image_loc, image

for item in items:
    item["image"] = load_image(item["name"] + ".png")

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for i, item in enumerate(items):
                if 10 <= pos[0] <= 110 and 100 + i * 105 <= pos[1] <= 150 + i * 105:
                    if item in selected_items:
                        selected_items.remove(item)
                        current_weight -= 1
                        current_value -= item["value"]
                    else:
                        if current_weight + 1 <= MAX_CAPACITY:
                            selected_items.append(item)
                            current_weight += 1
                            current_value += item["value"]

    draw_game()

    clock.tick(30)

# Encerramento do Pygame
pygame.quit()
