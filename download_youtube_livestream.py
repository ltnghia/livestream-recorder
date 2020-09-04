import os
from lib.video_recorder import create_json, run
from lib.utils import get_current_time

if __name__ == '__main__':
    json_file = 'urls.json'
    if not os.path.exists(json_file):
        create_json(json_file)

    time = get_current_time()

    run(json_file)
