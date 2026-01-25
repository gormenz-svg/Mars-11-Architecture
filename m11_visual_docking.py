import numpy as np
import matplotlib.pyplot as plt

class M11VisualEngine:
    def __init__(self, mass=100000, beta_base=0.6):
        self.mass = mass 
        self.beta = beta_base
        self.dt = 0.1
        self.Kp = 1800.0  # Коэффициент тяги
        self.Kd = 5200.0  # Коэффициент демпфирования (сопротивление)
        
        # Списки для хранения данных графика
        self.history = {'pos': [], 'vel': [], 'rs': [], 'time': []}

    def run_simulation(self):
        pos, vel = 50.0, -2.0  # Дистанция 50м, скорость 2м/с к цели
        target_pos = 0.05
        t = 0
        
        print("--- m-11 simulation started ---")
        
        for step in range(800): # Ограничение 80 сек
            noise = np.random.normal(0, 0.04)
            measured_pos = pos + noise
            
            # Расчет Resonance Index (Property 7)
            dynamic_beta = self.beta * (1 + abs(noise))
            rs = 1 / (pos + abs(vel) + (1 - dynamic_beta) + 1e-6)
            
            # PD-Control (Property 8)
            error = target_pos - measured_pos
            thrust = (self.Kp * error) - (self.Kd * vel)
            
            # Physics (Newton's Second Law)
            accel = thrust / self.mass
            vel += accel * self.dt
            pos += vel * self.dt
            t += self.dt
            
            # Запись данных
            self.history['pos'].append(pos)
            self.history['vel'].append(vel)
            self.history['rs'].append(rs)
            self.history['time'].append(t)
            
            if pos <= target_pos:
                print(f"target reached at {t:.1f}s")
                break

        self.plot_results()

    def plot_results(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        plt.subplots_adjust(hspace=0.3)

        # График 1: Траектория сближения
        ax1.plot(self.history['time'], self.history['pos'], color='blue', lw=2)
        ax1.set_ylabel('distance (m)')
        ax1.set_title('m-11 orbital coupling: approach trajectory')
        ax1.grid(True, alpha=0.3)

        # График 2: Профиль скорости
        ax2.plot(self.history['time'], self.history['vel'], color='red', lw=2)
        ax2.set_ylabel('velocity (m/s)')
        ax2.set_title('velocity profile (damping check)')
        ax2.grid(True, alpha=0.3)

        # График 3: Индекс Резонанса (наша уникальная метрика)
        ax3.plot(self.history['time'], self.history['rs'], color='green', lw=2)
        ax3.set_ylabel('rs index')
        ax3.set_xlabel('time (seconds)')
        ax3.set_title('resonance stability (m-11 core metric)')
        ax3.grid(True, alpha=0.3)

        print("displaying telemetry charts...")
        plt.show()

if __name__ == "__main__":
    sim = M11VisualEngine()
    sim.run_simulation()