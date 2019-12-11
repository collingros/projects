# cgros
# rename files so that i dont overwrite pictures, preserving modification time
# WILL overwrite files that have the same name, but start with '['!
import os
import subprocess


def rm(src):
    cmd = "rm -r \"{0}\"".format(src)
    run(cmd)


def mv(src, dst):
    cmd = "cp -r -p \"{0}\" \"{1}\"".format(src, dst)
    run(cmd)
    rm(src)


def run(cmd):
    print(cmd)
    print()

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    process.wait()


media = ["png", "jpg", "mp4", "gif"]

my_dir = "/media/surv/FLASHDRIVE/may_30/"
os.chdir(my_dir)

cwd = os.getcwd()
files = os.listdir(cwd)
files = sorted(files, key=os.path.getmtime)

count = 0
for file in files:
    str_list = file.split(".")
    ext = str_list[-1]
    if ext not in media:
        continue

    src = file
    dst = "i_{:05}".format(count)
    dst = "{0}.{1}".format(dst, ext)

    mv(src, dst)

    count += 1
