import os
from pysndfx import AudioEffectsChain

fx = (
    AudioEffectsChain()
    # gain=-20.0, frequency=3000, slope=0.5
    #.highshelf(-100.0)
    .lowpass(60)
    .normalize()
)

audio = ["wav"]
parent_dir = os.getcwd()
wav_dir = parent_dir + "/bass_boost"
for file in os.listdir(wav_dir):
    print("file: {0}".format(file))
    infile = wav_dir + "/" + file
    file_substr = file.split(".")

    if file_substr[-1] in audio:
        outfile = wav_dir + "/" +  file_substr[0] + "_BASS.ogg"
        print("outfile: {0}".format(outfile))
        fx(infile, outfile)
