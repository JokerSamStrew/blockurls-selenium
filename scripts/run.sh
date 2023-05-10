#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

BLACK_LIST='[ "*.css", "*.png", "*.ico", "*.jpg", "*.webp", "*.woff2", "*gstatic*", "*uviewer*", "*youtube*", "data:image*" ]'
TARGET='https://www.google.com'
MAIN_DIR="$SCRIPT_DIR/../src" 
MAIN=$MAIN_DIR/main.py

# python -m poetry run -C "$MAIN_DIR" python "$MAIN" "$TARGET" "$BLACK_LIST"
python "$MAIN" --target "$TARGET" --black-list "$BLACK_LIST" --timeout 15