chapterizate
============

Chapterizate is script for creating chapter file from video file By default script create chapter on every 10 minuts

writen for python 2.7

Version: 0.1.0

Requirements:
    Installed ffmpeg

Usage:
    chapterizate [option] filename

Options:
    -m  minuts  Create chapter on every 1,10,15
                etc minuts depend of value you enter
                default value is 10

Examples:
    chapterizate filename.avi
    chapterizate -m 5 filename.avi
    chapterizate -m 15 filename.avi

Program creates to files one .txt one .xml format""" \
