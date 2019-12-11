# for renaming and moving screenshots when a new one is taken so that
# screenshots are not overwritten
import os
import subprocess


def mv(src, dst):
    cmd = "mv {0} {1}".format(src, dst)
    run_cmd(cmd)


def run_cmd(cmd):
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    task.wait()


count = 0
my_dir = "/home/surv/Pictures/screenshots"
for pic in sorted(os.listdir(my_dir)):
    count += 1

src = "/home/surv/cap.png"
dst = "/home/surv/Pictures/screenshots/{0}.png".format(count)
mv(src, dst)
