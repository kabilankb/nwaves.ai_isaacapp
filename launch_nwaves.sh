#!/bin/bash
# ============================================================
# Nwaves.ai - AI-Powered Simulation Platform
# Launch Script
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate conda environment
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate leisaac

# Set environment
export NWAVES_AI_ROOT="${SCRIPT_DIR}"

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║      NWAVES.AI - Simulation Platform     ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""
echo "  Python:    $(python --version 2>&1)"
echo "  PyTorch:   $(python -c 'import torch; print(torch.__version__)' 2>/dev/null || echo 'not found')"
echo "  IsaacSim:  $(python -c 'import isaacsim; print(isaacsim.__version__)' 2>/dev/null || echo 'not found')"
echo ""

# Pass all arguments to the Python launcher
python "${SCRIPT_DIR}/nwaves_app.py" "$@"
