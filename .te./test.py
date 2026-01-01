import arcade

WIDTH = 600
HEIGHT = 400
TITLE = "Sound Test"

class SoundTest(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        print("Loading sound...")
        self.music = arcade.load_sound("assets/sound/background-1.ogg")
        self.player = None

    def on_show(self):
        print("Playing sound...")
        self.player = arcade.play_sound(self.music, loop=True, volume=0.4)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Playing Sound",
            WIDTH // 2,
            HEIGHT // 2,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )

# 🔑 IMPORTANT: keep reference
window = SoundTest()

arcade.run()
