import os
import tensorflow as tf
from tensorflow.contrib import tensorrt as trt

import click
import librosa
import numpy as np

from difflib import get_close_matches

import nltk
from nltk.corpus import words

from keyword_extraction import extract


def load_graph(frozen_graph_path):
    """Loads frozen graph.

    Parameters
    ----------
    frozen_graph_path:
        Path to frozen_graph.pb

    Returns
    -------
        graph: Restored tf.Graph()
    """
    with tf.gfile.GFile(frozen_graph_path, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
    return graph


def compute_mfcc(audio_data, sample_rate):
    """ Computes the mel-frequency cepstral coefficients.
        The audio time series is normalized and its MFCC features are computed.

    Parameters
    ----------
    audio_data:
        Time series of the speech utterance.
    sample_rate:
        Sampling rate.

    Returns
    -------
    mfcc_feat:[num_frames x F]
        Matrix representing the mfcc.
    """

    def normalize_signal(sg, gain=None):
        """
        Normalize float32 signal to [-1, 1] range
        """
        if gain is None:
            gain = 1.0 / (np.max(np.abs(sg)) + 1e-5)
        return sg * gain

    def preemphasis(sg, coeff=0.97):
        return np.append(sg[0], sg[1:] - coeff * sg[:-1])

    audio_data = normalize_signal(audio_data)

    num_fft = 1024
    audio_data = audio_data - np.mean(audio_data)
    audio_data = audio_data / np.max(audio_data)
    audio_data = preemphasis(audio_data, coeff=0.97)
    features = librosa.feature.mfcc(audio_data, sr=sample_rate, n_mfcc=64, n_mels=64, dct_type=4, n_fft=int(num_fft),
                                    hop_length=int(0.01 * sample_rate), win_length=int(0.025 * sample_rate),
                                    center=True, window=np.hamming, power=2).T

    return features


def load_mfcc_wav(file_path):
    """Load and compute MFCC for wav file."""
    audio, sample_rate = librosa.load(file_path, sr=16000)
    return compute_mfcc(audio, sample_rate)


def data_generator(data_path):
    """Generate Common Voice data for inference.

    Parameters
    ----------
    data_path:
        Path to Common Voice dataset.

    Returns
    -------
        feats, seq_len, label: Input features, input sequence length, input label
    """
    for file_name in os.listdir(data_path):
        np_data = load_mfcc_wav(os.path.join(data_path, file_name))
        yield np.expand_dims(np_data, axis=0), np.expand_dims(len(np_data), axis=0), file_name


def pattern_match(output_sentence, vocabulary):
    """

    Parameters
    ----------
    output_sentence:
        Sentence output by model.
    vocabulary:
        List of available words.

    Returns
    -------
        decoded: Matrix of decoded sequences.
    """
    cleaned_decoded = ' '.join(
        [next(iter(get_close_matches(w, vocabulary, n=1, cutoff=0.8)), '') for w in output_sentence.split(' ')])
    return cleaned_decoded

def inference(**options):
    alphabet = 'abcdefghijklmnopqrstuvwxyz\' '
    
    model_path = '/home/milos/Desktop/wingman-20200110T134708Z-001/wingman/model_1'
    data_path = '/home/milos/Desktop/wingman-20200110T134708Z-001/wingman/data'

    vocabulary = words.words()
    
    gpu_options = tf.GPUOptions(allow_growth=True)
    tf_config = tf.ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)

    with tf.Session(config=tf_config) as sess:
        trt_graph = trt.create_inference_graph(
            input_graph_def=None,
            outputs=['decoded:0'],
            input_saved_model_dir=model_path,
            input_saved_model_tags=['serve'],
            max_batch_size=1,
            max_workspace_size_bytes=4 * int(1e9),
            precision_mode='FP16')
        outputs = tf.import_graph_def(trt_graph, return_elements=['decoded:0'])

        dump = open("dump.txt", "a")
        for feats, seq_len, file_name in data_generator(data_path):
            feed_dict = {'import/input_placeholder:0': feats, 'import/seq_len_placeholder:0': seq_len}
            model_outputs = sess.run(outputs, feed_dict=feed_dict)[0][0]
            output_sentence = "".join([alphabet[i] for i in model_outputs])
            cleaned_output = pattern_match(output_sentence, vocabulary=vocabulary)

            #print(f'Raw output: {output_sentence}')
            cleaned_output = pattern_match(output_sentence, vocabulary=vocabulary)
            #print(f'Cleaned output: {cleaned_output}')
            
            dump.write(file_name)
            dump.write("\n")
            dump.write(cleaned_output)
            dump.write("\n")

    dump.close()


def get_keywords():
    data = "/home/milos/Desktop/wingman-20200110T134708Z-001/wingman/transcripted"
    file_output = open("database.txt", "a")    
    
    for file_name in os.listdir(data):
        file = open(os.path.join(data, file_name), "r")
        text = file.read()
        keywords = extract(text)
        file_output.write(file_name)
        file_output.write("\n")
        file_output.write(str([str(keyword[0]) for keyword in keywords]))
        file_output.write("\n")

    file_output.close

if __name__ == "__main__":
    #nltk.download('words')
    #inference()
    #get_keywords()

    database = open("database.txt", "r")
    podcasts = []
    
    for line in database:
        if line[0] != "[":
            podcasts.append({"name": line[:len(line) - 5]})
        else:
            podcasts[-1]["keywords"] = line


    while True:
        keyword = input("Enter keyword: ")

        for podcast in podcasts:
            if keyword in podcast["keywords"]:
                print(podcast["name"])



