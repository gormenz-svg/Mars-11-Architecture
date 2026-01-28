"""
MARS-11: Master Mission Controller (Executive Layer)
--------------------------------------------------
Orchestration script for autonomous Martian base operations.
Integrated Layers: Robotics, ISRU, Radiation, Visual LAM, Bio-Regen, and Cognitive Filtering.
"""

import sys
import os
import time
import random

# Adding the project root to sys.path for cross-folder imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing the specific modules from /modules/
try:
    from modules.m11_radiation_shield import RadiationShield
    from modules.m11_optimus_agentic_swarm import OptimusSwarm
    from modules.m11_optimus_prospector_v3 import M11GIEPProspector
    from modules.m11_sabatier_reactor_core_v2 import M11SabatierController
    from modules.m11_visual_docking import VisualDocking
    from modules.m11_visual_action_lam import VisualLAMAgent
    from modules.m11_gnosis_purifier import GnosisPurifier
    from modules.m11_bio_regen_logic import BioRegenSystem
except ImportError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    sys.exit(1)

class MarsBaseManager:
    def __init__(self):
        print("\n" + "="*45)
        print("   MARS-11 COMMAND & CONTROL INTERFACE v1.2")
        print("="*45)
        
        # Initializing core components
        self.shield = RadiationShield()
        self.swarm = OptimusSwarm()
        self.prospector = M11GIEPProspector()
        self.reactor = M11SabatierController()
        self.docking = VisualDocking()
        
        # Initializing Advanced Layers
        self.visual_navigator = VisualLAMAgent()
        self.cognitive_filter = GnosisPurifier()
        self.life_support = BioRegenSystem()
        
        self.sol = 0

    def run_daily_protocol(self):
        """A synchronized operational sequence representing 1 Martian Sol."""
        self.sol += 1
        print(f"\n[SOL {self.sol}] --- INITIALIZING DAILY PROTOCOL ---")

        # 1. COGNITIVE VALIDATION (Filtering incoming Earth commands)
        print(f"[SYSTEM] Receiving data packets from Earth Deep Space Network...")
        mock_packets = [
            {'content': 'Priority: Adjust shield harmonics', 'relevance': 0.9},
            {'content': 'Social: Trending topics on Mars-Net', 'relevance': 0.1}
        ]
        valid_orders = [p for p in mock_packets if self.cognitive_filter.process_stream(p)]

        # 2. SAFETY & ENVIRONMENT (Radiation & Bio-Regen)
        if not self.shield.monitor_radiation():
            print("[ALERT] High Solar Activity! Emergency shielding active.")
            return
        
        # Update Life Support Homeostasis
        # Simulating environment load based on sol activity
        env_load = random.uniform(0.5, 0.8)
        self.life_support.update_homeostasis(env_load)

        # 3. NAVIGATION & INTEGRITY
        if not self.docking.check_alignment():
            print("[MAINTENANCE] Alignment drift. Recalibrating via Swarm...")
            self.swarm.reallocate_units(role="MAINTENANCE", count=2)

        # 4. RESOURCE & PRODUCTION
        purified_signal = self.prospector.purification_logic([0.85, 0.92, 0.78])
        if purified_signal > 0.8:
            print(f"[SUCCESS] Sub-surface H2O signal stable ({purified_signal:.2f})")
            self.reactor.simulate_day(cycles=1)
            self.swarm.reallocate_units(role="MINING", count=4)
        else:
            self.swarm.reallocate_units(role="EXPLORATION", count=11)

        # 5. VISUAL FINAL INSPECTION (LAM)
        print("[LAM] Executing visual sanity check on all control panels...")
        self.visual_navigator.self_heal_protocol()

        print(f"[SOL {self.sol}] --- DAILY PROTOCOL COMPLETE ---")

if __name__ == "__main__":
    manager = MarsBaseManager()
    for _ in range(3):
        manager.run_daily_protocol()
        time.sleep(0.7)
