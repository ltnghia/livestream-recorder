import cv2
import numpy as np
import json
import os
from datetime import datetime


def write_json(info, file=''):
    outfile = open(file, 'w')
    x = json.dumps(info)
    outfile.write(x)
    outfile.close()
    return file


def load_json(file=''):
    info = json.load(open(file))
    return info


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_current_time(format=False):
    now = datetime.now()
    if format:
        current_time = now.strftime("%Y:%m:%d:%H:%M:%S")
    else:
        current_time = now.strftime("%Y%m%d%H%M%S")
    return current_time

