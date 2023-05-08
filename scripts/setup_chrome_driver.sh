#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VERSION="113.0.5672.63"
NAME="chromedriver_linux64"
OUT="$SCRIPT_DIR/../bin"

rm -rf $OUT

CHROMEDRIVER="$SCRIPT_DIR/../bin/$NAME.zip"
wget "https://chromedriver.storage.googleapis.com/$VERSION/$NAME.zip" -P "$SCRIPT_DIR/../bin" && \
unzip "$CHROMEDRIVER" -d "$SCRIPT_DIR/../bin" && \
rm "$CHROMEDRIVER"