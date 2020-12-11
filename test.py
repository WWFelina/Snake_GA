from game import * 
#from generate_training import generate_training
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE

def neural_net(x_train,x_test,y_train,y_test):
    encoder = LabelEncoder()
    encoder.fit(y_train)
    y_train = encoder.transform(y_train)
    y_train = np_utils.to_categorical(y_train)
    model = Sequential()
    model.add(Dense(4, input_dim=5, activation= 'relu'))
    model.add(Dense(5, activation= 'relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=50, batch_size=64)
    return model

def random_forest(x_train,x_test,y_train,y_test):
    model=RandomForestClassifier(n_estimators=100)
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    return model

def svm(x_train,x_test,y_train,y_test):
    sv = SVC()
    sv.fit(x_train, y_train)
    return sv

def run_game(model,flag):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    clock.tick(10)
    drawGrid(surface)
    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("monospace",32)
    while True:
        clock.tick(30)
        test = [[snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1],snake.length]]
        if flag == 1:
            move = model.predict_classes(pd.DataFrame(test))
        elif flag == 2:
            move = model.predict(pd.DataFrame(test))
        snake.random_movement(move)
        drawGrid(surface)
        score = snake.score
        death = snake.move()
        if death:
            return score
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            #pygame.mixer.music.load('eat_sound.mp3')
            #pygame.mixer.music.play(0)
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        pygame.display.update()

#y_test = [np.where(r==1)[0][0] for r in y_test]

data = pd.read_csv('data2.csv')
x = data.iloc[:,:5]
y = data.iloc[:,5:]
oversample = SMOTE()
x, y = oversample.fit_resample(x, y)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state = 42)

'''model = svm(x_train,x_test,y_train,y_test)
score = 0
for _ in range(20):
    score += run_game(model,2)
y_pred = model.predict(x_test)
print("SVM Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Confusion Matrix : ", confusion_matrix(y_test, y_pred))
print("SVM Average Score:",score/20)


model = random_forest(x_train,x_test,y_train,y_test)
score = 0
for _ in range(20):
    score += run_game(model,2)
y_pred = model.predict(x_test)
print("Random Forest Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Confusion Matrix : ", confusion_matrix(y_test, y_pred))
print("Random Forest Average Score:",score/20)'''

model = neural_net(x_train,x_test,y_train,y_test)
score = 0
for _ in range(20):
    score += run_game(model,1)
y_pred = model.predict_classes(x_test)
print("Neural Network Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Confusion Matrix : ", confusion_matrix(y_test, y_pred))
print("Neural Net Average Score:",score/20)
