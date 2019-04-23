#!/bin/bash
sudo rm -rf /opt/firefly/backend/seeds
sudo mkdir /opt/firefly/backend/seeds
sudo chown firefly /opt/firefly/backend/seeds
sudo cd /opt/firefly/backend/seeds
sudo git clone https://zexxon@github.com/shaunmkrueger/Seeds -b master ./backend/seeds 
