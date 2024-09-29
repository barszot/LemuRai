import pygame
import sys
from communicating import Communicator

class Window:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        pygame.font.init()  # Initialize fonts
        self.tour_state = 1
        self.communicator = Communicator()
        # Constants
        self.WIDTH, self.HEIGHT = 1200, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.FONT_SIZE = 32

        # Set up the display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Window with Text Fields")

        # Load the images
        self.lemur_image = pygame.image.load("icons/lemur.png")
        self.lemur_image = pygame.transform.scale(self.lemur_image, (32, 32))
        pygame.display.set_icon(self.lemur_image)

        # Font and variables
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.input_texts = ["", "", "", "", ""]  # List to store input texts for multiple fields
        self.input_values = [0, 0, 0, 0, ""]
        self.active_index = 0  # Track which input field is active
        self.external_text = ""
        self.clock = pygame.time.Clock()
        self.button_rect = pygame.Rect(700, 560, 100, 40)

        # Labels for each input field
        self.labels = ["Technologia", "Kultura", "Ochrona", "Zdrowie", "Prompt"]
        self.text_field_offset = 150

        # Yes/No button handling
        self.show_yes_no_buttons = False  # Condition to show buttons
        self.yes_no_value = ""
        self.yes_button = pygame.Rect(500, 500, 100, 40)
        self.no_button = pygame.Rect(650, 500, 100, 40)
        self.adviser_response = ""
        self.king_response = ""
        self.people_response = ""
        self.change_verdict = False

    def render_text_fields(self):
        """Render the text input fields."""
        for i in range(len(self.input_texts)):
            pygame.draw.rect(self.screen, self.WHITE, (30, self.text_field_offset + i * 100, 400, 50), 2)
            text_surface = self.font.render(self.input_texts[i], True, self.WHITE)
            self.screen.blit(text_surface, (35, self.text_field_offset + 10 + i * 100))
            label_surface = self.font.render(self.labels[i], True, self.WHITE)
            self.screen.blit(label_surface, (35, self.text_field_offset - 25 + i * 100))

    def render_button(self):
        """Render the submit button."""
        pygame.draw.rect(self.screen, self.BLUE, self.button_rect)
        small_font = pygame.font.Font(None, 24)
        button_text = small_font.render("Zatwierdź", True, self.WHITE)
        self.screen.blit(button_text, (self.button_rect.x + 11, self.button_rect.y + 11))

    def render_yes_no_buttons(self):
        """Render 'Yes' and 'No' buttons."""
        pygame.draw.rect(self.screen, self.BLUE, self.yes_button)
        pygame.draw.rect(self.screen, self.BLUE, self.no_button)

        small_font = pygame.font.Font(None, 24)
        yes_text = small_font.render("Tak", True, self.WHITE)
        no_text = small_font.render("Nie", True, self.WHITE)
        self.screen.blit(yes_text, (self.yes_button.x + 35, self.yes_button.y + 10))
        self.screen.blit(no_text, (self.no_button.x + 35, self.no_button.y + 10))

    def handle_submit(self):
        """Handle text submission."""
        sum_of_expense = 0
        for ix, text in enumerate(self.input_texts):
            if ix < 4:
                if text.strip() == "":
                    self.input_values[ix] = 0
                elif text.strip().isdigit():
                    inted_text = int(text.strip())
                    if inted_text < 0:
                        self.throw_error("Nie wolno podawać ujemnych liczb!")
                        return
                    else:
                        self.input_texts[ix] = str(inted_text)
                        self.input_values[ix] = inted_text
                        sum_of_expense += inted_text
                else:
                    self.throw_error("Należy podać całkowite nieujemne liczby!")
                    return

            if sum_of_expense > self.communicator.state.coins:
                self.throw_error("Nie ma tyle pieniędzy na taki wydatek!")
                return
            elif ix == 4:
                self.input_values[ix] = text

        data = {
            "verdict": self.input_values[4],
            "expense": {
                "technologia": self.input_values[0],
                "kultura": self.input_values[1],
                "ochrona": self.input_values[2],
                "szpitale": self.input_values[3]
            }
        }

        com_result = self.communicator.gameStep(True, data)
        self.adviser_response = com_result["adviser_response"]
        print(self.adviser_response)

        # Activate Yes/No buttons based on adviser response
        self.show_yes_no_buttons = True

    def handle_yes(self):
        """Handle 'Yes' button click."""
        print("Wybrano TAK")
        self.show_yes_no_buttons = False
        self.yes_no_value = "tak"
        self.process_verdict()

    def handle_no(self):
        """Handle 'No' button click."""
        print("Wybrano NIE")
        self.show_yes_no_buttons = False
        self.yes_no_value = "nie"
        self.process_verdict()

    def process_verdict(self):
        """Process the verdict based on Yes/No response."""
        if self.yes_no_value == "tak":
            self.change_verdict = True
        else:
            self.change_verdict = False

        if self.change_verdict:
            # Reset input fields after a "Tak" response
            self.input_texts = ["", "", "", "", ""]
            self.input_values = [0, 0, 0, 0, ""]
        else:
            # Get further responses after a "Nie" response
            data = {
                "verdict": self.input_values[4],
                "expense": {
                    "technologia": self.input_values[0],
                    "kultura": self.input_values[1],
                    "ochrona": self.input_values[2],
                    "szpitale": self.input_values[3]
                }
            }
            com_result = self.communicator.gameStep(False, data)
            self.king_response = com_result["king_response"]
            self.people_response = com_result["people_response"]
            print(self.king_response)
            print(self.people_response)
            # Reset input fields after the verdict processing
            self.input_texts = ["", "", "", "", ""]
            self.input_values = [0, 0, 0, 0, ""]

    def throw_error(self, message):
        """Display error messages."""
        print(f"Błąd: {message}")

    def run(self):
        """Main loop of the game."""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.handle_submit()
                    elif self.show_yes_no_buttons:
                        if self.yes_button.collidepoint(event.pos):
                            self.handle_yes()
                        elif self.no_button.collidepoint(event.pos):
                            self.handle_no()
                    else:
                        # Check if clicked inside any of the text fields
                        for i in range(len(self.input_texts)):
                            if 30 <= event.pos[0] <= 430 and (self.text_field_offset + i * 100) <= event.pos[1] <= (self.text_field_offset + 50 + i * 100):
                                self.active_index = i

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_texts[self.active_index] = self.input_texts[self.active_index][:-1]
                    elif event.key == pygame.K_RETURN:
                        self.handle_submit()
                    else:
                        if self.active_index < len(self.input_texts):
                            self.input_texts[self.active_index] += event.unicode

            # Fill the screen with black
            self.screen.fill(self.BLACK)

            # Render text fields and buttons
            self.render_text_fields()
            self.render_button()

            # Show Yes/No buttons if active
            if self.show_yes_no_buttons:
                self.render_yes_no_buttons()

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    window = Window()
    window.run()
