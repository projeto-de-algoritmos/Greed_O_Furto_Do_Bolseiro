import pygame
import random
import os
import pygame_gui
# Inicialização do Pygame
pygame.init()

# Dimensões da janela do jogo
WIDTH = 1200
HEIGHT = 700

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações da mochila
MAX_CAPACITY = 30

# Itens disponíveis
items = [
    {"name": "dark_blue_arkenstone", "value": 5, "image": None, "nickname":"Dark Blue Arkenstone"},
    {"name": "light_blue_arkenstone", "value": 5, "image": None, "nickname":"Light Blue Arkenstone"},
    {"name": "gold_coins", "value": 5, "image": None, "nickname":"Gold"},
    {"name": "red_gems", "value": 5, "image": None, "nickname":"Red Gems"},
    {"name": "green_gems", "value": 5, "image": None, "nickname":"Green Gems"}
    #{"name": "Moeda de prata", "weight": 3, "value": 2.5, "image": None},
    #{"name": "Moeda de bronze", "weight": 3, "value": 1, "image": None},
    #{"name": "Diamante", "weight": 5, "value": 10, "image": None},
]

# Inicialização da janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Mochila")

clock = pygame.time.Clock()


current_dir = os.path.dirname(os.path.abspath(__file__))


fonts_dir = os.path.join(current_dir, "fonts")


font_path = os.path.join(fonts_dir, "RINGM___.ttf")

input_style = os.getcwd() + ".\input_style.json"

manager = pygame_gui.UIManager((1600, 900), input_style)

manager.get_theme().load_theme(input_style)


clock = pygame.time.Clock()

selected_items = []
current_weight = 0
current_value = 0

def ramdom_items():
    global items
    

def draw_text(text, color, x, y, font_size):
    font = pygame.font.Font(font_path, font_size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_item(item, x, y):
    if item in selected_items:
        color = RED
    else:
        color = GREEN
    screen.blit(item["image"][1], (x, y))
    draw_text(item["nickname"], WHITE, x + (WIDTH * 0.10), y, 24)
    draw_text("Value", color, x + (WIDTH * 0.10), y + (HEIGHT * 0.06), 17)
    draw_text("{}".format(item["value"]), color, x + (WIDTH * 0.12), y + (HEIGHT * 0.08),22) # o valor mostrado deve ser a multiplicacao do peso pelo value
    draw_text("Weigth", color, x + (WIDTH * 0.20), y + (HEIGHT * 0.06), 17)
    draw_text("{} kg".format(10), color, x + (WIDTH * 0.22), y + (HEIGHT * 0.08), 21) # o peso gerado aleatoriamente entra aqui
    
def draw_border():
    border = load_image("borda_lotr.png",220,80)
    for aux in range(1,10):
        screen.blit(border[1], (WIDTH - (WIDTH * 0.54), HEIGHT - (80 * aux)))
    

def draw_game():
    screen.fill(BLACK)
    draw_border()
    background_image = load_image("thief2.jpg",528,810)
    screen.blit(background_image[1], (WIDTH - (WIDTH * 0.44), HEIGHT - (HEIGHT * 0.80)))
    draw_text("Selected items", WHITE, WIDTH - (WIDTH * 0.13), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("Current weight", WHITE,  WIDTH - (WIDTH * 0.28), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("{} kg".format(current_weight), WHITE,  WIDTH - (WIDTH * 0.22), HEIGHT - (HEIGHT * 0.95), 19)
    draw_text("Current value", WHITE,  WIDTH - (WIDTH * 0.43), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("{}".format(current_value), WHITE,  WIDTH - (WIDTH * 0.38), HEIGHT - (HEIGHT * 0.95), 19)

    
    for i, item in enumerate(items):
        draw_item(item, 10, 40 + i * 115)

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

def load_image(file, width, height):
    image = pygame.image.load(f'images/{file}')
    image = pygame.transform.scale(image, (width, height))
    image_loc = image.get_rect()
    return image_loc, image

for item in items:
    item["image"] = load_image(item["name"] + ".png", 100,100)



text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 400), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')

# Loop principal do jogo
running = True
while running:
    UI_REFRESH_RATE = clock.tick(60)/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry'):
                
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

        manager.process_events(event)

    manager.update(UI_REFRESH_RATE)

    manager.draw_ui(screen)
    pygame.display.update()
    draw_game()

    clock.tick(30)

# Encerramento do Pygame
pygame.quit()
