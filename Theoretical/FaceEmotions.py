import pygame as pg
import math


screen_size = (800, 480)
screen = pg.display.set_mode(screen_size)

pg.display.set_caption("Ekko Robot Assistant")

running = True
clock = pg.time.Clock()

origin = pg.Vector2(screen_size[0]*0.5, screen_size[1]*0.5,)

eyeSprite = pg.image.load("./Assets/Eye.png")
closedEyeRightSprite = pg.image.load("./Assets/ClosedRight.png")
closedEyeLeftSprite = pg.image.load("./Assets/ClosedLeft.png")
pupilSprite = pg.image.load("./Assets/Pupil.png")
eyebrowRight = pg.image.load("./Assets/EyebrowRight.png")
eyebrowLeft = pg.image.load("./Assets/EyebrowLeft.png")
mouthSpriteHappy = pg.image.load("./Assets/MouthHappy.png")
mouthSpriteSad = pg.image.load("./Assets/MouthSad.png")

sizes = {
    "eye": pg.Vector2(236/2, 237/2),
    "pupil": pg.Vector2(170/2, 170/2),
    "mouth": pg.Vector2(171/2, 70/2),
    "eyeClosed": pg.Vector2(262/2, 206/2),
    "eyeBrow": pg.Vector2(91/2, 86/2),
}


def debugLines():
    pg.draw.line(screen, "red", (origin.x, 0), (origin.x, origin.y*2), 1)
    pg.draw.line(screen, "red", (0, origin.y), (origin.x*2, origin.y), 1)


def drawEyes(position: pg.Vector2, open: bool = True):
    if open:
        screen.blit(eyeSprite, (origin - sizes["eye"] + position))
        screen.blit(eyeSprite, (origin -
                    sizes["eye"] + pg.Vector2(-1 * position.x, 1 * position.y)))
    else:
        screen.blit(closedEyeLeftSprite,
                    (origin - sizes["eyeClosed"] + position))
        screen.blit(closedEyeRightSprite, (origin -
                    sizes["eyeClosed"] + pg.Vector2(-1 * position.x, 1 * position.y)))
    pass


def drawPupils(position: pg.Vector2):
    screen.blit(pupilSprite, (origin - sizes["pupil"] + position))
    screen.blit(pupilSprite, (origin -
                sizes["pupil"] + pg.Vector2(-1 * position.x, 1 * position.y)))
    pass


def drawEyeborws(position: pg.Vector2):
    screen.blit(eyebrowLeft, (origin - sizes["eyeBrow"] + position))
    screen.blit(eyebrowRight, (origin -
                sizes["eyeBrow"] + pg.Vector2(-1 * position.x, 1 * position.y)))
    pass


def drawMouth(position: pg.Vector2, happy: bool = True):
    if happy:
        screen.blit(mouthSpriteHappy, (origin - sizes["mouth"] + position))
    else:
        screen.blit(mouthSpriteSad, (origin - sizes["mouth"] + position))
    pass


def drawEmotion(emotion):
    drawEyes(emotion[0], emotion[1])
    if emotion[1]:
        drawPupils(emotion[2])

    drawMouth(emotion[3], emotion[4])
    if emotion[6]:
        drawEyeborws(emotion[5])


emotions = {
    "idle": [pg.Vector2(-200, -0), 1, pg.Vector2(-180, -0), pg.Vector2(0, 100), True, pg.Vector2(-120, -130), 0],
    "happy": [pg.Vector2(-190, -50), 0, pg.Vector2(-160, -70), pg.Vector2(0, 80), True, pg.Vector2(-120, -130), 0],
    "sad": [pg.Vector2(-200, 10), 1, pg.Vector2(-180, 50), pg.Vector2(0, 120), False, pg.Vector2(-120, -130), 0],
    "angry": [pg.Vector2(-200, -0), 1, pg.Vector2(-180, -0), pg.Vector2(0, 100), False, pg.Vector2(-100, -120), 1],
}


def easeOutExpo(x: float):
    if x >= 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


def lerp(A: int, B: int, t: float):
    return A + t * (B - A)


def lerpVector(A: pg.Vector2, B: pg.Vector2, t: float):
    return pg.Vector2(lerp(A.x, B.x, t), lerp(A.y, B.y, t))


def lerpEmotion(A, B, t):
    return [lerpVector(A[0], B[0], t),
            round(lerp(A[1], B[1], t)),
            lerpVector(A[2], B[2], t),
            lerpVector(A[3], B[3], t),
            round(lerp(A[4], B[4], t)),
            lerpVector(A[5], B[5], t),
            round(lerp(A[6], B[6], t))
            ]


def changeEmotion(target="idle"):
    global frame
    global lastEmotion
    global currentEmotion
    frame = 0
    lastEmotion = currentEmotion
    currentEmotion = target


frame = 0
animLength = 200

lastEmotion = "idle"
currentEmotion = "happy"


def runFaceDisplay():
    global running
    global frame
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_1:
                        changeEmotion("idle")
                    case pg.K_2:
                        changeEmotion("happy")
                    case pg.K_3:
                        changeEmotion("sad")
                    case pg.K_4:
                        changeEmotion("angry")

        screen.fill((37, 58, 55))

        e = lerpEmotion(emotions[lastEmotion], emotions[currentEmotion],
                        easeOutExpo(frame/animLength))

        drawEmotion(e)

        pg.display.flip()
        frame += 1
