import random
import json
import pickle #for serialization
import numpy as np
import nltk#natural language processing toolkit
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer #reduces the words to its stem to not loose any performance effieciency
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD #for stochastic gradient descent 


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
#create 3 empty lists
words =[]
classes = []
documents =[]
ignore_letters = ['?','!','.',','] #characters that we are not really going to consider
for intent in intents['intents']:   # we are considering intents as a 
  for pattern in intent['patterns']:
    word_list = nltk.word_tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list,intent['tag']))
    if intent['tag'] not in classes:
      classes.append(intent['tag'])


print(documents)
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words)) #removing duplicates and sorting

print(words)
classes = sorted(set(classes))
pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))
training  = []
ouput_empty = [0]*len(classes)
for document in documents:
  bag = []
  word_patterns = document[0]
  word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
  for word in words :
    bag.append(1) if word in word_patterns else bag.append(0)
  output_row = list(ouput_empty)
  output_row[classes.index(document[1])] = 1
  training.append([bag, output_row])




random.shuffle(training)
training = np.array(training)
#features and labels
train_x = list(training[:, 0])
train_y = list(training[:, 1])
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation= 'relu')) #relu activation function used
model.add(Dropout(0.5)) #prevents overfitting
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))  #softmax scales all the output such that the sum is 1




#defining a SGD optimizer
sgd = SGD(lr = 0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist =  model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose = 1)
model.save('chatbot_model.model.h5, hist')
print("Done")


import random
import json
import pickle #for serialization
import numpy as np
import nltk#natural language processing toolkit
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer 
from tensorflow.keras.models import load_model
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('/content/chatbot_model.model.h5, hist')


def clean_up_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
  return sentence_words 

  
def bag_of_words(sentence):
  sentence_words = clean_up_sentence(sentence)
  bag = [0] * len(words)
  for w in sentence_words:
    for i, word in enumerate(words):
      if word == w:
        bag[i] = 1
  return np.array(bag)
  

def predict_class(sentence):
  bow = bag_of_words(sentence)
  res = model.predict(np.array([bow]))[0]
  ERROR_THRESHOLD = 0.25
  result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
  result.sort(key = lambda x: x[1], reverse=True)
  return_list = [] 
  for r in result:
    return_list.append({'intent' : classes[r[0]], 'probability': str(r[1])})
  return return_list


def get_response(intents_lists, intents_json):
  tag = intents_lists[0]['intent']
  list_of_intents = intents_json['intents']
  for i in list_of_intents:
    if i['tag'] == tag:
      result = random.choice(i['responses'])
      break
  return result

print("Hello user!The bot is running")
i=0
while i <7:
    message = input()
    ints = predict_class(message)
    res = get_response(ints,intents)
    i+=1
    if i<=6:
      print(res)
print("Thank you for your responses\n")
print("You will be redirected to a doctor for further consultation and prescription(if needed)")