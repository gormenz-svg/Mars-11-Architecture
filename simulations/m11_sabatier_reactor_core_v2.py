import numpy as np
import matplotlib.pyplot as plt

class M11SabatierController:
    """
    Advanced Sabatier Reactor Control (Engineering v2).
    Includes thermal stabilization, energy consumption, and catalyst degradation.
    """
    def __init__(self):
        self.temp = 20.0
        self.target_temp = 350.0
        self.methane_total = 0.0
        self.energy_overhead = 12.0 # Power needed just to stay online
        self.catalyst_health = 1.0  # 1.0 = perfect
        self.history = {'time': [], 'temp': [], 'ch4': [], 'energy': []}

    def simulate_day(self, cycles=24):
        print(f"--- M-11 ISRU REACTOR: 24h OPERATIONAL CYCLE ---")
        
        current_energy = 0
        for t in range(cycles):
            # 1. Solar Curve (Input Energy)
            solar_input = 100 * np.sin(np.pi * t / cycles) if 0 < t < cycles else 0
            current_energy = max(0, solar_input)
            
            # 2. Reactor Logic
            status = "IDLE"
            yield_rate = 0
            
            if current_energy > 30: # Minimum power to operate
                status = "ACTIVE"
                # Heating logic with limit (Property 6: Constraint)
                if self.temp < self.target_temp:
                    self.temp += 25.0
                else:
                    self.temp = self.target_temp + np.random.normal(0, 5) # Thermal noise

                # Sabatier Production (Efficiency depends on Temp & Catalyst)
                temp_efficiency = 1.0 if self.temp > 300 else (self.temp / 300)
                yield_rate = 5.0 * temp_efficiency * self.catalyst_health
                
                # Consuming energy based on production
                energy_cost = yield_rate * 8.0 + self.energy_overhead
                current_energy = max(0, current_energy - energy_cost)
                
                self.methane_total += yield_rate
                # Random catalyst wear (Entropy)
                if np.random.random() < 0.05:
                    self.catalyst_health -= 0.01

            # Log Telemetry
            self.history['time'].append(t)
            self.history['temp'].append(self.temp)
            self.history['ch4'].append(self.methane_total)
            self.history['energy'].append(current_energy)

        self.visualize()

    def visualize(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        ax1.plot(self.history['time'], self.history['temp'], color='coral', lw=2, label='Reactor Temp (°C)')
        ax1.axhline(y=self.target_temp, color='red', ls='--', alpha=0.5, label='Optimal Threshold')
        ax1.set_ylabel("Temperature")
        ax1.legend()
        ax1.grid(alpha=0.2)

        ax2.bar(self.history['time'], self.history['energy'], color='gold', alpha=0.3, label='Net Energy Surplus')
        ax2.step(self.history['time'], self.history['ch4'], color='lime', where='post', label='Methane Stock (kg)')
        ax2.set_ylabel("Resources / Energy")
        ax2.set_xlabel("Martian Hours (Sol)")
        ax2.legend()
        ax2.grid(alpha=0.2)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    M11SabatierController().simulate_day()
