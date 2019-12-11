# collin gros
# 09/18/2019
#
# from exported bookmarks.html file from firefox,
# get all youtube links and write them in a text file
# like the following:

# in links.txt:
#       https://www.youtube.com/watch?v=JdgcCUVdl6c
#       juicy_j_bandz
#       ...etc
import os


def get_title(line):
        line_sub = line.split("</A>")
        name_line = line_sub[-2]
        # get part of line right before "</A>" near the end of the line

        name_sub = name_line.split(">")
        name_line = name_sub[-1]
        # get part of line near the end, after ">"

        return name_line


def get_link(line):
        if "youtube.com" not in line:
                return ""

        line_sub = line.split("HREF=\"")
        link_line = line_sub[1]
        # get part of link right after beginning quotes

        link_sub = link_line.split("\"")
        link_line = link_sub[0]
        # cut off link right after ending quotes

        return link_line


write_arr = []
with open("bookmarks.html", 'r') as f:
# read from exported bookmarks html file from firefox
        for line in f:
                link = get_link(line)
                if link == "":
                # link didn't contain a youtube link
                        continue

                title = get_title(line)

                write_arr.append(link)
                write_arr.append(title)


with open("links.txt", 'w') as f:
# writing all links and names to "links.txt"
        for line in write_arr:
                f.write(line)
                f.write("\n")
