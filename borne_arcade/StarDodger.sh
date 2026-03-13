#!/bin/bash
xdotool mousemove 1280 1024
cd projet/StarDodger
touch highscore
java -cp .:../..:$HOME Main
