import numpy as np
import matplotlib.pyplot as plt

class M11SmartShield:
    def __init__(self):
        self.energy_bank = 100.0  # Percentage
        self.solar_input = 0.5    # Constant recharge from panels
        self.history = {'energy': [], 'flux': [], 'threats': [], 'time': []}
        self.prev_flux = 50.0

    def analyze_threat(self, current_flux):
        """
        Property 4 (Comprehension): Delta-based prediction.
        Detects spikes before they reach critical levels.
        """
        delta = current_flux - self.prev_flux
        self.prev_flux = current_flux
        
        # Threat if flux is high OR if it's rising too fast (Predictive Logic)
        is_threat = (current_flux > 80) or (delta > 15)
        return is_threat, delta

    def run_simulation(self, duration=60):
        print("--- m-11 phase III: smart pulse shield active ---")
        
        for t in range(duration):
            # Simulate fluctuating solar environment
            flux = 50 + np.random.normal(0, 5)
            if t in range(20, 30): flux += (t - 15) * 5  # Simulated Solar Flare spike
            
            is_threat, delta = self.analyze_threat(flux)
            
            # Energy Logic (Property 7: Balance)
            cost = 0
            if is_threat:
                # Pulse cost scales with flux intensity
                cost = (flux / 20) 
                self.energy_bank -= cost
            
            # Property 11: Realization (Constant recharge)
            self.energy_bank = min(100.0, self.energy_bank + self.solar_input)
            
            # Record telemetry
            self.history['energy'].append(self.energy_bank)
            self.history['flux'].append(flux)
            self.history['threats'].append(100 if is_threat else 0)
            self.history['time'].append(t)

        self.plot_telemetry()

    def plot_telemetry(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Plot 1: Solar Flux & Prediction Threshold
        ax1.plot(self.history['time'], self.history['flux'], color='orange', label='Solar Flux (p/cm²)')
        ax1.fill_between(self.history['time'], self.history['threats'], color='red', alpha=0.2, label='Shield Active (Pulse)')
        ax1.set_ylabel('Radiation Intensity')
        ax1.set_title('M-11 Predictive Response: Flux vs Shield Activation')
        ax1.legend()
        ax1.grid(True, alpha=0.2)

        # Plot 2: Energy Bank Management
        ax2.plot(self.history['time'], self.history['energy'], color='cyan', lw=2, label='Battery Level (%)')
        ax2.axhline(y=20, color='red', linestyle='--', alpha=0.5, label='Critical Reserve')
        ax2.set_ylabel('Energy Bank (%)')
        ax2.set_xlabel('Mission Time (seconds)')
        ax2.set_title('Property 7 & 8: Energy Balance & Resilience')
        ax2.legend()
        ax2.grid(True, alpha=0.2)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    m11 = M11SmartShield()
    m11.run_simulation()
