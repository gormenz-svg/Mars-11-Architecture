import random
import matplotlib.pyplot as plt

class M11AgenticSwarm:
    def __init__(self, unit_count=15):
        self.unit_count = unit_count
        self.energy = 10.0
        self.integrity = 0.0
        self.history = {'energy': [], 'integrity': [], 'roles': [], 'time': []}
        
        # Initial roles
        self.roles = ["Energy", "Build", "Repair"]
        self.units = [random.choice(self.roles) for _ in range(self.unit_count)]

    def _rebalance_roles(self):
        """
        Property 2 (Wisdom): Swarm intelligence redistribution.
        If energy is low, move units to Energy. If integrity is low, move to Repair.
        """
        energy_units = self.units.count("Energy")
        repair_units = self.units.count("Repair")

        for i in range(len(self.units)):
            if self.energy < 40 and self.units[i] != "Energy" and random.random() > 0.7:
                self.units[i] = "Energy"
            elif self.integrity < self.energy and self.units[i] == "Energy" and self.energy > 60:
                self.units[i] = "Build"
            elif self.integrity < 50 and repair_units < 3:
                if self.units[i] == "Build": self.units[i] = "Repair"

    def run(self, steps=100):
        print(f"--- M-11 AGENTIC SWARM ACTIVE ({self.unit_count} Units) ---")
        
        for t in range(steps):
            # 1. Dynamic Adaptation
            self._rebalance_roles()
            
            # 2. Agentic Leadership (AAB)
            # Leadership bonus is now tied to having a dedicated 'Energy' Lead if energy is low
            lead_bonus = 1.4 if (self.energy < 50 and self.units.count("Energy") > 5) else 1.1

            # 3. Resource Calculation
            n_energy = self.units.count("Energy")
            n_build = self.units.count("Build")
            n_repair = self.units.count("Repair")

            # Physics-based progress
            self.energy = min(100, self.energy + (n_energy * 0.8) - 2.0) # -2.0 is base consumption
            
            if self.energy > 20:
                # Wear and tear vs Repair capacity
                wear = random.uniform(1, 3)
                repair_effect = n_repair * 0.5
                net_damage = max(0, wear - repair_effect)
                
                build_rate = (n_build * 1.2 * lead_bonus)
                self.integrity = min(100, self.integrity + build_rate - net_damage)

            # Telemetry
            self.history['energy'].append(self.energy)
            self.history['integrity'].append(self.integrity)
            self.history['roles'].append(n_energy) # Tracking energy units as proxy for adaptation
            self.history['time'].append(t)

            if self.energy >= 100 and self.integrity >= 100:
                print(f"Mission Success at T+{t}")
                break

        self.visualize()

    def visualize(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        ax1.plot(self.history['time'], self.history['energy'], color='gold', label='Energy (%)')
        ax1.plot(self.history['time'], self.history['integrity'], color='red', label='Base Integrity (%)')
        ax1.set_title("M-11 Swarm: Behavioral Autonomy")
        ax1.legend()
        ax1.grid(True, alpha=0.1)

        ax2.stackplot(self.history['time'], self.history['roles'], labels=['Energy Units Count'], color='cyan', alpha=0.3)
        ax2.set_ylabel("Role Distribution")
        ax2.set_xlabel("Cycles")
        ax2.legend()
        ax2.grid(True, alpha=0.1)
        
        plt.show()

if __name__ == "__main__":
    M11AgenticSwarm().run()
