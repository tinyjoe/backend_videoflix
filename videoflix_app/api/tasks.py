import subprocess

def convert_480p(source_path):
    target_path = source_path + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_path, target_path)
    subprocess.run(cmd)


def convert_720p(source_path):
    target_path = source_path + '_720p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_path, target_path)
    subprocess.run(cmd)


def convert_1080p(source_path):
    target_path = source_path + '_1080p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_path, target_path)
    subprocess.run(cmd)