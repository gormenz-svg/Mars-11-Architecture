import numpy as np
import matplotlib.pyplot as plt

class M11ElectrostaticShield:
    def __init__(self, voltage=5e6): # 5 Million Volts potential
        self.voltage = voltage
        self.k = 8.987e9 # Coulomb constant
        self.proton_charge = 1.6e-19
        self.proton_mass = 1.67e-27

    def simulate_deflection(self, n_particles=40):
        plt.figure(figsize=(10, 6))
        
        # Visualize the ship hull as a charged line
        plt.axvline(x=0, color='gold', lw=5, label='Charged Hull (Positive)')
        
        deflected = 0
        for _ in range(n_particles):
            # Initial position (far away) and high velocity
            pos = np.array([-5.0, np.random.uniform(-3, 3)])
            vel = np.array([20.0, 0.0]) # 20 m/s for visual representation
            
            path = []
            hit = False
            
            for _ in range(200):
                path.append(pos.copy())
                r = np.linalg.norm(pos)
                if r < 0.1: # Collision check
                    hit = True
                    break
                
                # Coulomb Force: F = k * (q1 * q2) / r^2
                # Simplified 1D-repulsion for visualization
                dist_to_hull = abs(pos[0])
                if dist_to_hull < 2.0:
                    force_mag = self.k * (self.proton_charge * 0.01) / (dist_to_hull**2 + 0.1)
                    accel = -force_mag / self.proton_mass # Negative x direction
                    vel[0] += accel * 0.001
                
                pos += vel * 0.01
                if pos[0] < -10 or pos[0] > 5: break

            path = np.array(path)
            if not hit and vel[0] < 0:
                deflected += 1
                plt.plot(path[:,0], path[:,1], 'g-', alpha=0.4)
            else:
                plt.plot(path[:,0], path[:,1], 'r-', alpha=0.2)

        plt.title(f"m-11 breakthrough: electrostatic proton deflection\nEfficiency: {(deflected/n_particles)*100}%")
        plt.legend()
        plt.grid(True, alpha=0.1)
        plt.show()

if __name__ == "__main__":
    shield = M11ElectrostaticShield()
    shield.simulate_deflection()
