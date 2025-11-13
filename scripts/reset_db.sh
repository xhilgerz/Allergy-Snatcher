#!/usr/bin/env bash
set -euo pipefail

DB_CONTAINER="allergy-snatcher-db-1"
DB_USER="myuser"
DB_PASS="mypassword"
DB_NAME="mydatabase"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "⏳ Resetting ${DB_NAME} inside container ${DB_CONTAINER}..."

if ! docker ps --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
  echo "❌ Container ${DB_CONTAINER} is not running. Start docker-compose first."
  exit 1
fi

run_mysql() {
  local sql_file="$1"
  echo "→ Applying ${sql_file}"
  docker exec -i "${DB_CONTAINER}" \
    mysql -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" < "${sql_file}"
}

run_mysql "${REPO_ROOT}/drop.sql"
run_mysql "${REPO_ROOT}/create.sql"

echo "→ Regenerating init_data.sql from dummy-foods"
python3 "${REPO_ROOT}/dataimport.py" -i "${REPO_ROOT}/dummy-foods" --output "${REPO_ROOT}/init_data.sql"

run_mysql "${REPO_ROOT}/init_data.sql"
run_mysql "${REPO_ROOT}/crud.sql"

echo "✅ Database reset complete. Opening interactive mysql shell..."
exec docker exec -it "${DB_CONTAINER}" mysql -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}"
