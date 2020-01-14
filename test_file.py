# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 13:56:39 2019

@author: sicTa
"""



def print_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds  = (seconds % 3600) % 60
    
    print("Time elapsed:\n", hours, "h\n", minutes, "m\n",seconds, "s\n",)

import AudioAnalyzer
import RestrictedBoltzmannMachine
import DeepBeliefNetwork
import Word

from timeit import default_timer as timer

import numpy as np


analyzer = AudioAnalyzer.AudioAnalyzer()
features = analyzer.normalized_feature_vector('OSR_us_000_0061_8k.wav')
features = np.asarray(features)

print(features.shape[0], features.shape[1])

data_prefix = "data/"
data_locations = "data/testing_list.txt"

print("Opening testing files....")
f = open(data_locations)
cntr = 0
for l in f:
    cntr += 1
print("Files opened. In total, there are", cntr, "files to be parsed.")
x = input("Continue? [Y/N]")

x  = input()

if x.upper() == "N":
    exit()
elif x.upper() == "Y":
    'ROFLMAO'
else:
    x = input("Continue? [Y/N]\n")


total_parsed_files = 0
print("Creating total feature vector....")
start = timer()
f = open(data_locations)
features = []
for line in f:
    total_parsed_files += 1
    line = data_prefix + line
    line = line[0:len(line) - 1]
    features += analyzer.normalized_feature_vector(line)
    
    if total_parsed_files % 100 == 0:
        print("Parsed", total_parsed_files, "files")
    

print("Total feature vector created. Converting to numpy array...")
features = np.asarray(features)
print("Done.")
print("Dimensions---", "Rows:", features.shape[0], "Columns:", features.shape[1])
end = timer()
seconds = end - start
print_time(seconds)


print("Creating a  DBN.")
dbn = DeepBeliefNetwork.DBN(3, [39, 100, 150, 6], 6)
print("DBN created. Training the network. Number of epochs is 1000.")
start = timer()

dbn.train(features, 1000)
end = timer()
seconds = end - start
print("Training completed.")
print_time(seconds)




"""The dbn has been trained. Now, we can begin the classification problem"""

total_parsed_files = 0
words = []
print("Creating word vectors....")
start = timer()
f = open(data_locations)
for line in f:
    total_parsed_files += 1
    line = data_prefix + line
    line = line[0:len(line) - 1]
    helper += analyzer.normalized_feature_vector(line)
    helper = np.asarray(helper)
    
    name = ""
    pos = 0
    while line[pos] != "/":
        name += line[pos]
        pos += 1
    
    word = Word(helper, name)
    
    words.append(word)
    
    if total_parsed_files % 100 == 0:
        print("Parsed", total_parsed_files, "files")
    

print("Word vectors created.")
      
print("Dimensions---", "Word number:", features.shape[0], len(words))
end = timer()
seconds = end - start
print_time(seconds)


"""We will be using a context window of 7 frames"""
context = 5
for i in range(len(words)):
    curr_vector = words[i].return_array()
    curr_name = words[i].return_name()
    
    for j in range(len(curr_vector)):
        x = np.zeros(39)
        cntr = 0
        for k in range(context):
            if i + k < context:
                x += curr_vector[i + k]
                cntr++
            else:
                break
            
        x = x / cntr
        
        print(x) #problem, the network returns neary random data
    










#dbn = DeepBeliefNetwork.DBN(3, [39, 100, 100, 60], 6)
#dbn.train(features, 2000)

'''
rbm = RestrictedBoltzmannMachine.RBM(39, 100)
rbm.contrastive_divergence(features, 2000)
features = rbm.run_visible_probabilities(features)

print(features.shape[0], features.shape[1])


rbm = RestrictedBoltzmannMachine.RBM(100, 100)
rbm.contrastive_divergence(features, 2000)
features = rbm.run_visible_probabilities(features)

print(features.shape[0], features.shape[1])

rbm = RestrictedBoltzmannMachine.RBM(100, 6)
rbm.contrastive_divergence(features, 2000)

'''
