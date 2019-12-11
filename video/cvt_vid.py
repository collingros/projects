import os
import subprocess


def run(cmd):
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


def rm(name):
    cmd = "rm -rf {0}".format(name)
    run(cmd)


def cvt(name):
# reduce video size from name, deletes original video
    cmd = "ffmpeg -loglevel quiet -i {0} ffmpeg_{1}".format(name, name)
    run(cmd)
    rm(name)


video_media = ["mp4", "mkv"]
for file in sorted(os.listdir(os.getcwd())):
    file_ext = file.split(".")
    if file_ext[-1] in video_media:
        cvt(file)
