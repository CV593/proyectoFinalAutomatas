import pygame
import random
import os
import tkinter as tk
from tkinter import filedialog

NUM_CELLS = 100
VISIBLE_CELLS = 15
CELL_WIDTH = 80
SCREEN_WIDTH = VISIBLE_CELLS * CELL_WIDTH
SCREEN_HEIGHT = 700
position = 0
range_start = 0
range_end = NUM_CELLS - 1
cinta_original = []
cinta_modificada = []
cinta_cargada = []
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Máquina de Turing con Menú Mejorado")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
BLUE = (0, 102, 204)
GREEN = (0, 204, 0)
RED = (255, 51, 51)
BACKGROUND_COLOR = (240, 240, 240)
HIGHLIGHT_COLOR = (255, 239, 213)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
temp_message = ""
temp_message_timer = 0

def generar_cinta():
    cinta = ['B' if i % 15 == 0 else random.choice(['0', '1']) for i in range(NUM_CELLS)]
    guardar_cinta("cinta_generada.txt", cinta)
    return cinta

def guardar_cinta(filename, cinta):
    try:
        with open(filename, 'w') as file:
            file.write("".join(cinta))
        return True
    except Exception as e:
        print(f"Error al guardar cinta: {e}")
        return False

def cargar_cinta(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return list(file.read().strip())
        except Exception as e:
            print(f"Error al cargar cinta: {e}")
    return None

def draw_text(screen, text, x, y, color, font):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_tape(cinta, tape_position, is_active, y_position, title):
    draw_text(screen, title, 50, y_position - 40, BLACK, font)
    start_index = max(0, tape_position - VISIBLE_CELLS // 2)
    end_index = min(NUM_CELLS, start_index + VISIBLE_CELLS)
    
    for i in range(start_index, end_index):
        x = (i - start_index) * CELL_WIDTH + (SCREEN_WIDTH - VISIBLE_CELLS * CELL_WIDTH) // 2
        color = BLUE if i == tape_position and is_active else BLACK
        pygame.draw.rect(screen, HIGHLIGHT_COLOR if i == tape_position else BACKGROUND_COLOR, 
                         (x, y_position, CELL_WIDTH, CELL_WIDTH))
        pygame.draw.rect(screen, color, (x, y_position, CELL_WIDTH, CELL_WIDTH), 2)
        text = font.render(cinta[i], True, BLACK)
        screen.blit(text, (x + 25, y_position + 15))

def menu_principal():
    screen.fill(BACKGROUND_COLOR)
    options = [
        "1. Generar cinta",
        "2. Abrir cinta",
        "3. Modificar cinta",
        "4. Mostrar cinta",
        "5. Salir"
    ]
    y = 50
    draw_text(screen, "Máquina de Turing - Menú Principal", SCREEN_WIDTH // 2 - 200, y, ORANGE, font)
    y += 50
    for option in options:
        pygame.draw.rect(screen, GRAY, (50, y - 10, 300, 40), border_radius=5)
        draw_text(screen, option, 60, y, BLACK, font)
        y += 60
    pygame.display.flip()

def abrir_selector_archivo():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename()
    return file_path

def input_box(prompt):
    input_str = ""
    prompt_surface = font.render(prompt, True, BLACK)
    active = True
    while active:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(prompt_surface, (50, 100))
        draw_text(screen, "Ingrese el rango (ej: 20,25):", 50, 150, BLACK, font)
        pygame.draw.rect(screen, WHITE, (50, 200, 300, 40))
        text_surface = font.render(input_str, True, BLACK)
        screen.blit(text_surface, (60, 210))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_str
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                else:
                    input_str += event.unicode
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def confirmar_guardado():
    screen.fill(BACKGROUND_COLOR)
    draw_text(screen, "¿Guardar cinta modificada?", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, BLACK, font)
    draw_text(screen, "Presiona S para Sí o N para No", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, BLACK, font)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                elif event.key == pygame.K_n:
                    return False

def mostrar_mensaje_temporal(mensaje, color):
    global temp_message, temp_message_timer
    temp_message = mensaje
    temp_message_timer = pygame.time.get_ticks() + 3000  

def main():
    global temp_message, temp_message_timer
    global cinta_original, cinta_modificada, cinta_cargada, position, range_start, range_end
    cinta_modificada = cinta_original = generar_cinta()
    selected_option = None
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        if selected_option is None:
            menu_principal()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if selected_option is None:
                    if event.key == pygame.K_1:
                        cinta_original = generar_cinta()
                        cinta_modificada = cinta_original.copy()
                        mostrar_mensaje_temporal("Máquina de Turing generada correctamente", RED)
                    elif event.key == pygame.K_2:
                        file_path = abrir_selector_archivo()
                        if file_path:
                            cinta_cargada = cargar_cinta(file_path)
                            if cinta_cargada:
                                cinta_modificada = cinta_cargada.copy()
                                mostrar_mensaje_temporal("Archivo cargado correctamente", RED)
                    elif event.key == pygame.K_3:
                        rango = input_box("Rango de modificación")
                        if rango:
                            try:
                                range_start, range_end = map(int, rango.split(','))
                                if 0 <= range_start < range_end < NUM_CELLS:
                                    position = range_start
                                    mostrar_mensaje_temporal("Rango establecido correctamente", GREEN)
                                    selected_option = "modificar"
                                else:
                                    mostrar_mensaje_temporal("Rango fuera de límites", RED)
                            except ValueError:
                                mostrar_mensaje_temporal("Error en el formato de rango", RED)
                    elif event.key == pygame.K_4:
                        selected_option = "mostrar"
                    elif event.key == pygame.K_5:
                        running = False
                else:
                    if selected_option == "modificar":
                        if event.key == pygame.K_LEFT and position > range_start:
                            position -= 1
                        elif event.key == pygame.K_RIGHT and position < range_end:
                            position += 1
                        elif event.key == pygame.K_0:
                            cinta_modificada[position] = '0'
                        elif event.key == pygame.K_1:
                            cinta_modificada[position] = '1'
                        elif event.key == pygame.K_b:
                            cinta_modificada[position] = 'B'
                        elif event.key == pygame.K_SPACE:
                            selected_option = None
                    elif selected_option == "mostrar":
                        if event.key == pygame.K_SPACE:
                            selected_option = None
                        elif event.key == pygame.K_LEFT:
                            position = max(0, position - 1)
                        elif event.key == pygame.K_RIGHT:
                            position = min(NUM_CELLS - 1, position + 1)
                        elif event.key == pygame.K_g:
                            if confirmar_guardado():
                                guardar_cinta("cinta_modificada.txt", cinta_modificada)
                                mostrar_mensaje_temporal("Cinta modificada guardada correctamente", GREEN)
                            else:
                                os.remove("cinta_modificada.txt")
                                mostrar_mensaje_temporal("Guardado cancelado", RED)
        if temp_message_timer > 0 and pygame.time.get_ticks() > temp_message_timer:
            temp_message = ""
            temp_message_timer = 0
        draw_text(screen, temp_message, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, GREEN if temp_message else BLACK, font)
        if selected_option == "modificar":
            draw_tape(cinta_modificada, position, True, 200, "Cinta Modificada")
            mostrar_instrucciones([
                "Usa FLECHAS IZQUIERDA/DERECHA para mover el cabezal.",
                "Tecla '0', '1', 'B' para modificar.",
                "Tecla ESPACIO para regresar al menú principal."
            ])
        elif selected_option == "mostrar":
            draw_tape(cinta_original, position, False, 150, "Cinta Original")
            draw_tape(cinta_modificada, position, True, 350, "Cinta Modificada")
            mostrar_instrucciones([
                "FLECHAS IZQUIERDA/DERECHA: mover cinta original.",
                "Teclas A y S: mover cinta modificada.",
                "Tecla ESPACIO para regresar al menú principal.",
                "Tecla 'G' para guardar la cinta modificada."
            ])
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()

def mostrar_instrucciones(texto_instrucciones):
    y = SCREEN_HEIGHT - 180
    for linea in texto_instrucciones:
        instruccion = font.render(linea, True, GREEN)
        screen.blit(instruccion, (50, y))
        y += 30

if __name__ == "__main__":
    main()
