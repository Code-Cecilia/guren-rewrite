#!/bin/sh
while true
do
python3.9 main.py
echo "If you want to stop the boot from booting up please press CTRL+C before the time is up!"
echo "Rebooting  in:"
for i in 5 4 3 2 1
do
echo "$i..."
sleep 1
done
echo "Rebooting now!"
done