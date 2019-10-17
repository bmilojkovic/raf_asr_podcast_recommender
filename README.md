# TESTER

The following program acts as a tester, compating a referential timestamped transcript
with one provided by the tested program. The tester has two modes:
  COMPLETE: the tester compares two textual files, giving as an output
  the following data:
      number of total words in referential file 
      number of words in referential file untested
      number of correct words with correct timestamp
      number of incorrect words with correct timestamp
      number of correct words with incorrect timestamp
      number of incorrect words with incorrect timestamp
  
  As input the program takes the names of the referential and tested files, and the command COMPLETE
  in given order. 
  The data in both the referential and tested files should be in the following format:
  [minutes:ss:hh]word[minutes:ss:hh] (hh == hundredth of a second)
  
  FIND_WORDS: the tester finds the position of the words from the tested file in the referential
  file, giving as the output the following data:
      word tested
      list of all the occurences of that word (its timestamps)
      
  The data in the referential file should be in the following format:
  [minutes:ss:hh]word[minutes:ss:hh]
  while the tested file should contain a list of n words in separate lines.
  
  Example1:
  (input)
    ref.txt
    test4.txt
    COMPLETE
    
    
  Example2:
  (input)
    ref.txt
    words.txt
    FIND_WORDS
    
    
  
