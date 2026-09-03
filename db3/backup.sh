#!/bin/bash
cd ~/my_website/db3 || exit
docker exec db3 pg_dumpall -U postgres > `date +%Y-%m-%d`.sql
