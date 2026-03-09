#!/bin/bash
xdotool mousemove 1280 1024
cd projet/JavaSpace
touch highscore
java -cp .:../..:$HOME Main
