import os
import subprocess


def convert(pic):
    cmd = "convert -quality 25 \"{0}\" ../cvt/\"{1}\"".format(pic, pic)
    run(cmd)


def cp(src, dst):
    cmd = "cp -r -p \"{0}\" \"{1}\"".format(src, dst)
    run(cmd)


def rm(src):
    cmd = "rm -r {0}".format(src)
    run(cmd)


def mkdir(src):
    cmd = "mkdir {0}".format(src)
    run(cmd)


def run(cmd):
    print(cmd)

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while process.poll() is None:
        pass


rm("../cvt")
mkdir("../cvt")
rm("../vid")
mkdir("../vid")

blacklist = ["mp4", "gif", "py"]
for file in os.listdir(os.getcwd()):
    file_ext_l = file.split(".")
    file_ext = file_ext_l[-1]

    if file_ext in blacklist:
        new = "../vid/{0}".format(file)
        cp(file, new)

        continue

    convert(file)
