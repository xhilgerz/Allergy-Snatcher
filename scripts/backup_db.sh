#!/usr/bin/env bash
set -euo pipefail

DB_CONTAINER="allergy-snatcher-db-1"
DB_USER="myuser"
DB_PASS="mypassword"
DB_NAME="mydatabase"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKUP_FILE="${REPO_ROOT}/backup.sql"

echo "⏳ Creating backup of ${DB_NAME} from container ${DB_CONTAINER}..."

if ! docker ps --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
  echo "❌ Container ${DB_CONTAINER} is not running. Start docker-compose first."
  exit 1
fi

echo "→ Writing dump to ${BACKUP_FILE}"
docker exec "${DB_CONTAINER}" \
  mysqldump \
  -u "${DB_USER}" -p"${DB_PASS}" \
  --single-transaction \
  --routines \
  --triggers \
  "${DB_NAME}" > "${BACKUP_FILE}"

echo "✅ Backup complete."
