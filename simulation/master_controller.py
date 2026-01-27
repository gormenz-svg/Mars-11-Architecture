"""
MARS-11: Master Mission Controller (Executive Layer)
--------------------------------------------------
Orchestration script for the autonomous Martian base operations.
Links Swarm Robotics, GIEP Sensing, Radiation Protection, and ISRU.
"""

import sys
import os
import time

# Adding the project root to sys.path for cross-folder imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing the specific modules from /modules/
try:
    from modules.m11_radiation_shield import RadiationShield
    from modules.m11_optimus_agentic_swarm import OptimusSwarm
    from modules.m11_optimus_prospector_v3 import M11GIEPProspector
    from modules.m11_sabatier_reactor_core_v2 import M11SabatierController
    from modules.m11_visual_docking import VisualDocking  # Added for completeness
    # m11_optimus_site_scan can be used inside the swarm or as a separate tool
except ImportError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    sys.exit(1)

class MarsBaseManager:
    def __init__(self):
        print("\n" + "="*45)
        print("  MARS-11 COMMAND & CONTROL INTERFACE v1.0")
        print("="*45)
        
        # Initializing components
        self.shield = RadiationShield()
        self.swarm = OptimusSwarm()
        self.prospector = M11GIEPProspector()
        self.reactor = M11SabatierController()
        self.docking = VisualDocking()
        
        self.sol = 0

    def run_daily_protocol(self):
        """A synchronized operational sequence representing 1 Martian Sol."""
        self.sol += 1
        print(f"\n[SOL {self.sol}] Starting daily routines...")

        # 1. SAFETY FIRST (Property 6: Constraint)
        # Check radiation levels before any robot leaves the hangar
        if not self.shield.monitor_radiation():
            print("[ALERT] High Solar Activity! All units remain in shielded hangar.")
            return

        # 2. SITE SCAN & NAVIGATION
        # Visual docking check to ensure base integrity
        if not self.docking.check_alignment():
            print("[MAINTENANCE] Docking misalignment detected. Swarm calibrating...")
            self.swarm.reallocate_units(role="MAINTENANCE", count=2)

        # 3. RESOURCE DISCOVERY (Property 3: Knowledge)
        # Using GIEP logic to filter noise and find H2O
        print("[SCAN] Running GIEP-stabilized sub-surface scan...")
        # Simulated raw signal from sensors
        purified_signal = self.prospector.purification_logic([0.82, 0.90, 0.75])
        
        # 4. DYNAMIC PRODUCTION (Property 11: Realization)
        if purified_signal > 0.8:
            print(f"[SUCCESS] High-confidence H2O detected (Confidence: {purified_signal:.2f})")
            print("[ISRU] Activating Sabatier Reactor...")
            self.reactor.simulate_day(cycles=1)
            self.swarm.reallocate_units(role="MINING", count=4)
        else:
            print("[SCAN] No significant resources found. Continuing survey.")
            self.swarm.reallocate_units(role="EXPLORATION", count=11)

        print(f"[SOL {self.sol}] Protocol completed. Data synced to Earth.")

if __name__ == "__main__":
    manager = MarsBaseManager()
    # Let's run a 3-Sol test mission
    for _ in range(3):
        manager.run_daily_protocol()
        time.sleep(0.5)
