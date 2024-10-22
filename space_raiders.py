import tkinter as tk
from PIL import Image, ImageTk
import random
import time

class SpaceInvaders:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        
        # Load and resize images using Pillow
        self.ship_image = Image.open("ship.jpg").resize((60, 60), Image.LANCZOS)  # Larger ship image
        self.ship_image = ImageTk.PhotoImage(self.ship_image)
        
        self.alien_image = Image.open("alien.png").resize((40, 40), Image.LANCZOS)
        self.alien_image = ImageTk.PhotoImage(self.alien_image)
        
        self.ship = self.canvas.create_image(400, 550, image=self.ship_image)
        self.bullets = []
        self.aliens = []
        self.lives = 3
        self.hearts = []
        self.score = 0  # Initialize score
        self.score_text = self.canvas.create_text(400, 20, text=self.score, font=("Arial", 40), fill="white")  # Score display
        self.speed_factor = 0.6  # Initial speed factor
        self.target_fps = 60  # Target frames per second
        self.last_time = time.time()
        self.alien_spawn_timer = 0  # Timer for alien spawning
        self.alien_spawn_interval = 0.4  # Spawn a new alien every 2 seconds
        self.create_aliens()
        self.create_hearts()
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.start_shooting)
        self.root.bind("<KeyRelease-space>", self.stop_shooting)
        
        self.shooting = False

    def create_aliens(self):
        num_aliens = 5  # Reduced number of aliens
        for _ in range(num_aliens):
            self.spawn_alien()

    def spawn_alien(self):
        x = random.randint(50, 750)
        y = random.randint(50, 100)
        alien = self.canvas.create_image(x, y, image=self.alien_image)
        self.aliens.append(alien)

    def create_hearts(self):
        for i in range(self.lives):
            heart = self.canvas.create_text(20 + i * 30, 20, text="❤️", font=("Arial", 20), fill="red")
            self.hearts.append(heart)

    def update_lives(self):
        if self.lives > 0:
            self.lives -= 1
            self.canvas.delete(self.hearts.pop())
        if self.lives == 0:
            self.canvas.create_text(400, 300, text="Game Over", font=("Arial", 50), fill="white")
            self.root.after_cancel(self.game_loop)

    def move_left(self, event):
        self.canvas.move(self.ship, -40, 0)  # Increased move distance

    def move_right(self, event):
        self.canvas.move(self.ship, 40, 0)  # Increased move distance

    def shoot(self):
        if self.shooting:
            bullet = self.canvas.create_rectangle(self.canvas.coords(self.ship)[0] - 5, self.canvas.coords(self.ship)[1] - 40, self.canvas.coords(self.ship)[0] + 5, self.canvas.coords(self.ship)[1] - 20, fill='white')  # Thinner bullet
            self.bullets.append(bullet)
            self.root.after(100, self.shoot)  # Reduced delay for faster shooting

    def start_shooting(self, event):
        if not self.shooting:
            self.shooting = True
            self.shoot()

    def stop_shooting(self, event):
        self.shooting = False

    def move_bullets(self, delta_time):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -400 * delta_time * self.speed_factor)  # Adjusted bullet speed with delta_time
            if self.canvas.coords(bullet)[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

    def move_aliens(self, delta_time):
        for alien in self.aliens[:]:
            self.canvas.move(alien, 0, 80 * delta_time * self.speed_factor)  # Adjusted alien speed with delta_time
            if self.canvas.coords(alien)[1] >= 600:
                self.update_lives()
                self.canvas.delete(alien)
                self.aliens.remove(alien)

    def check_collision(self, bullet, alien):
        bullet_coords = self.canvas.coords(bullet)
        alien_coords = self.canvas.coords(alien)
        if len(bullet_coords) == 4 and len(alien_coords) == 2:
            bullet_x1, bullet_y1, bullet_x2, bullet_y2 = bullet_coords
            alien_x, alien_y = alien_coords
            alien_x1 = alien_x - 20  # Half the width of the alien image
            alien_y1 = alien_y - 20  # Half the height of the alien image
            alien_x2 = alien_x + 20
            alien_y2 = alien_y + 20
            if not (bullet_x2 < alien_x1 or bullet_x1 > alien_x2 or bullet_y2 < alien_y1 or bullet_y1 > alien_y2):
                self.canvas.delete(bullet)
                self.canvas.delete(alien)
                self.bullets.remove(bullet)
                self.aliens.remove(alien)
                self.update_score()  # Update score on kill
                return True
        return False

    def update_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_text, text=self.score)

    def game_loop(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        self.move_bullets(delta_time)
        self.move_aliens(delta_time)
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if self.check_collision(bullet, alien):
                    break

        # Update the alien spawn timer
        self.alien_spawn_timer += delta_time
        if self.alien_spawn_timer >= self.alien_spawn_interval:
            self.spawn_alien()
            self.alien_spawn_timer = 0

        self.speed_factor += 0.002  # Increase speed factor over time
        self.canvas.after(int(1000 / self.target_fps), self.game_loop)  # Run the game loop at target FPS

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceInvaders(root)
    game.game_loop()
    root.mainloop()