#!/bin/bash
# WSL Backup Script
# Backs up home directory to D: drive
# Usage: ./backup-wsl.sh

set -e

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/mnt/d/Backups/WSL"
BACKUP_FILE="$BACKUP_DIR/wsl_backup_$DATE.tar.gz"

echo "=========================================="
echo "WSL Backup Script"
echo "Date: $DATE"
echo "=========================================="

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if backup already exists today
if [ -f "$BACKUP_FILE" ]; then
    echo "Backup already exists for today: $BACKUP_FILE"
    read -p "Overwrite? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Backup cancelled."
        exit 0
    fi
fi

echo "Starting backup..."
echo "Excluding: node_modules, .venv, .cache, *.pyc, .git"

tar -czvf "$BACKUP_FILE" \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.cache' \
    --exclude='.npm' \
    --exclude='*.log' \
    -C /home oak38

# Get backup size
SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

echo "=========================================="
echo "Backup complete!"
echo "File: $BACKUP_FILE"
echo "Size: $SIZE"
echo "=========================================="

# List recent backups
echo ""
echo "Recent backups:"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5

# Cleanup old backups (keep last 5)
echo ""
echo "Cleaning up old backups (keeping last 5)..."
cd "$BACKUP_DIR" && ls -t *.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -v

echo ""
echo "Done!"
