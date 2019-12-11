import os
import subprocess


def cd(folder):
    cwd = os.getcwd()
    os.chdir(cwd + "/" + folder)


def ls():
    print(os.listdir())


def pwd():
    print(os.getcwd())

pwd()
ls()
cd("/Desktop")
pwd()
ls()
