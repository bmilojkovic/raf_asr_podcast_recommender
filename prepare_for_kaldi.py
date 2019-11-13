import glob
import os
import wave
import contextlib
import audioop
import librosa
from pydub import AudioSegment
from shutil import copyfile
from random import shuffle

def all_in_one():
    i = 0
    for filepath in glob.iglob("dataset_wav/" + '**/*.wav', recursive=True):
        if i % 100 == 0:
            print(filepath)

        filename = filepath.split("\\")[-1]
        copyfile(filepath, "dataset_all_wav/" + filename)

        i += 1

def split_train_validate_test():
    path = "dataset_all_wav/"
    files = []
    dirs = os.listdir(path)

    for file in dirs:
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)

    shuffle(files)

    train_files = files[:len(files)*7//10]
    validate_files = files[len(files)*7//10:round(len(files)*8.5//10)]
    test_files = files[round(len(files)*8.5//10):]

    for file in train_files:
        print(file)
        filepath = "dataset_all_wav/" + file
        copyfile(filepath, "dataset_all_wav/train/" + file)

    for file in validate_files:
        print(file)
        filepath = "dataset_all_wav/" + file
        copyfile(filepath, "dataset_all_wav/validation/" + file)

    for file in test_files:
        print(file)
        filepath = "dataset_all_wav/" + file
        copyfile(filepath, "dataset_all_wav/test/" + file)

def create_text_file():
    path = "dataset_all_wav/test/"
    f = open("text_test", "w+")
    i = 10000
    for filename in os.listdir(path):
        word = filename.split("_")[-2]
        utt_id = filename.split(".")[0].upper()
        # f.write(filename.split(".")[0].upper() + " " + word.upper() + "\n")
        f.write(str(i) + "_" + utt_id + " " + word.upper() + "\n")
        i += 1
    f.close()

def create_segments_file():
    path = "dataset_all_wav/test/"
    seg_f = open("segments_test", "w+")
    i = 10000
    for filename in os.listdir(path):
        with contextlib.closing(wave.open(path + filename, "r")) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            # print(rate)
            # print(f.getnchannels())
            duration = frames / float(rate)
            utt_id = filename.split(".")[0].upper()
            seg_f.write(str(i) + "_" + utt_id + " " + utt_id + " 0 " + str(round(duration, 2)) + "\n")
        i += 1
    seg_f.close()

def create_wav_scp_file():
    path = "dataset_all_wav/validation/"
    scp_file = open("wav_validation.scp", "w+")
    for filename in os.listdir(path):
        utt_id = filename.split(".")[0].upper()
        scp_file.write(utt_id + " " + "/home/bogdan/kaldi/egs/mycorpus/data/validate/validate_data/" + filename + "\n")
    scp_file.close()

def create_utt2spk_file():
    path = "dataset_all_wav/test/"
    utt2spk_f = open("utt2spk_test", "w+")
    i = 10000
    for filename in os.listdir(path):
        utt_id = filename.split(".")[0].upper()
        utt2spk_f.write(str(i) + "_" + utt_id + " " + str(i) + "\n")
        i += 1
    utt2spk_f.close()

def filter_lexicon_words():
    ref = dict()
    phones = dict()

    with open("lexicon.txt") as f:
        for line in f:
            line = line.strip()
            columns = line.split(" ", 1)
            word = columns[0]
            if "(" in word:
                word = word.split("(")[0]
            pron = columns[1]
            try:
                ref[word].append(pron)
            except:
                ref[word] = list()
                ref[word].append(pron)

    print(ref)

    lex = open("lexicon1.txt", "w+")

    with open("words.txt") as f:
        for line in f:
            line = line.strip()
            if line in ref.keys():
                for pron in ref[line]:
                    lex.write(line + " " + pron + "\n")
            else:
                print("Word not in lexicon:" + line)

def rename_all_files():
    path = "dataset_all_wav/test/"
    for filename in os.listdir(path):
        filename_split = filename.split()
        os.rename(path + filename, path + filename_split[0] + "_" + filename_split[1])

def convert_all_to_8khz():
    path = "dataset_all_wav/train/"
    new_path = "dataset_all_wav/train1/"
    for filename in os.listdir(path):
        y, s = librosa.load(path + filename, sr=8000)  # Downsample 44.1kHz to 8kHz
        librosa.output.write_wav(new_path + filename, y, 8000)

def convert_all_to_mono():
    path = "dataset_all_wav/test/"
    new_path = "dataset_all_wav/test2/"
    for filename in os.listdir(path):
        sound = AudioSegment.from_wav(path + filename)
        sound = sound.set_channels(1)
        sound.export(new_path + filename, format="wav")

# convert_all_to_mono()
# convert_all_to_8khz()
# rename_all_files()
create_wav_scp_file()
# create_text_file()
# create_segments_file()
# create_utt2spk_file()
# filter_lexicon_words()
