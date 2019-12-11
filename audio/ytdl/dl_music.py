import os

import subprocess


def load_file(filename):
    links = []
    names = []
    with open(filename, "r") as file:
        count = 0
        for line in file:
            line = line.rstrip()
            if count % 2 == 0:
                links.append(line)
            else:
                name = line
                names.append(name)

            count += 1

    return links, names


def get_songs(music_dir):
    songs = []
    for song in os.listdir(music_dir):
            song_substr = song.split(".")
            song = song_substr[0]

            songs.append(song)

    return songs


def download(name, link):
    print("name: {0}\tlink: {1}".format(name, link))
    cmd = "youtube-dl -x {0} --audio-format mp3 -o {1}.webm".format(link, name)

    print("cmd: {0}".format(cmd))
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    process.wait()


cwd = os.getcwd()
music_dir = "/home/surv/Music"
filename = "links.txt"
links, names = load_file(filename)
songs = get_songs(music_dir)

os.chdir(music_dir)
count = 0

print(songs)

for link in links:
    cur_name = names[count]

    cur_name_substr = cur_name.split(".")
    cur_name = cur_name_substr[0]

    print(cur_name)
    if cur_name not in songs:
        download(names[count], link)

    count += 1

