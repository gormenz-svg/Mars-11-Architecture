import numpy as np
import matplotlib.pyplot as plt

class M11RadiationShield:
    def __init__(self, magnetic_strength=5.0):
        self.B_field = magnetic_strength  # Тесла (сила поля)
        self.dt = 0.001
        self.particles_deflected = 0
        self.particles_hit = 0

    def simulate_particle(self):
        # Начальные условия: частица (протон) летит в сторону корабля
        # Позиция [x, y], Скорость [vx, vy]
        pos = np.array([-10.0, np.random.uniform(-5, 5)]) 
        vel = np.array([50.0, 0.0]) # Очень высокая скорость
        charge = 1.6e-19
        mass = 1.67e-27
        
        path = []
        for _ in range(500):
            path.append(pos.copy())
            
            # Магнитное поле активно только в зоне x > -2 и x < 2 (вокруг корабля)
            if -2 < pos[0] < 2 and -2 < pos[1] < 2:
                # Сила Лоренца: F = q(v x B). В 2D это упрощенно:
                force = charge * vel[0] * self.B_field
                accel = force / mass
                vel[1] += accel * self.dt # Отклонение по вертикали
            
            pos += vel * self.dt
            
            # Проверка столкновения с корпусом (x=0, y от -1 до 1)
            if abs(pos[0]) < 0.1 and abs(pos[1]) < 1.0:
                self.particles_hit += 1
                return np.array(path), False
            
            if pos[0] > 5: # Частица пролетела мимо
                self.particles_deflected += 1
                return np.array(path), True
        return np.array(path), False

    def run_shield_test(self, n_particles=50):
        plt.figure(figsize=(10, 6))
        # Рисуем корпус корабля
        plt.gca().add_patch(plt.Rectangle((-0.2, -1), 0.4, 2, color='grey', label='starship hull'))
        
        for _ in range(n_particles):
            path, deflected = self.simulate_particle()
            color = 'green' if deflected else 'red'
            plt.plot(path[:,0], path[:,1], color=color, alpha=0.3)

        plt.title(f"m-11 phase III: active magnetic shielding test\nDeflected: {self.particles_deflected} | Hits: {self.particles_hit}")
        plt.xlabel("distance x")
        plt.ylabel("deflection y")
        plt.grid(True, alpha=0.2)
        print(f"shield efficiency: {(self.particles_deflected/n_particles)*100:.1f}%")
        plt.show()

if __name__ == "__main__":
    shield = M11RadiationShield(magnetic_strength=10.0) # Увеличь силу, чтобы увидеть отклонение
    shield.run_shield_test()
