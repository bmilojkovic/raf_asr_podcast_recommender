import yake
import csv
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#path = '/home/milos/RAF_HAKATON/data/questions.csv'
language = "en"
max_ngram_size = 1
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20


def read_file(path):
    text = ""

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in csv_reader:
            if first_line:
                first_line = False
            else:
                text += str(row[2])
                
    return text

def extract_keywords(text):
    #text = read_file(path)
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords


def remove_verbs(keywords):
    verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
    verbs = []
    final = []
    for kw in keywords:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(kw[0]))):
                    if pos in verb_tags:
                        verbs.append(word)
    for kw in keywords:
        if kw[0] not in verbs:
            final.append(kw)

    return final

def extract(text):
    #text = read_file(path)
    keywords = extract_keywords(text)
    final = remove_verbs(keywords)
    
    return final

if __name__ == "__main__":
    #main()
    pass























