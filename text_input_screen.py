import pygame
import sys
from communicating import Communicator

class TextInputScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.FONT_SIZE = 32
        self.UPDATE_INTERVAL = 1000  # Time in milliseconds (1 second)
        self.BACKSPACE_HOLD_TIME = 300  # Time in milliseconds to hold backspace to start rapid delete
        self.BACKSPACE_REPEAT_INTERVAL = 100  # Time in milliseconds for rapid delete

        # Set up the display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Window with Text Field")

        # Load the image
        self.lemur_image = pygame.image.load("icons/lemur.png")
        self.lemur_image = pygame.transform.scale(self.lemur_image, (32, 32))
        pygame.display.set_icon(self.lemur_image)

        # Load the other images
        self.book_image = pygame.image.load("icons/book.png")
        self.skull_image = pygame.image.load("icons/skull.png")
        self.bacteria_image = pygame.image.load("icons/bacteria.png")
        self.brain_image = pygame.image.load("icons/brain.png")

        # Font setup
        self.font = pygame.font.Font(None, self.FONT_SIZE)

        # Variables
        self.input_text = ""
        self.external_text = ""
        self.active = True  # Variable to track if text input is active
        self.clock = pygame.time.Clock()
        self.last_update_time = 0
        self.button_rect = pygame.Rect(700, 560, 100, 40)

        # Backspace tracking
        self.backspace_pressed = False
        self.backspace_last_delete_time = 0
        self.backspace_initial_press = True
        self.user_text = ""

    def get_external_text(self, text = "Hello from external function!"):
        """Simulates getting text from an external source."""
        return text

    def render_icon(self, icon, icon_position, count):
        small_image = pygame.transform.scale(icon, (30, 30))
        self.screen.blit(small_image, icon_position)
        number_surface = self.font.render(str(count), True, self.WHITE)
        self.screen.blit(number_surface, (icon_position[0] + 40, icon_position[1] + 5))

    def render_text_field(self):
        """Render the text input field."""
        pygame.draw.rect(self.screen, self.WHITE, (0, self.HEIGHT - 100, self.WIDTH, 100), 2)
        text_surface = self.font.render(self.input_text, True, self.WHITE)
        self.screen.blit(text_surface, (35, 505))

    def render_button(self):
        """Render the submit button."""
        pygame.draw.rect(self.screen, self.BLUE, self.button_rect)
        small_font = pygame.font.Font(None, 24)
        button_text = small_font.render("Zatwierdź", True, self.WHITE)
        self.screen.blit(button_text, (self.button_rect.x + 11, self.button_rect.y + 11))

    def render_external_text_field(self):
        """Render the external text field."""
        pygame.draw.rect(self.screen, self.WHITE, (30, 400, 400, 40), 2)
        external_text_surface = self.font.render(self.external_text, True, self.WHITE)
        self.screen.blit(external_text_surface, (35, 405))

    def update_external_text_if_needed(self, current_time):
        """Update external text every second."""
        if current_time - self.last_update_time > self.UPDATE_INTERVAL:
            self.external_text = self.get_external_text()
            self.last_update_time = current_time

    def handle_submit(self):
        """Handle the text submission."""
        print(f"Text entered: {self.input_text}")
        #self.input_text = ""  # Clear input after submission

    def run_screen(self):
        """Main loop for the screen."""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            if self.backspace_initial_press:
                                self.input_text = self.input_text[:-1]  # Immediately remove one character
                                self.backspace_initial_press = False
                            self.backspace_pressed = True
                            self.backspace_last_delete_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_RETURN:
                            self.handle_submit()
                        else:
                            self.input_text += event.unicode
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_pressed = False
                        self.backspace_initial_press = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.handle_submit()

            # Get the current time in milliseconds
            current_time = pygame.time.get_ticks()

            # Check if it's time to update the external text
            self.update_external_text_if_needed(current_time)

            # Handle backspace hold for rapid delete
            if self.backspace_pressed:
                if current_time - self.backspace_last_delete_time > self.BACKSPACE_HOLD_TIME:
                    if current_time - self.backspace_last_delete_time > self.BACKSPACE_REPEAT_INTERVAL:
                        if len(self.input_text) > 0:
                            self.input_text = self.input_text[:-1]
                            self.backspace_last_delete_time = current_time

            # Fill the screen with black
            self.screen.fill(self.BLACK)

            # Render icons
            self.render_icon(self.lemur_image, (30, 30), 3)
            self.render_icon(self.book_image, (30, 60), 3)
            self.render_icon(self.skull_image, (90, 30), 3)
            self.render_icon(self.bacteria_image, (90, 60), 3)
            self.render_icon(self.brain_image, (150, 30), 3)

            # Render the text input field
            self.render_text_field()

            # Render the external text field
            self.render_external_text_field()

            # Render the submit button
            self.render_button()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate to 60 FPS
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    #communicator = Communicator()
    #communicator.startGame()

    text_input_screen = TextInputScreen()
    text_input_screen.run_screen()
