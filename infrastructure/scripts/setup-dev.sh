#!/usr/bin/env bash

# LeadScan AI Developer Environment Setup Script
set -euo pipefail

echo "========================================="
echo "Initializing LeadScan AI Monorepo Dev Env"
echo "========================================="

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed." >&2
    exit 1
fi

# Check PNPM
if ! command -v pnpm &> /dev/null; then
    echo "Error: PNPM is not installed. Please run: npm install -g pnpm" >&2
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed." >&2
    exit 1
fi

echo "Installing JS/TS workspace dependencies..."
pnpm install

echo "Setting up local env config..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env created from template."
else
    echo ".env already exists, skipping."
fi

echo "========================================="
echo "Monorepo initialized successfully!"
echo "========================================="
