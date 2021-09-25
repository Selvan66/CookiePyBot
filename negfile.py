import os

def make_neg_file():
    with open('negWorm.txt', 'w') as f:
        for filename in os.listdir('HaarCascade/Worm/Negative'):
            f.write('HaarCascade/Worm/Negative/' + filename + '\n')