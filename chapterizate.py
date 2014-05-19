#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

__version__ = '0.1.0'
__author__ = 'Mihail'


class Chapterizate(object):

    def convertToSeconds(self, hours, minuts, seconds):
        totalDuration = hours*3600 + minuts*60 + seconds
        return totalDuration

    def convertToHour(self, seconds):
        hours = int(seconds / 3600)
        hours = str(hours).zfill(2)
        seconds %= 3600
        minuts = int(seconds / 60)
        minuts = str(minuts).zfill(2)
        seconds %= 60
        seconds = str(seconds).zfill(2) + '.000'
        res = hours + ':' + minuts + ':' + seconds
        return res

    def createChapters(self, totalDuration, saveDir, step=10):
        i = 0
        j = 0
        step *= 60
        out = '<?xml version="1.0"?>'
        out += '\n<!-- <!DOCTYPE Chapters SYSTEM "matroskachapters.dtd"> -->'
        out += '\n<Chapters>'
        out += '\n\t<EditionEntry>'
        if saveDir:
            f = open(saveDir + '/Chapters.txt', 'w')
            fxml = open(saveDir + '/Chapters.xml', 'w')
        else:
            f = open('Chapters.txt', 'w')
            fxml = open('Chapters.xml', 'w')
        while i <= totalDuration:
            time = self.convertToHour(i)
            strOut = 'CHAPTER' + str(j).zfill(2) + '=' + time
            strOut2 = 'CHAPTER' + str(j).zfill(2) + 'NAME=' + \
                      'Chapter ' + str(j+1)
            f.write(strOut + '\n' + strOut2 + '\n')

            out += '\n\t\t<ChapterAtom>'
            out += '\n\t\t\t<ChapterDisplay>'
            out += '\n\t\t\t\t<ChapterString>Chapter ' + str(j+1) + \
                   '</ChapterString>'
            out += '\n\t\t\t\t<ChapterLanguage>eng</ChapterLanguage>'
            out += '\n\t\t\t</ChapterDisplay>'
            out += '\n\t\t\t<ChapterTimeStart>' + time + '</ChapterTimeStart>'
            out += '\n\t\t\t<ChapterFlagHidden>0</ChapterFlagHidden>'
            out += '\n\t\t\t<ChapterFlagEnabled>1</ChapterFlagEnabled>'
            out += '\n\t\t</ChapterAtom>'

            i += step
            j += 1
            sys.stdout.write('\r')
            percent = self.percentage(i, totalDuration)
            if percent > 100:
                percent = 100
            print 'Progress: %0.f%%' % percent,
            sys.stdout.flush()
        f.close()
        out += '\n\t</EditionEntry>'
        out += '\n</Chapters>'
        fxml.write(out)
        fxml.close()

    def getLength(self, filename):
        result = subprocess.Popen(["ffprobe", filename],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        for line in result.stdout.readlines():
            if 'Duration' in line:
                res = ''.join(line).strip()
                res = res.split(',')
        return res

    def percentage(self, part, whole):
        return 100 * float(part) / float(whole)


def about():
    print """Chapterizate is script for creating chapter file from video file
By default script create chapter on every 10 minuts
Author: %s
Version: %s

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
% (__author__, __version__)


def creator(filename, byMinuts=10):
    if os.path.isfile(filename):
        print 'Creating chapters'
        saveDir = os.path.split(filename)[0]
        chapt = Chapterizate()
        leng = chapt.getLength(filename)
        leng = leng[0].split(':')
        hours = int(leng[1])
        minuts = int(leng[2])
        seconds = float(leng[3])
        totalDuration = chapt.convertToSeconds(hours, minuts, seconds)
        chapt.createChapters(totalDuration, saveDir, byMinuts)
        print '\n Creating chapters finished'
    else:
        about()


def main():
    # Input arguments
    args = sys.argv
    numOfArgs = len(args)
    if numOfArgs > 1:
        if numOfArgs == 2:
            filename = args[1]
            creator(filename)
        elif numOfArgs == 4:
            if args[1] == '-m' or args[1] == 'minuts':
                byMinuts = int(args[2])
                if isinstance(byMinuts, (int, long)):
                    filename = args[3]
                    creator(filename, byMinuts)
                else:
                    print 'Wrong time %s' % args[2]
            else:
                print 'Wrong parametar %s' % args[1]
        else:
            about()
    else:
        about()


if __name__ == '__main__':
    main()
