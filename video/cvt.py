import os
import subprocess


def run_cmd(cmd):
    print("running:\t{0}".format(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    process.wait()


def cvt(name):
    sub = name.split(".")
    base = sub[0]

    cmd = "ffmpeg -i {0} {1}.mp3".format(name, base)
    run_cmd(cmd)


cwd = os.getcwd()
for song in os.listdir(cwd):
    cvt(song)
