#!/usr/bin/env bash
echo "Install required packages"

case `uname` in
    Linux )
        sudo apt-get update
        sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
        ;;
    Darwin )
        brew update
        brew install postgres
        ;;
    *)
    exit 1
    ;;
esac

type virtualenv >/dev/null 2>&1 || { echo >&2 "No suitable python virtual env tool found, aborting"; exit 1; }

rm -rf .venv
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt