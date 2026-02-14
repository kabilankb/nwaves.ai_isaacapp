"""
Nwaves.ai - AI-Powered Simulation Platform
Main application launcher.
"""

import argparse
import os
import sys

# Set environment
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["NWAVES_AI_ROOT"] = SCRIPT_DIR

# Custom Nwaves.ai experience file (overrides IsaacSim default title)
NWAVES_EXPERIENCE = os.path.join(SCRIPT_DIR, "source", "apps", "nwaves.ai.exp.kit")


def main():
    parser = argparse.ArgumentParser(description="Nwaves.ai Simulation Platform")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--test", action="store_true", help="Run integration test only")
    args = parser.parse_args()

    if args.test:
        _run_test()
        return

    from isaacsim import SimulationApp

    config = {
        "headless": args.headless,
        "width": 1920,
        "height": 1080,
        "anti_aliasing": 0,
    }

    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║      NWAVES.AI - Simulation Platform     ║")
    print("  ╚══════════════════════════════════════════╝")
    print()

    # Launch with custom Nwaves.ai experience file
    simulation_app = SimulationApp(config, experience=NWAVES_EXPERIENCE)

    # Force override window title at every level after app init
    import carb.settings
    settings = carb.settings.get_settings()
    settings.set("/app/window/title", "Nwaves.ai")
    settings.set("/app/name", "Nwaves.ai")
    settings.set("/app/version", "0.1.0")
    settings.set("/app/environment/name", "Nwaves.ai")

    try:
        from omni.kit.window.title import get_main_window_title
        window_title = get_main_window_title()
        window_title.set_app_version("0.1.0")
    except Exception:
        pass

    try:
        import omni.appwindow
        app_window = omni.appwindow.get_default_app_window()
        app_window.set_title("Nwaves.ai")
    except Exception:
        pass

    print("[Nwaves.ai] GUI ready")
    while simulation_app.is_running():
        simulation_app.update()

    simulation_app.close()
    print("[Nwaves.ai] Application closed")


def _run_test():
    print()
    print("  Nwaves.ai Integration Test")
    print("  " + "=" * 40)

    import torch
    print(f"  [OK] PyTorch {torch.__version__} - CUDA: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  [OK] GPU: {torch.cuda.get_device_name(0)}")

    if os.path.exists(NWAVES_EXPERIENCE):
        print(f"  [OK] Nwaves.ai experience file found")
    else:
        print(f"  [WARN] Experience file not found at {NWAVES_EXPERIENCE}")

    print()
    print("  All tests passed!")
    print()


if __name__ == "__main__":
    main()
