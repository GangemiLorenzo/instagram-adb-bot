import os
import random
import warnings
from enum import Enum
from time import sleep
from typing import List

import numpy as np
from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import match_template
from skimage.io import imread

warnings.filterwarnings("ignore")

DEBUG = False

#Gives the app more time to load content
SLOWSPEED = 0

SHORTSLEEP = 3.0 + SLOWSPEED*5.0
LONGSLEEP = 6.0 + SLOWSPEED*10.0

#Topic
class Topic(Enum):
    ALL = 1
    HASHTAG = 2
    ACCOUNT = 3
    PLACE = 4

class Device:
    def __init__(self, h=0, w=0):
        self.height = h
        self.width = w

#OS-ONLY FUNCTIONS _______________________________________________________________________

def _getScreenSize():
    os.system("adb shell wm size")
    res = os.popen('adb shell wm size').read()[15:].strip().split('x')
    return [int(res[0]), int(res[1])]


def _getScreen(d: Device):
    os.system("adb exec-out screencap -p > screen.png")
    _mySleep(SHORTSLEEP)
    im = Image.open('screen.png')
    left = 0
    top = 0
    right = d.width
    bottom = d.height - 20
    im1 = im.crop((left, top, right, bottom))
    im1.save('screen.png', 'png')

def _getCoordinates(ref: str, d: Device):
    _getScreen(d)
    image = imread('screen.png')
    template = imread(ref)
    image_gray = rgb2gray(image)
    template_gray = rgb2gray(template)
    result = match_template(image_gray, template_gray)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]
    #Here I can handle some offsets
    x = x + 0
    y = y + 0
    return [x,y]

def _mySleep(sec:float):
    rnd = random.uniform(-0.5, 0.5)
    if(DEBUG):
            print('sleep: ', sec + rnd)
    sleep(sec + rnd)

def _tap(x:int, y:int):
    if(DEBUG):
            print('tap | x:',x,' | y:',y)
    os.system("adb shell input tap " + str(x) + " " + str(y))

def _swipeVertical(l:int):
    if(DEBUG):
            print('vertical swipe: ',l)
    os.system("adb shell input swipe 540 " + str(l) + " 540 10 500")

def _clickOn(ref: str, d: Device):
    [x,y] = _getCoordinates(ref, d)
    _tap(x,y)


def _textInput(text: str):
    if(DEBUG):
            print('text input: ', text)
    os.system("adb shell input keyboard text " + "\"" + text + "\"")
    _mySleep(SHORTSLEEP)

def _osHome():
    os.system("adb shell input keyevent 3")

def _osSquare():
    os.system("adb shell input keyevent 187")

def _osBack():
    os.system("adb shell input keyevent 4")

def _clearConsole():
    os.system("clear")

#INSTAGRAM-BASIC FUNCTIONS _______________________________________________________________________

class InstagramBot:
    def __init__(self):
        size = _getScreenSize()
        self.device = Device(h=size[1], w=size[0])
        _clearConsole()
        print('Bot initiated')
        print('Screen size:', self.device.height, 'x', self.device.width)

    def openInstagram(self):
        if(DEBUG):
            print('open instagram')
        os.system("adb shell monkey -p com.instagram.android 1 -")
        _mySleep(LONGSLEEP)

    def closeInstagram(self):
        if(DEBUG):
            print('close instagram')
        os.system("adb shell am force-stop com.instagram.android")
        _mySleep(LONGSLEEP)

    def clickFirstResultList(self):
        if(DEBUG):
            print('click first result list')
        x = (self.device.width / 2)
        y = 0.188*self.device.height
        _tap(x,y)
        _mySleep(SHORTSLEEP)

    def clickFirstResultGrid(self):
        if(DEBUG):
            print('click first result list')
        x = (self.device.width / 6) * 1
        y = 0.36*self.device.height
        os.system("adb shell input tap " + str(x) + " " + str(y))
        _mySleep(SHORTSLEEP)

    def clickSearchTextbox(self):
        if(DEBUG):
            print('click search textbox')
        _clickOn('./riferimenti/search_textbox.png', self.device)
        _mySleep(SHORTSLEEP)

    def clickHashtag(self):
        if(DEBUG):
            print('click hashtag')
        _clickOn('./riferimenti/hashtag_button.png', self.device)
        _mySleep(SHORTSLEEP)

    def clickSearch(self):
        if(DEBUG):
            print('click search icon')
        _clickOn('./riferimenti/search_icon.png', self.device)
        _mySleep(SHORTSLEEP)

    def clickRecenti(self):
        if(DEBUG):
            print('click recenti')
        _clickOn('./riferimenti/recenti_button.png', self.device)
        _mySleep(LONGSLEEP)

    def clickHome(self):
        if(DEBUG):
            print('click Home')
        _clickOn('./riferimenti/home_icon.png', self.device)
        _mySleep(SHORTSLEEP)

    def clickSeguiti(self):
        if(DEBUG):
            print('click seguiti')
        _clickOn('./riferimenti/seguiti.png', self.device)
        _mySleep(LONGSLEEP)

    def clickUtentiConCuiHaiInteragitoDiMeno(self):
        if(DEBUG):
            print('click utenti con cui hai interagito di meno')
        _clickOn('./riferimenti/utenti_da_sfolloware.png', self.device)
        _mySleep(SHORTSLEEP)

    def clickMyProfile(self):
        x = (self.device.width / 10) * 9
        y = self.device.height - 150
        _tap(x,y)
        _mySleep(SHORTSLEEP)


    #INSTAGRAM-COMPLEX FUNCTIONS _______________________________________________________________________

    #Cerca un termine, va in recenti e apre il feed a partire dal primo post
    def searchFor(self, term:str, type: Topic):
        self.clickSearch()
        self.clickSearchTextbox()
        _textInput(term)
        if type == Topic.HASHTAG:
            self.clickHashtag()
        self.clickFirstResultList()
        self.clickRecenti()
        self.clickFirstResultGrid()

    #Mette un like, se le coordinate hanno senso riporta la Y, altrimenti riporta 0
    def putLike(self):
        [x,y] = _getCoordinates('./riferimenti/heart_icon.png', self.device)
        if 0 <= x <= (0.12*self.device.width) and (0.12*self.device.height) <= y <= (0.88*self.device.height):
            _tap(x,y)
            print("Like effettuato!")
            _mySleep(SHORTSLEEP)
            return y
        else:
            print("Like non effettuato")
            return 0

    #Mette Like, scorre verticalmente, ripete per n volte
    def likesTrain(self, n_likes: int):
        n = 0
        n_mis = 0
        while n < n_likes:
            if n_mis == n_likes * 2:
                return n, n_mis
            try:
                y = self.putLike()
                if y == 0:
                    n_mis = n_mis + 1
                    y = (self.device.height/2)
                else:
                    n = n + 1
                _swipeVertical(y)
                _mySleep(SHORTSLEEP)
            except Exception as e:
                print(str(e))
                return n, n_mis
        return n, n_mis

    #Esegue un treno di like ad ogni elemento di una lista di Hashtag
    def likeTags(self, tags: list, n: int):
        self.closeInstagram()
        self.openInstagram()
        for tag in tags:
            _clearConsole()
            print("Eseguo " + str(n) + " like al tag: " + tag)
            self.searchFor(tag, Topic.HASHTAG)
            self.likesTrain(n)
            self.closeInstagram()
            self.openInstagram()
