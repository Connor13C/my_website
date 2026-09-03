#!/bin/bash
cd ~/my_website/db3 || exit
read -p "Enter name of dump.sql backup in db3 folder to restore in db3 container: " -r filename
if [ -e "$filename" ]
then
  cat $filename | docker exec -i db3 psql -U postgres
else
  echo "Datebase backup not found. Check if filename is correct."
fi
