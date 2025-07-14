import pygame
import sys
import random

FPS = 60
WIDTH, HEIGHT = 1920, 1080

BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GROUND_COLOR = (34, 139, 34)

ROCKET_MASS = 500

class RocketEngine:
    def __init__(self, air_mass, fuel_mass):
        self.air_mass = air_mass
        self.fuel_mass = fuel_mass
        self.thrust = 0

    def compress_air(self):
        self.air_mass *= 0.8

    def burn_fuel(self):
        if self.fuel_mass > 0:
            energy_released = self.fuel_mass * 42000
            self.thrust = energy_released / 1000
            self.fuel_mass -= self.fuel_mass * 0.1
        else:
            self.thrust = 0

    def expel_gases(self):
        return f"Выброс газов с тягою {self.thrust:.2f} Н"

def draw_rocket(screen, center_x, center_y):
    pygame.draw.rect(screen, GRAY, (center_x - 25, center_y - 100, 50, 200))
    pygame.draw.polygon(screen, DARK_GRAY, [(center_x - 25, center_y - 100),
                                            (center_x, center_y - 150),
                                            (center_x + 25, center_y - 100)])
    pygame.draw.circle(screen, BLUE, (center_x, center_y - 30), 15)

    pygame.draw.polygon(screen, DARK_GRAY, [(center_x - 25, center_y + 50),
                                            (center_x - 50, center_y + 100),
                                            (center_x - 25, center_y + 100)])
    pygame.draw.polygon(screen, DARK_GRAY, [(center_x + 25, center_y + 50),
                                            (center_x + 50, center_y + 100),
                                            (center_x + 25, center_y + 100)])

def draw_exhaust(screen, center_x, center_y):
    for _ in range(20):
        size = random.randint(3, 8)
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(0, 30)
        color = random.choice([ORANGE, YELLOW])
        pygame.draw.circle(screen, color, (center_x + offset_x, center_y + offset_y + 100), size)

def draw_ground(screen, ground_y):
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, WIDTH, HEIGHT - ground_y))

def main(air_mass, fuel_mass):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Симуляция ракеты с реалистичной высотой")

    engine = RocketEngine(air_mass, fuel_mass)

    velocity = 0
    altitude = 0
    gravity = 9.81
    thrust_force = 0

    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    ground_y = HEIGHT - 100

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_RETURN:
                    engine.compress_air()
                    engine.burn_fuel()
                    thrust_force = engine.thrust
                    print(engine.expel_gases())
                else:
                    thrust_force = 0

        rocket_mass = ROCKET_MASS + engine.fuel_mass
        net_force = thrust_force - (rocket_mass * gravity)
        acceleration = net_force / rocket_mass
        velocity += acceleration * dt
        altitude += velocity * dt

        if altitude <= 0:
            altitude = 0
            velocity = 0
            thrust_force = 0

        screen.fill(BLACK)

        draw_ground(screen, int(ground_y))
        draw_rocket(screen, center_x, center_y)

        if thrust_force > 0:
            draw_exhaust(screen, center_x, center_y + 100)

        font = pygame.font.Font(None, 48)
        height_surface = font.render(f"Высота: {int(max(altitude, 0))} м", True, WHITE)
        velocity_surface = font.render(f"Скорость: {velocity:.2f} м/с", True, WHITE)
        acceleration_surface = font.render(f"Ускорение: {acceleration:.2f} м/с²", True, WHITE)
        thrust_surface = font.render(f"Тяга: {thrust_force:.2f} Н", True, WHITE)
        air_mass_surface = font.render(f"Масса воздуха: {engine.air_mass:.2f} кг", True, WHITE)
        fuel_mass_surface = font.render(f"Масса топлива: {engine.fuel_mass:.2f} кг", True, WHITE)

        screen.blit(height_surface, (50, 50))
        screen.blit(velocity_surface,(50 ,100))
        screen.blit(acceleration_surface,(50 ,150))
        screen.blit(thrust_surface,(50 ,200))
        screen.blit(air_mass_surface,(50 ,250))
        screen.blit(fuel_mass_surface,(50 ,300))

        print(f"Высота: {int(altitude)} м")
        print(f"Скорость: {velocity:.2f} м/с")
        print(f"Ускорение: {acceleration:.2f} м/с²")
        print(f"Тяга: {thrust_force:.2f} Н")
        print(f"Масса воздуха: {engine.air_mass:.2f} кг")
        print(f"Масса топлива: {engine.fuel_mass:.2f} кг")
        print("-" * 40)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    try:
        air_mass_input = float(input("Введите массу воздуха (кг): "))
        fuel_mass_input = float(input("Введите массу топлива (кг): "))

        if air_mass_input <= 0 or fuel_mass_input <= 0:
            print("Масса воздуха и топлива должны быть положительными числами.")
        else:
            main(air_mass_input,fuel_mass_input)

    except ValueError:
        print("Пожалуйста , введите корректные числовые значения.")
