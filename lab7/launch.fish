#!/usr/bin/env fish

docker compose up -d --build

tmux new-session -d -s iotlab 'docker attach host1'
tmux split-window -h -t iotlab:1 'docker exec -it host2 bash'

tmux new-window -t iotlab -n task-2 'docker attach device'
tmux split-window -h -t iotlab:2 'docker attach monitor'

tmux select-window -t iotlab:1
tmux select-pane -t iotlab:1

tmux attach-session -t iotlab
