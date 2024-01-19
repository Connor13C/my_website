#!/bin/bash
cd ~/Server/db1 || exit
read -p "Enter name of dump.sql backup in db1 folder to restore in db1 container: " -r filename
if [ -e "$filename" ]
then
  cat $filename | docker exec -i db1 psql -U postgres
else
  echo "Datebase backup not found. Check if filename is correct."
fi
