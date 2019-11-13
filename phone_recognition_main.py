import AudioAnalyzer
import numpy
from RestrictedBoltzmannMachine import RBM
from DeepBeliefNetwork import DBN
import glob


dbn = DBN(3, 39, [100, 100, 50], 6, 1, 1e-3)
#
#print(rbm.weights)



'''
The English language has 44 sounds, which can be encoded in a 
64-dim binary vector. That means we can use 6 output binary
neurons to encode the 44 classes. 
'''

analyzer = AudioAnalyzer.AudioAnalyzer()
features = analyzer.normalized_feature_vector('OSR_us_000_0061_8k.wav')

filenames = glob.glob('three\*.wav')

features = []

for i in range(len(filenames)):
    if  i % 100 == 0:
        print(i)
    features += analyzer.normalized_feature_vector(filenames[i])

print(len(features))
dbn.train(features, 5)

#current example of a word is three
#its phone representation is θriː, meaning it has 3 phonemes
#we could take a list of feature vectors representing those 3 phonemes
#and divide it into 3 parts, with each part representing a probability distribution 
#over the single phone. Then, we could average them


