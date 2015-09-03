#!/usr/bin/env bash

PYVENV=yes

case `uname` in
	Linux )
		pyvenv='/usr/bin/pyvenv-3.4'
		;;
	Darwin )
		echo 'You may need to install postgresql with "brew install postgresql"'
		pyvenv='/usr/local/bin/pyvenv'
		;;
	* )
		exit 1
		;;
esac

$pyvenv -h > /dev/null 2>&1 || unset PYVENV

if [ -n "$PYVENV" ]; then
	echo "pyvenv found.."
else
	echo "no suitable python virtual env tool found, aborting"
	exit 1
fi

$pyvenv --without-pip .venv
source .venv/bin/activate # Seems not work properly
if [ ! -f .venv/bin/pip ]; then
    # Due to Ubuntu 14.04 and Debian have a broken pyvenv-3.4 tool
	echo "no pip found.. in .venv"
	curl https://bootstrap.pypa.io/get-pip.py | python
	deactivate
	source .venv/bin/activate
fi
pip install -r requirements.txt