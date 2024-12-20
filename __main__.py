#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import sys
from os import rename, chdir, listdir, getcwd
from builtins import str

VIDEO_FORMAT = ('avi', 'flv', 'mkv', 'm4p', 'm4v', 'mp4', 'mpeg', 'mpg', 'webm', 'wmv')
SUBTITLE_FORMAT = ('ass', 'srt', 'ssa', 'sub')

def get_files(_format, files):
    return sorted([f for f in files if f.split('.')[-1] in _format])

def match_name(movies, subtitles):
    for (movie, subtitle) in zip(movies, subtitles):
        new_name = "%s.%s" % ('.'.join(movie.split('.')[:-1]), subtitle.split('.')[-1])
        try:
            rename(subtitle, new_name)
            print("Success!!!")
        except OSError:
            print("Oops! Somehow I cannot match the subtitle for you. Sorry...")
            pass

def main():
    chdir(str(sys.argv[1]) if len(sys.argv) > 1 else getcwd())
    files_in_movie_dir = listdir(getcwd())
    if files_in_movie_dir:
        movies = get_files(VIDEO_FORMAT, files_in_movie_dir)
        subtitles = get_files(SUBTITLE_FORMAT, files_in_movie_dir)
        match_name(movies, subtitles)
        print(">>> Done!!! <<<")
    else:
        print("There's nothing here. I'm leaving...")

if __name__ == '__main__':
    main()
