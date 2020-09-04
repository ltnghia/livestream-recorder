# pip install pytube3
# brew install streamlink

from pytube import YouTube
# import streamlink
import os
import subprocess
from multiprocessing import Pool
import shlex

from .utils import get_current_time, write_json, load_json


def download_video(url="https://www.youtube.com/watch?v=cl05DnHnxIw", output_path=".", quality="best"):
    youtube = YouTube(url)
    if quality == 'best':
        video = youtube.streams.get_highest_resolution()
    elif quality == 'all':
        video = youtube.streams.filter(file_extension="../mp4").all()
    else:
        video = youtube.streams.first()
    video.download(output_path)
    info = {'id': video.video_id,
            'title': video.title,
            'length': video.length,
            'rating': video.rating,
            'views': video.views}
    return info


def download_livestream(url="https://www.youtube.com/embed/jEhIe2SDKso", output_path="raw_video.mp4",
                        quality="best", duration='00:01:00', exe=True):
    # streams = streamlink.streams(url)
    # stream = streams["source"]
    # fd = stream.open()
    # data = fd.read(1024)
    # fd.close()
    cmd = "streamlink {} {} --output {}".format(url, quality, output_path)
    if duration is not None and duration:
        cmd = '{} --hls-duration {}'.format(cmd, duration)
    if exe:
        os.system(cmd)
    return cmd


def convert_video(input_path, output_path, exe=True):
    cmd = 'ffmpeg -i {} {}'.format(input_path, output_path)
    if os.path.exists(input_path) and exe:
        os.system(cmd)
    return cmd


def record_livestream(url="https://www.youtube.com/embed/jEhIe2SDKso", id=0,
                      raw_output_folder="raw", mp4_output_folder="mp4",
                      quality="best", duration='00:01:00'):
    current_time = get_current_time()
    cmd1 = download_livestream(url=url,
                               output_path=os.path.join(raw_output_folder, 'stream_{}_{}.mp4'.format(id, current_time)),
                               quality=quality, duration=duration, exe=False)
    cmd2 = convert_video(input_path=os.path.join(raw_output_folder, 'stream_{}_{}.mp4'.format(id, current_time)),
                         output_path=os.path.join(mp4_output_folder, 'stream_{}_{}.mp4'.format(id, current_time)), exe=False)
    cmd = cmd1 + ' && ' + cmd2
    # print(shlex.split(cmd))
    # file = open('run.sh', 'w')
    # file.write(cmd1 + "\n")
    # file.write(cmd2)
    # file.close()
    # process = subprocess.Popen(cmd, shell=True)
    # proc_stdout = process.communicate()
    # print(proc_stdout)
    os.system(cmd)


def record(param):
    record_livestream(url=param['url'], id=param['id'], raw_output_folder=param['raw_output_folder'],
                      mp4_output_folder=param['mp4_output_folder'], quality=param['quality'], duration=param['duration'])


def create_json(json_file='urls.json'):
    data = {'info': [], 'current_stream': 0, 'max_streams': 3}
    for i in range(10):
        data['info'].append({'id': i,
                             'url': "https://www.youtube.com/embed/jEhIe2SDKso",
                             'quality': "best",
                             'duration': '00:01:00',
                             'raw_output_folder': 'raw',
                             'mp4_output_folder': 'mp4'})
    write_json(data, json_file)


def get_params(json_file='urls.json'):
    data = load_json(json_file)
    current_stream = data['current_stream']
    max_streams = data['max_streams']
    next_stream = min(current_stream + max_streams, len(data['info']))
    params = []
    for i in range(current_stream, next_stream):
        params.append(data['info'][i])
    data['current_stream'] = 0 if next_stream == len(data['info']) else next_stream
    write_json(data, json_file)
    return params, current_stream


def run(json_file='urls.json'):
    if os.path.exists(json_file):
        params, current_stream = get_params(json_file)
        if params:
            current_time = get_current_time(format=True)
            print('Downloading {} streams from id={}, at {}'.format(len(params), current_stream, current_time))
            # for param in params:
            #     record(param)
            pool = Pool()
            pool.map(record, params)


if __name__ == '__main__':
    run()
