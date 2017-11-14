from pico2d import *
import random
from Unit_Class import *
from Object_Class import *
import game_framework
import title_state
import pause_state

name = "MainState"

current_time = 0.0

mx = 0
my = 0
ms = 0
build = True

card_type = 0
card_no = 0

TIME = 0
Gold = 120
Human_Score = 0
Orc_Score = 0

selection = -1

cursor = None
click = False

back_frame = None
commandbar = None
qwer = None
sqwer = None
numbers = None
unitselect = None

enemyList = []
peasantList= []
unitList = []
buildingList= []
cardList = []
numList = [0,1,2,3,4]

map = None

timer = 0

def TIMER():
    global TIME
    TIME = int(get_time())

# 숫자그리는 함수(변수,좌표)
def draw_number(A,x,y):

    i = 10
    Num = []
    count =0
    font = load_image('Images\\numbers.png')
    if A == 0:
        font.clip_draw(0 * 20, 0, 20, 20, x, y)
    else:
        while A != 0:
            a = A % i
            Num.append(a)
            A = (A - a) // 10
            count += 1

        for n in range(count):
            font.clip_draw(Num[n] * 20, 0, 20, 20, x - 10 * n, y)

# 카드 그리기
def draw_cards():
    global cardList
    #current
    for i in range(4):
        cardList[i].image.clip_draw(cardList[i].type * 60, 0, 60,80,70,350 - cardList[i].no*100)
    #next
    cardList[4].image.clip_draw(cardList[4].type*60,0,60,80,70,440,40,60)

# 카드 초기 설정
def init_cards():
    global numList,cardList,card_type,card_no

    for i in range(5):
        x = random.randint(0,len(numList)-1)
        card_type = numList[x]
        card_no = i
        card = Card()
        cardList.append(card)
        numList.remove(card_type)

# 카드 바꾸기
def change_card():
    global selection, cardList,numList, card_no,card_type, Gold

    numList.append(cardList[selection].type)
    Gold -= cardList[selection].cost
    cardList[selection].type = cardList[4].type
    del (cardList[4])
    x = random.randint(0, len(numList) - 1)
    card_type = numList[x]
    card_no = 4
    card = Card()
    cardList.append(card)
    numList.remove(card_type)

# 유닛 빌드여부
def unit_build():##
    global mx,my,selection, cardList, unitselect, build,Gold

    if mx > 150 and mx < 530 and my < 300 and my > 120 and Gold >= cardList[selection].cost:
        build = True
    else:
        build = False

    if selection != -1:
        unitselect.clip_draw(50 * (cardList[selection].type - 1), 50 - 50*build, 50, 50, mx, my,40,40)

def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def collide(a, b):
    # fill here
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return  False
    if right_a < left_b: return False
    if top_a < bottom_b: return  False
    if bottom_a > top_b: return  False

    return True

def range_collide(ra, b):
    left_a,bottom_a,right_a,top_a = ra.get_rb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return  False
    if right_a < left_b: return False
    if top_a < bottom_b: return  False
    if bottom_a > top_b: return  False

    return True

def agro_collide(ra,rb):
    left_a, bottom_a, right_a, top_a = ra.get_rb()
    left_b, bottom_b, right_b, top_b = rb.get_rb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def create_world():
    global peasantList, commandbar, qwer, sqwer, unitselect, back_frame, cursor, cardList, card_type, card_no, \
        enemyList

    # 시작 일꾼
    peasant = Peasant()
    peasantList.append(peasant)

    # 시작 건물 배치
    tower1 = orc_Tower1()
    tower2 = orc_Tower2()
    enemyList.append(tower1)
    enemyList.append(tower2)

    castle = orc_Castle()
    enemyList.append(castle)
    castle = human_Castle()
    unitList.append(castle)
    buildingList.append(castle)

    tower1 = human_Tower1()
    tower2 = human_Tower2()
    unitList.append(tower1)
    unitList.append(tower2)
    buildingList.append(tower1)
    buildingList.append(tower2)

    # 시작 카드 설정
    init_cards()

    back_frame = load_image('back.png')
    commandbar = load_image('commandbar_frame.png')
    qwer = load_image('qwer.png')
    sqwer = load_image('sqwer.png')
    unitselect = load_image('unitselect.png')
    cursor = load_image('Images\\cursor.png')


