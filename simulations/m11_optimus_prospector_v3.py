import numpy as np
import matplotlib.pyplot as plt

class M11GIEPProspector:
    """
    GIEP (Inertial Signal Purification) - Reference Implementation.
    Focus: Multimodal sensor fusion with confidence accumulation.
    """
    def __init__(self):
        self.threshold = 0.80
        self.memory = 0.5 # Starting with neutral bias
        self.alpha = 0.3  # Learning rate (inertia factor)
        self.weights = [0.5, 0.3, 0.2] # GPR, Neutron, Thermal
        self.history = []

    def purification_logic(self, raw_data):
        """
        Core GIEP: Weighted Fusion + Divergence Penalty + Temporal Inertia.
        """
        # 1. Spatial Fusion
        weighted_val = np.average(raw_data, weights=self.weights)
        
        # 2. Coherence Check (Damping)
        divergence = np.std(raw_data)
        damping = max(0.1, 1.0 - (divergence * 0.5)) # GPT fix: no negative damping
        
        instant_confidence = weighted_val * damping
        
        # 3. Temporal Inertia (Property 10: Opora)
        # New value = (1-alpha)*Old + alpha*New
        self.memory = ((1 - self.alpha) * self.memory) + (self.alpha * instant_confidence)
        return self.memory

    def scan_cycle(self, iterations=10):
        print(f"--- GIEP Accumulative Scan Initiated ---")
        for i in range(iterations):
            # Simulate environment (first 4 cycles - noise, then 6 cycles - signal)
            base = 0.85 if i > 4 else 0.4
            raw = [np.random.normal(base, 0.15) for _ in range(3)]
            
            purified = self.purification_logic(raw)
            self.history.append(purified)
            
            status = "STABLE_SIGNAL" if purified > self.threshold else "SCANNING"
            print(f"Cycle {i}: Confidence {purified:.2f} | {status}")

        self.visualize()

    def visualize(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.history, color='cyan', marker='o', lw=2, label='GIEP Purified Confidence')
        plt.axhline(y=self.threshold, color='red', ls='--', label='Drill Threshold')
        plt.fill_between(range(len(self.history)), self.threshold, 1.0, color='green', alpha=0.1, label='Decision Zone')
        plt.title("M-11 Prospector: Accumulative GIEP Logic")
        plt.xlabel("Scan Iterations")
        plt.ylabel("Confidence Level")
        plt.legend()
        plt.grid(alpha=0.2)
        plt.show()

if __name__ == "__main__":
    M11GIEPProspector().scan_cycle()
