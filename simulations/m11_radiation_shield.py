import numpy as np
import matplotlib.pyplot as plt

class M11UltimateElectrostatic:
    def __init__(self, voltage=1e8): # 100 Megavolts (NASA conceptual level)
        self.voltage = voltage
        self.k = 8.987e9
        self.q_p = 1.602e-19  # Proton charge (C)
        self.m_p = 1.672e-27  # Proton mass (kg)
        self.c = 3e8          # Speed of light
        
        # Calculate Hull Charge Q based on V = kQ/R (Assuming hull radius R=4.5m)
        self.R_hull = 4.5
        self.Q_hull = (self.voltage * self.R_hull) / self.k

    def run_simulation(self, n_particles=50):
        plt.figure(figsize=(12, 7))
        
        # Drawing the Starship Hull (The "Charged Node")
        hull_x = 0
        plt.axvline(x=hull_x, color='gold', lw=8, label='Starship Charged Hull (100MV)', alpha=0.7)
        
        # High-speed solar protons (10% of speed of light)
        v0 = 0.1 * self.c 
        dt = 1e-9 # Nanosecond steps for high-speed physics
        
        deflected_count = 0
        
        for _ in range(n_particles):
            # Initial position: 20m away, random y-offset
            pos = np.array([-20.0, np.random.uniform(-10, 10)])
            vel = np.array([v0, 0.0])
            
            path = []
            hit = False
            
            for _ in range(1000):
                path.append(pos.copy())
                
                # Vector distance to hull
                r_vec = pos - np.array([hull_x, pos[1]]) # Simplification to x-axis repulsion
                r_mag = abs(r_vec[0])
                
                if r_mag < 0.1: # Collision check
                    hit = True
                    break
                
                # Coulomb Force: F = k * (q1 * q2) / r^2
                force_x = (self.k * self.Q_hull * self.q_p) / (r_mag**2)
                
                # Acceleration: a = F / m
                accel_x = -force_x / self.m_p # Repelling from hull
                
                # Update velocity and position
                vel[0] += accel_x * dt
                pos += vel * dt
                
                # Stop if particle is far away
                if pos[0] < -30 or pos[0] > 10: break

            path = np.array(path)
            # Determine success: if particle reversed direction
            if not hit and vel[0] < 0:
                deflected_count += 1
                plt.plot(path[:,0], path[:,1], 'g-', alpha=0.4)
            else:
                plt.plot(path[:,0], path[:,1], 'r-', alpha=0.2)

        efficiency = (deflected_count / n_particles) * 100
        plt.title(f"m-11 phase III: relativistic proton deflection\nVoltage: {self.voltage/1e6:.0f}MV | Efficiency: {efficiency:.1f}%")
        plt.xlabel("distance to hull (meters)")
        plt.ylabel("deflection spread")
        plt.grid(True, alpha=0.1)
        plt.show()

if __name__ == "__main__":
    # Property 9 (Hardening): Testing 100MV shield against 0.1c protons
    sim = M11UltimateElectrostatic()
    sim.run_simulation()
