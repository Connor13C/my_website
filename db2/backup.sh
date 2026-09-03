#!/bin/bash
cd ~/my_website/db2 || exit
docker exec db2 pg_dumpall -U postgres > `date +%Y-%m-%d`.sql
