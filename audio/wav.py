import os
import subprocess


def convert(file):
    file_substr = file.split(".")
    out_dir = "bass_boost"
    convcmd = ("ffmpeg -i " + file + " " + out_dir + "/" +
                file_substr[0] + ".wav")

    process = subprocess.Popen(convcmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


audio = ["opus", "ogg"]
cwd = os.getcwd()
for file in os.listdir(cwd):
    file_substr = file.split(".")

    if file_substr[-1] not in audio:
        continue

    convert(file)
