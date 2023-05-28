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
    {"name": "dark_blue_arkenstone", "value": 13, "weight": 0 ,"image": None, "nickname":"Dark Blue Arken"},
    {"name": "light_blue_arkenstone", "value": 12,"weight": 0 ,"image": None, "nickname":"Light Blue Arken"},
    {"name": "gold_coins", "value": 1, "weight": 0 , "image": None, "nickname":"Gold"},
    {"name": "red_gems", "value": 5, "weight": 0 ,"image": None, "nickname":"Red Gems"},
    {"name": "green_gems", "value": 7,"weight": 0 , "image": None, "nickname":"Green Gems"}
]

# Inicialização da janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Mochila")

clock = pygame.time.Clock()


current_dir = os.path.dirname(os.path.abspath(__file__))


fonts_dir = os.path.join(current_dir, "fonts")


font_path = os.path.join(fonts_dir, "blackchancery.regular.ttf")

input_style = os.getcwd() + "input_style.json"

manager = pygame_gui.UIManager((1200, 700), input_style)

manager.get_theme().load_theme(input_style)

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10 + (WIDTH * 0.27) , 100), (100, 30)), manager=manager,
                                                object_id='#main_text_entry')
text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10 + (WIDTH * 0.27), 215), (100, 30)), manager=manager,
                                                object_id='#main_text_entry2')
text_input3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10 + (WIDTH * 0.27), 330), (100, 30)), manager=manager,
                                                object_id='#main_text_entry3')
text_input4 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10 + (WIDTH * 0.27), 445), (100, 30)), manager=manager,
                                                object_id='#main_text_entry4')
text_input5 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10 + (WIDTH * 0.27), 560), (100, 30)), manager=manager,
                                                object_id='#main_text_entry5')


clock = pygame.time.Clock()

selected_items = []
empty_item = []
available_weight = 0
current_value = 0

