# Collin Gros
#
# to sort the files in a folder on my desktop
#
# TODO:
# complete!
# maybe add usr input for in/out dirs?

# also, i know using lists for file extensions is probably
# retarded. some guy out there has definitely made a huge list
# of file extensions. plus, even using the file extension
# method to differentiate between files is retarded. i just
# decided to use it because most of the files i had to sort were
# on windows, which requires file extensions. doing so was particularly
# easier for me than learning how to parse output from
# file {filename} | grep blah blah blah don't know

# WARNING: will overwrite files with same name
#
import os


def sort_files(file_list):
    docs = ["txt", "pdf", "iso", "zip",
            "7z", "docx", "odt", "xlsx",
            "deb", "md", "pptx"]
    code = ["c", "css", "js", "html",
            "h", "sh", "cmake", "xml",
            "pickle", "py", "yml", "url",
            "cpp", "java", "class"]
    music = ["sunvox", "sunsynth", "xi",
             "mp3", "flac", "wav", "xm",
             "reason", "repatch", "ufs",
             "ogg", "sfk", "mid", "m4r"]
    media = ["mp4", "avi", "m4a", "jpg",
             "png", "m4", "bmp", "webm",
             "gif", "jpeg", "mov", "wma",
             "3gp", "thm", "mts", "aae",
             "m2ts"]

    for file_path in file_list:
        #print("FILEPATH:\t{0}".format(file_path))
        in_docs = False
        in_code = False
        in_music = False
        in_media = False
        unknown = False

        file_substr = file_path.split("/")
        file_title = file_substr[-1]
        file_substr_ext = file_path.split(".")
        ext = file_substr_ext[-1].lower()

        in_steam = "SteamLibrary" in file_path

        if ext in docs:
            in_docs = True
        elif ext in code:
            in_code = True
        elif ext in music:
            in_music = True
        elif ext in media:
            in_media = True

        if not (in_docs or in_code or in_music or in_media):
            unknown = True
            #print("unknown ext:\t{0}".format(ext))

        dir_name = ""
        if in_steam:
            dir_name = "sorted/steam/"
        elif in_docs:
            dir_name = "sorted/docs/"
        elif in_code:
            dir_name = "sorted/code/"
        elif in_music:
            dir_name = "sorted/music/"
        elif in_media:
            dir_name = "sorted/pics/"
        elif unknown:
            dir_name = "sorted/unknown/"


        new_path = "/media/surv/2TB/" + dir_name + file_title
        #print("moving from {0} to {1}".format(file_path, new_path))
        os.rename(file_path, new_path)


def get_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    return file_list


sort_path = "/media/surv/2TB/"
file_list = get_files(sort_path)

sort_files(file_list)
#for elm, value in enumerate(exts):
#    print("elm:\t{0}\tvalue:\t{1}".format(elm, value))
