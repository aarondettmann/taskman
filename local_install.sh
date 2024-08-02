HERE=$(dirname "$(readlink -f "$0")")
ln -s ${HERE}/src/taskman/taskman.py ~/.local/bin/tman