def destroy_world():
    global cursor, back_frame

    del (back_frame)
    del (cursor)


def enter():
    create_world()


def exit():
    destroy_world()


def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    global mx,my,click,unitselect,build,peasantList,Gold,ATK,DEF,selection,card_type,card_no

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION :
            mx = event.x
            my = 720 - event.y
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_p:
                game_framework.push_state(pause_state)

            elif event.key == SDLK_q:
                if selection == 0:
                    selection = -1
                else:
                    selection= 0
                    if Gold >= cardList[selection].cost:
                        # 일꾼
                        if cardList[selection].type == 0:
                            peasant = Peasant()
                            peasantList.append(peasant)
                            change_card()
                            selection = -1


            elif event.key == SDLK_w:
                if selection == 1:
                    selection = -1
                else:
                    selection = 1
                    if Gold >= cardList[selection].cost:
                        # 일꾼
                        if cardList[selection].type == 0:
                            peasant = Peasant()
                            peasantList.append(peasant)
                            change_card()
                            selection = -1

            elif event.key == SDLK_e:
                if selection == 2:
                    selection = -1
                else:
                    selection = 2
                    if Gold >= cardList[selection].cost:
                        # 일꾼
                        if cardList[selection].type == 0:
                            peasant = Peasant()
                            peasantList.append(peasant)
                            change_card()
                            selection = -1

            elif event.key == SDLK_r:
                if selection == 3:
                    selection = -1
                else:
                    selection = 3
                    if Gold >= cardList[selection].cost:
                        # 일꾼
                        if cardList[selection].type == 0:
                            peasant = Peasant()
                            peasantList.append(peasant)
                            change_card()
                            selection = -1

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                click = True
                if selection != -1 and build == True:
                    if cardList[selection].type == 1:
                        unit = Footman()
                        unitList.append(unit)
                        change_card()
                        selection = -1
                    elif cardList[selection].type == 2:
                        unit = Archer()
                        unitList.append(unit)
                        change_card()
                        selection = -1
                    elif cardList[selection].type == 3:
                        unit = Knight()
                        unitList.append(unit)
                        change_card()
                        selection = -1
                    elif cardList[selection].type == 4:
                        unit = Mage()
                        unitList.append(unit)
                        change_card()
                        selection = -1


        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                click = False


def update(frame_time):
   TIMER()

   if TIME % 5 == 0 and get_time() - TIME > 0.01 and get_time() - TIME < 0.03:
        grunt = Grunt()
        enemyList.append(grunt)
        troll = Troll()#
        enemyList.append(troll)
        ogre = Ogre()
        enemyList.append(ogre)
        death = Death_kinght()
        enemyList.append(death)

   for enemy in enemyList:
        enemy.update(frame_time)

   for unit in unitList:
       unit.update(frame_time)

   for peasant in peasantList:
       peasant.update(frame_time)


def draw_scene():

    back_frame.draw(290, 340, 580, 680)
    commandbar.draw(60, 340, 120, 680)
    qwer.draw(60,250)
    draw_number(TIME, 80, 630)

    draw_number(Human_Score, 90, 580)
    draw_number(Orc_Score, 90, 550)
    draw_number(Gold, 90, 520)

    draw_cards()

    if selection > -1:
        sqwer.clip_draw(0, 300 - 100*selection , 120, 100, 60, 350 - 100*selection)

    #for enemy in enemyList:
    #    enemy.draw()
    #    enemy.draw_bb()
    #    enemy.draw_rb()

    for i in range(len(enemyList)):
        enemyList[-i].draw()
        #enemyList[-i].draw_bb()
        #enemyList[-i].draw_rb()

    for unit in unitList:
        unit.draw()
        #unit.draw_bb()
        #unit.draw_rb()

    for building in buildingList:
        building.draw()

    for peasant in peasantList:
        peasant.draw()

    unit_build()

    # 커서는 최후방

    cursor.clip_draw(click * 50, 0, 50, 50, mx, my, 40, 40)


def draw(frame_time):
    clear_canvas()
    draw_scene()
    update_canvas()




