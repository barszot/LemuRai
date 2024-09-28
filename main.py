import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
FONT_SIZE = 32
UPDATE_INTERVAL = 1000  # Time in milliseconds (1 second)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window with Text Field")
# Load the image
lemur_image = pygame.image.load("icons/lemur.png")

# Resize the image to 32x32 pixels
lemur_image = pygame.transform.scale(lemur_image, (32, 32))

# Set the window icon
pygame.display.set_icon(lemur_image)


# Load the images
book_image = pygame.image.load("icons/book.png")
skull_image = pygame.image.load("icons/skull.png")
bacteria_image = pygame.image.load("icons/bacteria.png")
brain_image = pygame.image.load("icons/brain.png")

# Font setup
font = pygame.font.Font(None, FONT_SIZE)

# Variable to store input text
input_text = ""
external_text = ""
active = True  # Variable to track if text input is active

# Clock for controlling updates
clock = pygame.time.Clock()

# Track the last time the external text was updated
last_update_time = 0

# Button position and size
button_rect = pygame.Rect(700, 560, 100, 40)


def get_external_text():
    """
    This function simulates getting text from an external source.
    In a real scenario, this could be from a file, API, or other source.
    """
    return "Hello from external function!"


def render_icon(icon, icon_position, count):
    small_image = pygame.transform.scale(icon, (30, 30))
    screen.blit(small_image, icon_position)
    number_surface = font.render(str(count), True, WHITE)
    screen.blit(number_surface, (icon_position[0] + 40, icon_position[1] + 5))


def render_text_field():
    # Render the text field background
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 100, WIDTH, 100), 2)
    # Render the current input text
    text_surface = font.render(input_text, True, WHITE)
    screen.blit(text_surface, (35, 505))


def render_button():
    # Draw button and its label
    pygame.draw.rect(screen, BLUE, button_rect)
    small_font = pygame.font.Font(None, 24)
    button_text = small_font.render("Zatwierdź", True, WHITE)
    screen.blit(button_text, (button_rect.x + 11, button_rect.y + 11))


def render_external_text_field():
    # Render the external text field background
    pygame.draw.rect(screen, WHITE, (30, 400, 400, 40), 2)
    # Render the text from the external function
    external_text_surface = font.render(external_text, True, WHITE)
    screen.blit(external_text_surface, (35, 405))


def update_external_text_if_needed(current_time):
    global last_update_time, external_text
    if current_time - last_update_time > UPDATE_INTERVAL:
        external_text = get_external_text()  # Update external text every second
        last_update_time = current_time


def handle_submit():
    global input_text
    print(f"Text entered: {input_text}")
    input_text = ""  # Clear input after submission


# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character on backspace
                elif event.key == pygame.K_RETURN:
                    handle_submit()  # Submit text on Enter
                else:
                    input_text += event.unicode  # Add typed character to the input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                handle_submit()  # Submit text on button click

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Check if it's time to update the external text
    update_external_text_if_needed(current_time)

    # Fill the screen with black
    screen.fill(BLACK)

    # Render icons
    render_icon(lemur_image, (30, 30), 3)
    render_icon(book_image, (30, 60), 3)
    render_icon(skull_image, (90, 30), 3)
    render_icon(bacteria_image, (90, 60), 3)
    render_icon(brain_image, (150, 30), 3)

    # Render the text input field
    render_text_field()

    # Render the external text field
    render_external_text_field()

    # Render the submit button
    render_button()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
