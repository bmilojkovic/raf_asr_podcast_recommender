import os
from os import path
import random
from os import listdir
from os.path import isfile, join

def mock1(audio):
    if random.randint(0,100) < 56:
        return "water"
    else:
        return "book"
    

#PARAMETRI: ###############################################################################
path_dataset = r'C:\Users\Luka\Desktop\dataset'  #Treba da se poklapa sa path_dataset iz download_test_files.py
allow_specific_words = True      #ako je true, testira samo reci iz liste specific_words         
allow_specific_gender = False    #ako je true, testira samo pol iz liste specific_gender
allow_specific_locations = False  #ako je true, testira samo pol iz liste specific_locations
specific_words = ['water','book']
specific_gender = ['Male']
specific_locations = ['United Kingdom']

###########################################################################################

audio_count = 0
all_words = None
locations = None

all_right = 0
male_right = 0
female_right = 0
location_right = {}
word_right = {}

word_count = {}
male_count = 0
female_count = 0
location_count = {}



if allow_specific_words :
    all_words = specific_words
else:
    all_words = os.listdir(path_dataset)
    
for word in all_words:
    if allow_specific_gender:
        genders = specific_gender
    else:    
        genders = os.listdir(path_dataset+"\\"+word)
    for gender in genders:
        if allow_specific_locations:
            locations = specific_locations
        else:
            locations = os.listdir(path_dataset+"\\"+word+'\\'+gender)
        for location in locations:
            audio_files = [f for f in listdir(path_dataset+"\\"+word+'\\'+gender+'\\'+location) if isfile(join(path_dataset+"\\"+word+'\\'+gender+'\\'+location, f))]
            audio_count += len(audio_files)
            for audio_file in audio_files:  
                if location not in location_count:
                    location_count.setdefault(location,1)
                    location_right.setdefault(location,0)
                else:
                    location_count[location] += 1
                if word not in word_count:
                    word_count.setdefault(word,1)
                    word_right.setdefault(word,0)
                else:
                    word_count[word] += 1
                if gender == "Male":
                    male_count+=1
                else:
                    female_count+=1
                #OVDE TREBA UCITATI PRAVI AUDIO FILE I PROSLEDITI U NAREDNOJ FUNKCIJI PRAVI AUDIO_FILE
                #
                #  promenljiva audio_file ovde je samo naziv file-a
                #  path to tog file bice: path_dataset+"\\"+word+'\\'+gender+'\\'+location+"\\"+audio_file
                #
                ###################################################################################################  
                if word == mock1(audio_file):
                    all_right+=1
                    if gender == "Male":
                        male_right+=1
                    else:
                        female_right+=1

                    old = location_right.get(location)+1
                    location_right[location] += 1
                    word_right[word] += 1


all_accuracy = float((100*all_right)/audio_count)
locations = [key for key in location_count.keys()];
words = [key for key in word_count.keys()];

        
print("Words that are tested: "+str(all_words))

if allow_specific_gender:
    print("Specific gender: " + specific_gender[0])
print("Locations: "+ str(locations))
print("Number of tested files: " + str(audio_count))
print("Accuracy of all tested files: " + str(all_accuracy)+"%")
print("Accuracy by gender: ")
if allow_specific_gender and specific_gender[0]== 'Male':
    male_accuracy = float((100*male_right)/male_count)
    print("  Male count :" + str(male_count))
    print("  Male acc: " + str(male_accuracy)+"%")
else:
    if allow_specific_gender and specific_gender[0]== 'Female':
        female_accuracy = float((100*female_right)/female_count)
        print("  Female count :" + str(female_count))
        print("  Female acc: " + str(female_accuracy)+"%")
    else:
        male_accuracy = float((100*male_right)/male_count)
        female_accuracy = float((100*female_right)/female_count)
        print("  Male count :" + str(male_count))
        print("  Male acc: " + str(male_accuracy)+"%")
        print("  Female count :" + str(female_count))
        print("  Female acc: " + str(female_accuracy)+"%")
print("Accuracy by locations: ")
for location in locations:
    location_accuracy = float((100*location_right[location])/location_count[location])
    print("  "+ location+ " -count: "+ str(location_count[location])+"; acc: "+ str(location_accuracy)+"%" )
print("Accuracy by words: ")    
for word in words:
    word_accuracy = float((100*word_right[word])/word_count[word])
    print("  "+ word+ " -count: "+ str(word_count[word])+"; acc: "+ str(word_accuracy)+"%" )




