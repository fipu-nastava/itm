import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.utils import np_utils

global seq_length, max_seq_length, files_path

seq_length = 10
max_seq_length = 50
files_path = "./application/files/"


def read_file(filename):
    global files_path

    return open(files_path + filename).read()


def save_file(content, filename):
    global files_path

    with open(files_path + filename, "w") as file:
        file.write(content)


def tokenize_words(input):

    input = input.lower()

    tokenizer = RegexpTokenizer(r"\w+")

    out = ""
    for i in input.split("\n"):
        filtered = filter(lambda token: token not in stopwords.words("english"), tokenizer.tokenize(i))
        out += " ".join(filtered) + "\n"

    return out


def train():

    global seq_length, files_path

    file = read_file("tasks.txt")
    processed_inputs = tokenize_words(file)

    chars = sorted(list(set(processed_inputs)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))

    save_file(",".join(chars), "chars.txt")

    input_len = len(processed_inputs)
    vocab_len = len(chars)

    x_data = []
    y_data = []

    for i in range(0, input_len - seq_length, 1):

        in_seq = processed_inputs[i:i + seq_length]
        out_seq = processed_inputs[i + seq_length]

        x_data.append([char_to_num[char] for char in in_seq])
        y_data.append(char_to_num[out_seq])

    n_patterns = len(x_data)

    X = np.reshape(x_data, (n_patterns, seq_length, 1))
    X = X/float(vocab_len)

    y = np_utils.to_categorical(y_data)

    # Model
    model = Sequential()
    model.add(LSTM(128, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(64))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam")

    try:
        model = load_model(files_path + "task_model.h5")
    except:
        pass

    model.fit(X, y, epochs=2000, batch_size=128, verbose=2)

    model.save(files_path + "task_model.h5")


def predict(input):

    global seq_length, max_seq_length

    out = input
    input = input.lower()

    assert len(input) >= seq_length, "Min input size must be {0}".format(seq_length)

    model = load_model(files_path + "task_model.h5")

    chars = read_file("chars.txt").split(",")
    vocab_len = len(chars)
    num_to_char = dict((i, c) for i, c in enumerate(chars))
    char_to_num = dict((c, i) for i, c in enumerate(chars))

    input = [char_to_num[char] for char in input][:seq_length]

    for i in range(max_seq_length - len(input)):

        x = np.reshape(input, (1, len(input), 1))
        x = x / float(vocab_len)

        prediction = model.predict(x, verbose=0)

        index = np.argmax(prediction)
        result = num_to_char[index]

        #seq_in = [num_to_char[value] for value in input]
        #print(seq_in, result)

        input.append(index)
        input = input[1:len(input)]

        out += result

    return out.split("\n")[0]