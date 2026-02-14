# Nwaves.ai Simulation Platform

AI-powered simulation platform built on NVIDIA Isaac Sim.

## Prerequisites

- Ubuntu 22.04+
- NVIDIA GPU with CUDA 12.x
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- NVIDIA Isaac Sim 4.5+

## Setup

### 1. Clone the repository

```bash
git clone --recursive https://github.com/kabilankb/nwaves.ai_isaacapp.git
cd nwaves.ai_isaacapp
```

### 2. Create conda environment

```bash
conda create -n leisaac python=3.10 -y
conda activate leisaac
```

### 3. Install dependencies

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install isaacsim-rl isaacsim-replicator isaacsim-extscache-physics isaacsim-extscache-kit-sdk \
    --extra-index-url https://pypi.nvidia.com
```

### 4. Install LeIsaac

```bash
cd leisaac
pip install -e .
cd ..
```

## Launch

```bash
./launch_nwaves.sh
```

Run in headless mode:

```bash
./launch_nwaves.sh --headless
```

Run integration test:

```bash
./launch_nwaves.sh --test
```

## Project Structure

```
nwaves-sim/
├── .gitignore
├── .gitmodules
├── README.md
├── nwaves_app.py              # Main application launcher
├── launch_nwaves.sh           # Shell launch script
├── leisaac/                   # LeIsaac framework (git submodule)
└── source/
    └── apps/
        └── nwaves.ai.exp.kit  # Isaac Sim experience config
```

## License

Proprietary - All rights reserved.
