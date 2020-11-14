# 9.3 Assignment
# load libraries
from pathlib import Path
import os
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Dense
from keras.preprocessing.text import Tokenizer
from keras.layers import LSTM

import numpy as np
import matplotlib.pyplot as plt


# set-up directories
assignment_dir = 'C:/Users/Tim/PycharmProjects/dsc650/dsc650/assignments/assignment09'
results_dir = os.path.join(assignment_dir, 'results')
data_dir = 'C:/Users/Tim/PycharmProjects/dsc650/data/external/imdb/aclImdb'
train_dir = os.path.join(data_dir, 'train')
neg_train_dir = os.path.join(train_dir, 'neg')
pos_train_dir = os.path.join(train_dir, 'pos')
test_dir = os.path.join(data_dir, 'test')
model_2_dir = os.path.join(results_dir, 'model_2')


def process_labels(train_dir):
    # read and process labels of the raw data files
    # initialize empty list for labels
    labels = []
    # initialize empty list for texts/data
    texts = []

    # separate iterations for neg and pos files:
    for label_type in ['neg', 'pos']:
        # set dir name to train dir plus pos or neg
        dir_name = os.path.join(train_dir, label_type)
        # for each file in the neg and pos train dirs
        for fname in os.listdir(dir_name):
            # check whether file name contains .txt
            if fname[-4:] == ".txt":
                # use try/except since about 20 files are causing errors
                try:
                    # open each file (one string per file)
                    f = open(os.path.join(dir_name, fname))
                    # append string sentence to texts list
                    texts.append(f.read())
                    # close file
                    f.close()
                except:
                    print('Error reading file: ', label_type, fname)

                # if negative review then append 0 to list
                if label_type == 'neg':
                    labels.append(0)
                # if positive review then append 1 to list
                else:
                    labels.append(1)

    # return text sentence and labels (pos/neg)
    return(texts, labels)


def tokenize_text(texts, labels):
    # tokenize (convert sentence to words) words and labels
    maxlen = 500 # We will cut reviews after 100 words
    training_samples = 10000  # We will be training on 2000 samples
    validation_samples = 5000  # We will be validating on 10000 samples
    max_words = 10000  # We will only consider the top 10,000 words in the dataset

    # instantiate tokenizer
    tokenizer = Tokenizer(num_words=max_words)
    # fit tokenizer on text data
    tokenizer.fit_on_texts(texts)
    # convert texts to numpy sequence (numeric array)
    sequences = tokenizer.texts_to_sequences(texts)

    # create word index
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    # pad sequences
    data = pad_sequences(sequences, maxlen=maxlen)

    # assign numpy array (neg/pos - 0/1) to labels
    labels = np.asarray(labels)
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)

    # create numpy array for indices
    indices = np.arange(data.shape[0])

    # But first, shuffle the data, since we started from data
    # where sample are ordered (all negative first, then all positive).
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]

    # Split the data into a training set and a validation set
    x_train = data[:training_samples]
    y_train = labels[:training_samples]
    x_val = data[training_samples: training_samples + validation_samples]
    y_val = labels[training_samples: training_samples + validation_samples]

    return maxlen, max_words, x_train, y_train, x_val, y_val


def train_LSTM_model(x_train, y_train, x_val, y_val):
    max_features = 10000
    model = Sequential()
    model.add(Embedding(max_features, 32))
    model.add(LSTM(32))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['acc'])
    history = model.fit(x_train, y_train,
                        epochs=20,
                        batch_size=128,
                        validation_split=0.2)

    # save model and results to model_2_directory
    # serialize model to JSON
    model_json = model.to_json()
    with open(os.path.join(model_2_dir, "model_2.json"), "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(os.path.join(model_2_dir, "model_2.h5"))
    print("Saved LSTM model to disk")

    return model, history

def plot_LSTM_results(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)

    # plot training and validation accuracy curbes
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('LSTM model - Training and validation accuracy')
    plt.legend()

    # save training and validation accuracy curves to results directory
    plt.savefig(os.path.join(model_2_dir, 'model_2.png'))

    plt.show()

    # plot training and validation losses
    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('LSTM model - Training and validation loss')
    plt.legend()

    plt.show()


def main():
    texts, labels = process_labels((train_dir))
    maxlen, max_words, x_train, y_train, x_val, y_val = tokenize_text(texts, labels)
    LSTM_model, LSTM_history = train_LSTM_model(x_train, y_train, x_val, y_val)
    plot_LSTM_results(LSTM_history)


if __name__ == '__main__':
    main()