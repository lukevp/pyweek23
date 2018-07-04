from pygame.locals import *

#display settings
width = 1920
height = 1080
screen_setting = FULLSCREEN | HWSURFACE | DOUBLEBUF

# Keyboard settings
quitkeys = [K_ESCAPE]
downkeys = [K_DOWN, K_s]
upkeys = [K_UP, K_w]
leftkeys = [K_LEFT, K_a]
rightkeys = [K_RIGHT, K_d]
jumpkeys = [K_SPACE]
swapkeys = [K_UP, K_RETURN]



#don't change any of this unless you want to watch the world burn.
FONT_ROOT = "assets/fonts/"

IMAGE_ROOT = "assets/images/"

#don't change this.
GAME_WIDTH = 1920 # half of 4K width
GAME_HEIGHT = 2160 # 4K height

def reload_scores():
    global highscores
    highscores = []
    f = file("highscores.txt")
    for line in f.readlines():
        highscores.append((line.split("|")[0], int(line.split("|")[1].strip())))
    f.close()

def update_scores(newscores):
    # only accept the top 10 scores.
    newscores = newscores[:10]
    scorefile = file("highscores.txt", "w")
    for score in newscores:
        scorefile.write(score[0] + "|" + str(int(score[1])) + "\n")
    scorefile.close()
    reload_scores()

reload_scores()
highscores
