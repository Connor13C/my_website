#!/bin/bash
cd ~/my_website/db1 || exit
docker exec db1 pg_dumpall -U postgres > `date +%Y-%m-%d`.sql
