#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== MkDocs: Настройка окружения Linux (Tuxedo OS / Ubuntu) ==="

echo "[*] Рекомендуемые системные библиотеки (для cairosvg и генерации соц. карточек):"
echo "    sudo apt update && sudo apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 python3-venv python3-pip"

if [ ! -d "docs-env" ]; then
    echo "[*] Создание виртуального окружения docs-env..."
    python3 -m venv docs-env
fi

echo "[*] Обновление pip и установка зависимостей..."
docs-env/bin/pip install --upgrade pip
docs-env/bin/pip install -r requirements.txt

echo "[+] Настройка завершена!"
echo "    Запуск сервера: ./serve.sh"
echo "    Сборка сайта:   ./build.sh"
