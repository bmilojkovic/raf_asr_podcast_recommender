#input data should be in the format of an array
#[minutes:ss:hshs]word[minutes:ss:hshs].....
#minutes == string of 1, 2, 3...numbers representing minutes
#ss == seconds
#ms == hundreds of a second

#program mode == WHOLE (anayze whole transcript) or PARTIAL (find all occurences for 10 words) 


def parse_word(word):
    pos = word.index('[')
    word = word[pos + 1:]
    
    pos = word.index(':')
    starting_minutes = word[0:pos]
    word = word[pos + 1:]

    pos = word.index(':')
    starting_seconds = word[0:pos]
    word = word[pos + 1:]

    pos = word.index(']')
    starting_hundedths = word[0:pos]
    word = word[pos + 1:]

    pos = word.index('[')
    word_out = word[0:pos]
    word = word[pos + 1:]

    pos = word.index(':')
    ending_minutes = word[0:pos]
    word = word[pos + 1:]

    pos = word.index(':')
    ending_seconds = word[0:pos]
    word = word[pos + 1:]

    pos = word.index(']')
    ending_hundedths = word[0:pos]
    word = word[pos + 1:]

    return [starting_minutes, starting_seconds, starting_hundedths, word_out, ending_minutes, ending_seconds, ending_hundedths]

    


def complete_analysis(ref_file, tested_file):


    ref_file_words = []
    tested_file_words = []


    print("Populating lists with words...")
    for line in ref_file:
        #line might contain spaces, we should remove them
        line.replace(" ", "")
        pos = 0
        pos_prev = 0
        nmb = 0
        for char in line:
            if (char == "[" or char == "]") and nmb < 4:
                nmb = nmb + 1
            if nmb  == 4:
                nmb = 0
                ref_file_words.append(line[pos_prev:pos + 1])
                pos_prev = pos + 1 
            pos = pos + 1

    for line in tested_file:
        #line might contain spaces, we should remove them
        line.replace(" ", "")
        pos = 0
        pos_prev = 0
        nmb = 0
        for char in line:
            if (char == "[" or char == "]") and nmb < 4:
                nmb = nmb + 1
            if nmb  == 4:
                nmb = 0
                tested_file_words.append(line[pos_prev:pos + 1])
                pos_prev = pos + 1 
            pos = pos + 1

    print("Complete.")
    
    ctcw = 0 #correct time, correct word
    wtww = 0 #wrong time, wrong word
    ctww = 0 #correct time, wrong word
    wtcw = 0 #wrong time, correct word


    pos = 0
    untested_words = 0

    print("Caluclation efficiency...")
    for word in ref_file_words:
        if pos == len(tested_file_words):
            untested_words = untested_words + (len(ref_file_words) - len(tested_file_words))
            break;
        
        smr, ssr, shr, wr, emr, esr, ehr = parse_word(word)
        smt, sst, sht, wt, emt, est, eht = parse_word(tested_file_words[pos])

        if wr == wt and smr == smt and sst == sst and shr == sht:
            ctcw = ctcw + 1
            pos = pos + 1
        elif wr == wt and not (smr == smt and sst == sst and shr == sht):
            wtcw = wtcw + 1
            pos = pos + 1
        elif wr != wt and smr == smt and sst == sst and shr == sht:
            ctww = ctww + 1
            pos = pos + 1
        else:
            #wrong word and wrong time
            #most likely the tested program didn't recognize the word
            #so we should skip the current word in refferential list
            untested_words = untested_words + 1
            wtww = wtww + 1
            continue
    print("Done.\n\n\n")

    total = len(ref_file_words)
    print("Total number of words tested:", total)
    print("Total number of words in ref file untested:", untested_words, " or:", untested_words/total * 100, "%")
    print("Correct words with correct timestamp:", ctcw, " or:", ctcw/total * 100, "%")
    print("Correct words with wrong timestamp:", wtcw, " or:", wtcw/total * 100, "%")
    print("Wrong words with correct timestamp:", ctww, " or:", ctww/total * 100, "%")
    print("Wrong words with wrong timestamp:", wtww, " or:", wtww/total * 100, "%")




def find_words(ref_file, tested_file):
    ref_file_words = []
    tested_file_words = []

    print("Populating lists with words...")
    for line in ref_file:
        #line might contain spaces, we should remove them
        line.replace(" ", "")
        pos = 0
        pos_prev = 0
        nmb = 0
        for char in line:
            if (char == "[" or char == "]") and nmb < 4:
                nmb = nmb + 1
            if nmb  == 4:
                nmb = 0
                ref_file_words.append(line[pos_prev:pos + 1])
                pos_prev = pos + 1 
            pos = pos + 1

    for line in tested_file:
        line.strip()
        tested_file_words.append(line)
    print("Complete.")

    for word in tested_file_words:
        if word[len(word) - 1] == '\n':
            word = word[0: len(word) - 1] #to remove trailing newline
        print('Word: "' + word + '" appears in the following positions: ') 
        for word2 in ref_file_words:
            smr, ssr, shr, wr, emr, esr, ehr = parse_word(word2)
            if word == wr:
                print("Beginning at:", smr, ":", ssr, ":", shr, "  Ending at:", emr, ":", esr, ":", ehr)
    
    





ref_file_name = input("Referential transcript: ")
tested_file_name = input("Tested transcript: ")

program_mode = input("Program mode(type COMPLETE or FIND_WORDS): ") 

print("Opening ref file....")
ref_file = open(ref_file_name, "r")
print("Complete.")

print("Opening tested file....")
tested_file = open(tested_file_name, "r")
print("Complete.")





if program_mode == "COMPLETE":
    complete_analysis(ref_file, tested_file)
elif program_mode == "FIND_WORDS":
    find_words(ref_file, tested_file)
else:
    print("Wrong command.")
        

        




















    
        
        
