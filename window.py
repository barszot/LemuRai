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
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 180, 0)  # Dodaj ten wiersz
        self.RED = (180, 0, 0)  # Dodaj ten wiersz

        self.FONT_SIZE = 32
        self.verdict_prompt = "Czy chcesz zmienić decyzję?"

        # Set up the display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Window with Text Fields")

        # Load the images
        self.lemur_image = pygame.image.load("icons/lemur.png")
        self.lemur_image = pygame.transform.scale(self.lemur_image, (32, 32))
        pygame.display.set_icon(self.lemur_image)


        # Load the other images
        self.book_image = pygame.image.load("icons/book.png")
        self.skull_image = pygame.image.load("icons/skull.png")
        self.bacteria_image = pygame.image.load("icons/bacteria.png")
        self.brain_image = pygame.image.load("icons/brain.png")
        self.backgroud_image = pygame.image.load("assets/background.png")
        self.culture1 = pygame.image.load("assets/culture1.png")
        self.culture2 = pygame.image.load("assets/culture2.png")
        self.culture3 = pygame.image.load("assets/culture3.png")
        self.hospital1 = pygame.image.load("assets/hospital1.png")
        self.hospital2 = pygame.image.load("assets/hospital2.png")
        self.hospital3 = pygame.image.load("assets/hospital3.png")
        self.hospital4 = pygame.image.load("assets/hospital4.png")
        self.lemurraw = pygame.image.load("assets/lemurraw.png")
        self.lemursick = pygame.image.load("assets/lemursick.png")
        self.technology1 = pygame.image.load("assets/technology1.png")
        self.technology2 = pygame.image.load("assets/technology2.png")
        self.technology3 = pygame.image.load("assets/technology3.png")

        self.coin_image = pygame.image.load("icons/coin.png")
        self.defense_image = pygame.image.load("icons/defense.png")
        self.hospitals_image = pygame.image.load("icons/hospitals.png")

        # Font and variables
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.input_texts = ["", "", "", "", ""]  # List to store input texts for multiple fields
        self.input_values = [0, 0, 0, 0, ""]
        self.active_index = 4  # Track which input field is active
        self.external_text = ""
        self.clock = pygame.time.Clock()
        self.button_rect = pygame.Rect(self.WIDTH - 150, self.HEIGHT - 115, 100, 40)  # Obniżenie przycisku "Zatwierdź"
        self.yes_button = pygame.Rect(850, 550, 100, 40)    # Obniżenie przycisku "Tak"
        self.no_button = pygame.Rect(980, 550, 100, 40)     # Obniżenie przycisku "Nie"

            
        # Labels for each input field
        self.labels = ["Technologia", "Kultura", "Ochrona", "Szpitale", "Wiadomość do Doradcy"]
        self.text_field_offset = 150

        # Yes/No button handling
        self.show_yes_no_buttons = False  # Condition to show buttons
        self.yes_no_value = ""


        self.adviser_response = ""
        self.people_response = ""
        self.error_response = ""
        self.change_verdict = False
        self.prompt_scroll_offset = 0  # Add this in __init__
        self.scroll_offset = 0  # Nowa zmienna do śledzenia przewinięcia tekstu
        self.scroll_speeds = 1  # Ustaw wartość numeryczną
        self.text_widths = {
            "adviser": 0,
            "people": 0,
        }

    def render_icon(self, icon, icon_position, count):
        small_image = pygame.transform.scale(icon, (30, 30))
        self.screen.blit(small_image, icon_position)
        number_surface = self.font.render(str(count), True, self.WHITE)
        self.screen.blit(number_surface, (icon_position[0] + 40, icon_position[1] + 5))

    def render_text_fields(self):
        """Render the text input fields with adjusted widths."""
        for i in range(len(self.input_texts)):
            width = 100 if i < 4 else self.WIDTH - 200  # Set width to 100 for the first four fields
            

            # Determine the text to display based on the field
            if i == 4:  # Special handling for the prompt field
                pygame.draw.rect(self.screen, self.WHITE, (30, self.HEIGHT - 120, width, 50), 2)
                text_to_display = self.input_texts[i][self.scroll_offset:]  # Apply scroll offset
                # Truncate text if it exceeds the width of the rectangle
                text_surface = self.font.render(text_to_display, True, self.WHITE)
                max_text_width = width - 10  # Leave some padding
                if text_surface.get_width() > max_text_width:
                    # Only show the last part of the text if it's too long
                    text_to_display = text_to_display[-max_text_width // self.font.size('a')[0]:]
                text_surface = self.font.render(text_to_display, True, self.WHITE)
                self.screen.blit(text_surface, (35, self.HEIGHT - 115))
                label_surface = self.font.render(self.labels[i], True, self.WHITE)
                self.screen.blit(label_surface, (35, self.HEIGHT - 145))
            else:
                pygame.draw.rect(self.screen, self.WHITE, (30, self.text_field_offset + i * 100, width, 50), 2)
                text_to_display = self.input_texts[i]
                text_surface = self.font.render(text_to_display, True, self.WHITE)
                self.screen.blit(text_surface, (35, self.text_field_offset + 10 + i * 100))
                label_surface = self.font.render(self.labels[i], True, self.WHITE)
                self.screen.blit(label_surface, (35, self.text_field_offset - 25 + i * 100))
            

    def render_background(self, game_state):
        # Load the background image
        background_image = self.backgroud_image

        # Get the display dimensions
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h

        # Calculate the maximum size for the background image
        max_width = (display_width * 3 ) // 4  # Use half the display width
        max_height = display_height  # Use the full display height

        # Get the size of the background image
        image_width, image_height = background_image.get_size()

        # Calculate the scale factor to fit the image within the maximum size
        scale_factor = min(max_width / image_width, max_height / image_height)

        # Resize the image
        background_image = pygame.transform.smoothscale(background_image, (int(image_width * scale_factor), int(image_height * scale_factor)))

        # Draw the background image on the right side of the screen
        self.screen.blit(background_image, (display_width - background_image.get_width(), 0))

        # Depending on the game state, draw different sprites
        if game_state == 'state1':
            sprite_image = self.lemurraw
        elif game_state == 'state2':
            sprite_image = self.lemursick
        # Add more states as needed...

        # Draw the sprite on top of the background
        self.screen.blit(sprite_image, (display_width - background_image.get_width(), 0))


    def render_scrolling_text(self, text, position, color):
        text = "           " + text.replace("\n", " ")

        """Render scrolling text with a background color."""
        # Drawing the background for the text
        background_rect = pygame.Rect(0, position[1], self.WIDTH, 50)  # Full width background
        pygame.draw.rect(self.screen, color, background_rect)

        # Create the text surface
        text_surface = self.font.render(text, True, self.WHITE)
        text_width = text_surface.get_width()
        text_x_position = position[0] - self.scroll_offset

        # Scroll the text
        self.scroll_offset += self.scroll_speeds  # Increase offset

        # Reset scrolling when text goes off the screen
        if self.scroll_offset > text_width + self.WIDTH:
            self.scroll_offset = 0

        # Display the text
        self.screen.blit(text_surface, (text_x_position, position[1] + 10))

    def render_responses(self):
        """Render responses for adviser and people."""
        bottom_position = (0, self.screen.get_height() - 50)  # Move to the bottom of the screen
        self.scroll_speeds = 1
        if self.error_response:
            error_text = f"BŁĄD: {self.error_response}"
            self.scroll_speeds = 0
            self.render_scrolling_text(error_text, bottom_position, self.RED)
        # Render adviser response
        elif self.adviser_response:
            adviser_text = f"Doradca: {self.adviser_response}"
            self.render_scrolling_text(adviser_text, bottom_position, self.BLUE)

        # Render people's response
        elif self.people_response:
            people_text = f"Lemury: {self.people_response}"
            self.render_scrolling_text(people_text, bottom_position, self.GREEN)  # Dark green color



    def render_button(self):
        """Render the submit button."""
        pygame.draw.rect(self.screen, self.BLUE, self.button_rect)
        small_font = pygame.font.Font(None, 24)
        button_text = small_font.render("Wyślij", True, self.WHITE)
        self.screen.blit(button_text, (self.button_rect.x + 25, self.button_rect.y + 11))

    def render_yes_no_buttons(self):
        """Render 'Yes' and 'No' buttons with a border and a prompt."""
        # Draw the border around the buttons
        border_rect = pygame.Rect(self.yes_button.x - 10, self.yes_button.y - 30, 
                                self.no_button.x + self.no_button.width - (self.yes_button.x - 10) + 20, 
                                self.no_button.height + 50)
        pygame.draw.rect(self.screen, self.WHITE, border_rect, 2)  # White border

        # Draw the prompt above the buttons
        prompt_surface = self.font.render(self.verdict_prompt, True, self.WHITE)
        prompt_position = (border_rect.x + 10, border_rect.y - 30)
        self.screen.blit(prompt_surface, prompt_position)

        # Draw the buttons
        pygame.draw.rect(self.screen, self.BLUE, self.yes_button)
        pygame.draw.rect(self.screen, self.BLUE, self.no_button)

        small_font = pygame.font.Font(None, 24)
        yes_text = small_font.render("Tak", True, self.WHITE)
        no_text = small_font.render("Nie", True, self.WHITE)
        self.screen.blit(yes_text, (self.yes_button.x + 35, self.yes_button.y + 10))
        self.screen.blit(no_text, (self.no_button.x + 35, self.no_button.y + 10))


    def handle_submit(self):
        """Handle text submission."""
        self.error_response = ""
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
        self.scroll_offset = 0

        self.adviser_response = com_result["adviser_response"]

        # Activate Yes/No buttons based on adviser response
        self.show_yes_no_buttons = True

    def handle_yes(self):
        """Handle 'Yes' button click."""
        self.show_yes_no_buttons = False
        self.yes_no_value = "tak"
        self.adviser_response = ""
        self.input_texts[4] = ""  # Reset prompt field after accepting
        self.input_values[4] = ""  # Reset prompt field after accepting

        self.process_verdict()
        self.active_index = 4  # Focus on the prompt field again


    def handle_no(self):
        """Handle 'No' button click."""
        self.show_yes_no_buttons = False
        self.yes_no_value = "nie"
        self.adviser_response = ""
        self.input_texts[4] = ""  # Reset prompt field after accepting
        self.input_values[4] = ""  # Reset prompt field after accepting

        self.process_verdict()
        self.active_index = 4  # Focus on the prompt field

    def process_verdict(self):
        """Process the verdict based on Yes/No response."""
        if self.yes_no_value == "tak":
            self.change_verdict = True
        else:
            self.change_verdict = False
        self.yes_no_value = ""
        if self.change_verdict:
            # Reset input fields after a "Tak" response
            self.input_texts = ["", "", "", "", ""]  # Reset all fields
            self.input_values = [0, 0, 0, 0, ""]
            self.active_index = 4  # Focus on the prompt field

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
            self.adviser_response = ""
            self.people_response = com_result["people_response"]
            self.scroll_offset = 0

            # Reset for a new round
            self.input_texts = ["", "", "", "", ""]  # Reset all fields for the next round
            self.input_values = [0, 0, 0, 0, ""]
            self.active_index = 4  # Focus on the prompt field for the next round


    def throw_error(self, message):
        """Display error messages."""
        self.error_response = message

    def run(self):
        """Main loop of the game."""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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
                            if i == 4:
                                if 30 <= event.pos[0] <= 430 and (self.HEIGHT - 130)  <= event.pos[1] <= (self.HEIGHT - 80):
                                    self.active_index = i
                            else:
                                if 30 <= event.pos[0] <= 430 and (self.text_field_offset + i * 100) <= event.pos[1] <= (self.text_field_offset + 50 + i * 100):
                                    self.active_index = i

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_texts[self.active_index] = self.input_texts[self.active_index][:-1]

                    else:
                        if self.active_index < 5:
                            self.input_texts[self.active_index] += event.unicode

            # Fill the screen with black
            self.screen.fill(self.BLACK)

            self.render_icon(self.lemur_image, (30, 20), self.communicator.state.population.population)
            self.render_icon(self.coin_image, (30, 50), self.communicator.state.coins)
            self.render_icon(self.defense_image, (140, 20), self.communicator.state.defense)
            self.render_icon(self.hospitals_image, (140, 50), self.communicator.state.hospitals)
            self.render_icon(self.book_image, (230, 20), self.communicator.state.culture)
            self.render_icon(self.brain_image, (230, 50), self.communicator.state.technology)
            if (self.communicator.state.population.is_epidemy):
                self.render_icon(self.bacteria_image, (30, 80), self.communicator.state.population.sick)
                self.render_icon(self.skull_image, (140, 80), self.communicator.state.population.dead)
                epidemic_text = self.font.render("Epidemia", True, (210, 80,10))
                self.screen.blit(epidemic_text, (230, 80))
            if (self.communicator.state.population.is_plague):
                self.render_icon(self.skull_image, (140, 80), self.communicator.state.population.dead)
                plague_text = self.font.render("Kataklizm", True, (210, 80,10))
                self.screen.blit(plague_text, (230, 80))

            self.render_text_fields()
            self.render_button()
            self.render_responses()
            # Show Yes/No buttons if active
            if self.show_yes_no_buttons:
                self.render_yes_no_buttons()
            # Render icons

            # Render the background
            self.render_background("state1")

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

