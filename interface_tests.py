testfolder='/Users/davidgreenfield/Downloads/pics_boots/'
testimage='B00A0GVP8A.jpg'

import random

def get_random(path):
    from os import walk

    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)

    return random.choice(f)


def main():
    file=get_random(testfolder)
    print file


if __name__ == '__main__':
    main()