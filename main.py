from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Insect movement speed
INSECT_SPEED = 2.5

# Game modes
MODES = ["Classic", "Timed", "Endless", "Challenge"]
current_mode = 0  # Default mode: Classic

class Insect(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = random.choice(["fly.png", "bee.png", "butterfly.png"])  # Load different insects
        self.size_hint = (None, None)
        self.size = (80, 80)  # Insect size
        self.pos = (random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100))
        self.move_insect()

    def move_insect(self):
        """Animate insect movement with Kivy's Animation system."""
        new_x = random.randint(50, SCREEN_WIDTH - 100)
        new_y = random.randint(50, SCREEN_HEIGHT - 100)
        anim = Animation(x=new_x, y=new_y, duration=random.uniform(1, 3))
        anim.start(self)
        anim.bind(on_complete=lambda *args: self.move_insect())  # Loop animation

class CatGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Background color (Bluey-inspired gradient)
        self.bg = Image(source="background.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        # Score Label
        self.score = 0
        self.score_label = Label(text="Score: 0", font_size=40, color=(1, 1, 1, 1), pos=(20, SCREEN_HEIGHT - 60))
        self.add_widget(self.score_label)

        # Game Mode Label
        self.mode_label = Label(text=f"Mode: {MODES[current_mode]}", font_size=30, color=(1, 1, 1, 1), pos=(20, SCREEN_HEIGHT - 100))
        self.add_widget(self.mode_label)

        # Load sound
        self.catch_sound = SoundLoader.load("catch.wav")

        # Add insects
        self.insects = [Insect() for _ in range(5)]
        for insect in self.insects:
            self.add_widget(insect)

        # Start game loop
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        """Game loop - Handles score updates and animations."""
        if MODES[current_mode] == "Timed":
            # Implement timer logic if needed
            pass

    def on_touch_down(self, touch):
        """Detects taps on insects and updates score."""
        for insect in self.insects:
            if insect.collide_point(*touch.pos):
                self.score += 10
                self.score_label.text = f"Score: {self.score}"
                if self.catch_sound:
                    self.catch_sound.play()
                
                # Respawn insect at a new location
                insect.pos = (random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100))

    def switch_mode(self):
        """Switch between game modes when needed."""
        global current_mode
        current_mode = (current_mode + 1) % len(MODES)
        self.mode_label.text = f"Mode: {MODES[current_mode]}"
        self.score = 0  # Reset score

class CatGameApp(App):
    def build(self):
        return CatGame()

# Run the game
if __name__ == "__main__":
    CatGameApp().run()
