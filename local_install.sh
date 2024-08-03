HERE=$(dirname "$(readlink -f "$0")")
ln -s ${HERE}/src/taskman/cli.py ~/.local/bin/tman

