import os
import subprocess


def delete(dir):
    cmd = ("rm -r " + dir)
    process = subprocess.Popen(rmcmd.split(), stdout=subprocess.PIPE)


def git_clone(dir):
    cmd = ("git clone https://github.com/collingros/{0}".format(dir))
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    process.wait()


git_dirs = ["research", "random", "school", "games"]
cwd = os.getcwd()
for file in os.listdir(cwd):
    if os.path.isdir(file):
        if file in git_dirs:
            delete(file)


for dir in git_dirs:
    git_clone(dir)
