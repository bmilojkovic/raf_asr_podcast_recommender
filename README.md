# MFCC/GMM/DNN > HMM


## Getting started


Run the following to obtain  this task:
```
git clone https://github.com/bmilojkovic/raf_asr_podcast_recommender.git
git checkout task5
``` 
To install all the required dependencies run:
```bash
cd raf_asr_podcast_recommender
pip install -r requirements.txt
```
To test the currently implemented methods run:

```bash
python mfcc-hmm.py # For mfcc-hmm approach.
python gmm-hmm.py # For gmm-hmm approach.
```

## Data
Directories `data`, `test_audio` and `train_audio` are small datasets of digits and fruit, they are used just to show that algorithms work.

## TODO
The following files are empty

`dnn-hmm.py` - Implement DNN - HMM method

`main.py` - Integrate all algorithms in one place
