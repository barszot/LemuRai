import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window with Text Field")

# Set up font
font = pygame.font.Font(None, FONT_SIZE)

# Text input variables
input_box = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color = color_inactive
active = False
text = ""

# Load the image
lemur_image = pygame.image.load("icons/lemur.png")
book_image = pygame.image.load("icons/book.png")
skull_image = pygame.image.load("icons/skull.png")
bacteria_image = pygame.image.load("icons/bacteria.png")
brain_image = pygame.image.load("icons/gitbrain.png")


def render_icon(icon, icon_position, count):
    small_image = pygame.transform.scale(icon, (30, 30))
    screen.blit(small_image, icon_position)
    number_surface = font.render(str(count), True, WHITE)
    screen.blit(number_surface, (icon_position[0] + 40, icon_position[1] + 5))


def render_text_box():
    # Render the current text.
    txt_surface = font.render(text, True, WHITE)
    # Resize the box if the text is too long.
    width = max(200, WIDTH)
    input_box.w = width
    # Blit the text.
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)  # Print the text to the console
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Fill the screen with white
    screen.fill(BLACK)

    # render_lemur_icon(2)
    # render_book_icon(3)
    render_icon(lemur_image, (30, 30), 3)
    render_icon(book_image, (30, 60), 3)
    render_icon(skull_image, (90, 30), 3)
    render_icon(bacteria_image, (90, 60), 3)
    render_icon(brain_image, (150, 30), 3)

    render_text_box()
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
