#!/bin/bash
xdotool mousemove 1280 1024
cd projet/Minesweeper
touch highscore
java -cp .:../..:$HOME Minesweeper
