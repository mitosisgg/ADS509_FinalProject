#!/usr/bin/env bash
# tell OS to run using bash and 
# safety flags
    # e - exits immediately if any fails
    # u - treats undefined vars as errors and fails early
    # o - if the pipeline fails exit with the failing cmd status
set -euo pipefail

# enable repo root to allow running from anywhere
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/"; pwd)"

# set paths
VENV_DIR="$REPO_DIR/.venv" # project virtual environment
PY="$VENV_DIR/bin/python" # specify the python interpreter
MAIN="$REPO_DIR/fetch_articles.py" # id the main script to fetch articles
LOG_DIR="$REPO_DIR/logs" # establish location for logs
RAW_DIR="$REPO_DIR/data/raw" # establish where the raw JSON files go

# makes logging directories and data directories
# skips if they exist
mkdir -p "$LOG_DIR" "$RAW_DIR"

# create the locking mechanism to prevent multiple copies from running in parallel
LOCK_DIR="$REPO_DIR/.fetch_lock"
cleanup() {
  rm -rf "$LOCK_DIR" || true
}
if mkdir "$LOCK_DIR" 2>/dev/null; then
  # remove lock on normal exit
  trap cleanup EXIT INT TERM
else
  # exit gracefully if another run is in progress
  echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') [WARN] Another fetch is in progress (lock present). Exiting." >> "$LOG_DIR/fetch.log"
  exit 0
fi

# activate our venv and dont rely solely on cron environment
if [[ ! -x "$PY" ]]; then
  echo "[ERROR] Python venv not found at $PY. Make sure you've created it and installed requirements." >&2
  exit 1
fi

# create timestamped log files and a rolling main log for data acquisition
RUN_STAMP="$(date +'%Y%m%d_%H%M%S')"
RUN_LOG="$LOG_DIR/fetch_${RUN_STAMP}.log"
MAIN_LOG="$LOG_DIR/fetch.log"

# run the job and send output to both logs (RUN and MAIN)
{
  echo "==== $(date -u +'%Y-%m-%dT%H:%M:%SZ') | START fetch_articles ===="
  echo "Repo: $REPO_DIR"
  echo "Python: $PY"
  echo "Script: $MAIN"
  echo "Working dir contents:"
  ls -la "$REPO_DIR"

  # ensure .env is in repo root so python-dotenv can find it
  if [[ ! -f "$REPO_DIR/.env" ]]; then
    echo "[ERROR] .env not found at $REPO_DIR/.env (expected NEWS_API_KEY=...)" >&2
    exit 2
  fi

  # run the fetch (unbuffered stdout)
  "$PY" -u "$MAIN"

  echo "==== $(date -u +'%Y-%m-%dT%H:%M:%SZ') | DONE fetch_articles ===="
} | tee -a "$RUN_LOG" >> "$MAIN_LOG" 2>&1