#!/bin/bash
cd ~/Server/db2 || exit
read -p "Enter name of dump.sql backup in db2 folder to restore in db2 container: " -r filename
if [ -e "$filename" ]
then
  cat $filename | docker exec -i db2 psql -U postgres
else
  echo "Datebase backup not found. Check if filename is correct."
fi
