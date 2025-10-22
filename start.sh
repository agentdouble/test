#!/usr/bin/env bash

# Script de démarrage: backend + jeu (Snake)
# Version UV: utilise `uv sync` pour installer et `uv run` pour exécuter

set -Eeuo pipefail
export PYTHONUNBUFFERED=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log() { printf "[start.sh] %s\n" "$*"; }

# 0) Vérifier la présence de uv
if ! command -v uv >/dev/null 2>&1; then
  log "uv n'est pas installé. Installez-le avec :"
  log "  curl -LsSf https://astral.sh/uv/install.sh | sh"
  log "ou via pipx : pipx install uv"
  exit 1
fi

# 1) Forcer un environnement projet dans .venv (comportement par défaut de uv)
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-.venv}"

# 2) Synchroniser l'environnement à partir de pyproject.toml (créera .venv si absent)
log "Synchronisation de l'environnement avec uv (pyproject.toml)"
uv sync

# 3) Lancer le backend en arrière‑plan avec uv run
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

BACKEND_CMD=(uv run python backend/main.py)
log "Démarrage du backend: ${BACKEND_CMD[*]}"
"${BACKEND_CMD[@]}" >"$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
log "Backend PID: $BACKEND_PID (logs: $LOG_DIR/backend.log)"

cleanup() {
  log "Arrêt du backend (PID $BACKEND_PID)"
  if kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# 4) Lancer le jeu au premier plan via uv run (assure que l'env est à jour)
GAME_CMD=(uv run python backend/snake.py)
log "Lancement du jeu (Snake): ${GAME_CMD[*]}"
"${GAME_CMD[@]}"

# 5) Le trap EXIT s'occupera d'arrêter le backend
log "Jeu terminé. Nettoyage en cours…"
