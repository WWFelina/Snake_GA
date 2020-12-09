from game import * 
from generate_training import generate_training
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

def neural_net(x,y):
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 42)

    y1 = y_train
    encoder = LabelEncoder()
    encoder.fit(y1)
    y1 = encoder.transform(y1)
    # convert integers to dummy variables (i.e. one hot encoded)
    y1 = np_utils.to_categorical(y1)
    print(y1)

    model = Sequential()
    model.add(Dense(5, input_dim=4, activation= 'relu'))
    model.add(Dense(4, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    history = model.fit(x_train, y1, epochs=100, batch_size=32)
    return model
    #y_pred = model.predict_classes(x_test)
    #print(y_pred)
    #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

def random_forest(x,y):
    y = pd.get_dummies(y)
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state = 42)
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(x_train,y_train)
    y_pred=clf.predict(x_test)
    #print(y_pred)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    return clf


x,y = generate_training(10000)
x = pd.DataFrame(x)
y = pd.DataFrame(y)

model = neural_net(x,y)
for _ in range(5):
    #model = neural_net(x,y)
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
    for i in range(500):
        clock.tick(30)
        test = [[snake.positions[0][0], snake.positions[0][1],food.position[0],food.position[1]]]
        #move = model.predict_classes(pd.DataFrame(test))
        move = model.predict_classes(pd.DataFrame(test))
        snake.random_movement(move)
        #snake.handle_keys()
        drawGrid(surface)
        snake.move()
        # == 1 or dead == 2:
         #   break
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
