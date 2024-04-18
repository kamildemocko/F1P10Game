#!/bin/bash
until poetry run python3 main.py; do
	echo "F1Game crashed with exit code $?. Respawning..." >&2
	sleep 1
done