def ramdom_pesos(items):
    global available_weight
    available_weight = random.randint(20,50)
    aux = available_weight * 3

    items[0]["weight"] = random.randint(1,7)
    items[1]["weight"] = random.randint(1,7)

    for item in items:
        temp = random.randint(7,aux//2)
        if aux - temp >= 0 and item["weight"] == 0:
            item["weight"] += temp
            aux -= temp
    return items
    
def draw_text(text, color, x, y, font_size):
    font = pygame.font.Font(font_path, font_size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_item(item, x, y):
    global empty_item
    if item in empty_item:
        color = RED
    else:
        color = GREEN
    screen.blit(item["image"][1], (x, y))
    draw_text(item["nickname"], WHITE, x + (WIDTH * 0.10), y, 24)
    draw_text("Value", color, x + (WIDTH * 0.10), y + (HEIGHT * 0.06), 17)
    draw_text("{}".format(item["value"]), color, x + (WIDTH * 0.12), y + (HEIGHT * 0.08),22) # o valor mostrado deve ser a multiplicacao do peso pelo value
    draw_text("Weigth", color, x + (WIDTH * 0.20), y + (HEIGHT * 0.06), 17)
    draw_text("{} kg".format(item["weight"]), color, x + (WIDTH * 0.22), y + (HEIGHT * 0.08), 21) # o peso gerado aleatoriamente entra aqui
    
def draw_border():
    border = load_image("borda_lotr.png",220,80)
    for aux in range(1,10):
        screen.blit(border[1], (WIDTH - (WIDTH * 0.54), HEIGHT - (80 * aux)))
    

def draw_game():
    global selected_items

    if available_weight == 0:
        color = RED
    else:
        color = WHITE

    screen.fill(BLACK)
    draw_border()
    background_image = load_image("thief2.jpg",528,810)
    screen.blit(background_image[1], (WIDTH - (WIDTH * 0.44), HEIGHT - (HEIGHT * 0.80)))
    draw_text("Selected items", WHITE, WIDTH - (WIDTH * 0.13), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("Available weight", color,  WIDTH - (WIDTH * 0.28), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("{} kg".format(available_weight), color,  WIDTH - (WIDTH * 0.25), HEIGHT - (HEIGHT * 0.95), 19)
    draw_text("Current value", WHITE,  WIDTH - (WIDTH * 0.43), HEIGHT - (HEIGHT * 0.98), 19)
    draw_text("{}".format(current_value), WHITE,  WIDTH - (WIDTH * 0.40), HEIGHT - (HEIGHT * 0.95), 19)
    
    for i, item in enumerate(items):
        draw_item(item, 10, 50 + i * 115)

    for i, item in enumerate(selected_items):
        
        draw_text("{}".format(item["nickname"]), WHITE, WIDTH - (WIDTH * 0.14), ((i+1) * 20) + HEIGHT - (HEIGHT * 0.97), 15)
        draw_text("{} kg".format(item["weight"]), WHITE, WIDTH - (WIDTH * 0.04), ((i+1) * 20) + HEIGHT - (HEIGHT * 0.97), 15)

def endgame():
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    text_input.visible = False
    text_input2.visible = False
    text_input3.visible = False
    text_input4.visible = False
    text_input5.visible = False

    screen.fill(BLACK)
    draw_text("Game Over, Mr. Baggins", WHITE, WIDTH * 0.33, HEIGHT - (HEIGHT * 0.97), 30)

    MENU_BUTTON = pygame.Rect((WIDTH / 2) - 150, HEIGHT - 125, 300, 50)
    MENU_TEXT = font.render("Return to main menu", True, WHITE)
    MENU_TEXT_RECT = MENU_TEXT.get_rect(center=MENU_BUTTON.center)

    QUIT_BUTTON = pygame.Rect((WIDTH / 2) - 150, (HEIGHT - 125) + (HEIGHT * 0.10), 300, 50)
    QUIT_TEXT = font.render("Exit", True, WHITE)
    QUIT_TEXT_RECT = QUIT_TEXT.get_rect(center=QUIT_BUTTON.center)

    pygame.draw.rect(screen, RED, MENU_BUTTON)
    pygame.draw.rect(screen, RED, QUIT_BUTTON)

    screen.blit(MENU_TEXT, MENU_TEXT_RECT)
    screen.blit(QUIT_TEXT, QUIT_TEXT_RECT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MENU_BUTTON.collidepoint(MENU_MOUSE_POS):
                print("Menu principal")

            if QUIT_BUTTON.collidepoint(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

        pygame.display.update()

def knapsack():
    global available_weight, current_value

    selected_items.clear()

    items.sort(key=lambda x: x["value"] / x["weight"], reverse=True)

    for item in items:
        if available_weight + item["weight"] <= MAX_CAPACITY:
            selected_items.append(item)
            available_weight += item["weight"]
            current_value += item["value"]

def load_image(file, width, height):
    image = pygame.image.load(f'images/{file}')
    image = pygame.transform.scale(image, (width, height))
    image_loc = image.get_rect()
    return image_loc, image

def procura_item(item):
    for i in range(len(selected_items)):
        if selected_items[i]["nickname"] == item:
            return i

def math_weight(item, text):
    global available_weight, current_value, selected_items, empty_item

    aux = available_weight - float(text)

    if aux >= 0 and float(text) <= items[item]["weight"]:
        available_weight -= float(text)
        current_value += float(text)*items[item]["value"]
        items[item]["weight"] -= float(text)
        if items[item]["weight"] == 0:
           empty_item.append(items[item])
        
        aux = procura_item(items[item]["nickname"])
        if aux != None:
            selected_items[aux]["weight"] += float(text)
        else:
            selected_items.append({"nickname":items[item]["nickname"],"weight":float(text)})


for item in items:
    item["image"] = load_image(item["name"] + ".png", 100,100)


total_time = 3
current_time = 0
starting_time = pygame.time.get_ticks()
timer_visible = True
# Loop principal do jogo
running = True
items = ramdom_pesos(items)
font = pygame.font.Font(font_path, 24)
while running:
    
    current_time = (pygame.time.get_ticks() - starting_time) / 1000
    if current_time >= total_time:
        timer_visible = False
        endgame()
    UI_REFRESH_RATE = clock.tick(60)/1000
    time_text = font.render("Time: {:.1f}".format(current_time), True, (255, 255, 255))
    if timer_visible:
        screen.blit(time_text, (10, 10))  # Desenhar o texto na tela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry':
            try:
                float(event.text)
                math_weight(0,event.text)
            except ValueError:
                print("Not a float")
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry2':
            try:
                float(event.text)
                math_weight(1,event.text)
            except ValueError:
                print("Not a float")
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry3':
            try:
                float(event.text)
                math_weight(2,event.text)
            except ValueError:
                print("Not a float")
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry4':
            try:
                float(event.text)
                math_weight(3,event.text)
            except ValueError:
                print("Not a float")
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry5':
            try:
                float(event.text)
                math_weight(4,event.text)
            except ValueError:
                print("Not a float")

        manager.process_events(event)

    manager.update(UI_REFRESH_RATE)

    manager.draw_ui(screen)
    pygame.display.update()
    draw_game()

    clock.tick(60)


# Encerramento do Pygame
pygame.quit()
