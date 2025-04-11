import threading
import pygame as pg

background_color = (7, 144, 199)

# initialize pygame
pg.init()

screen_size = (800, 480)

screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Ekko Robot Assistant")


# create a window

# clock is used to set a max fps
clock = pg.time.Clock()

origin = pg.Vector2(screen_size[0]*0.5, screen_size[1]*0.5,)

features = {

    # Eye assets
    "eye": pg.image.load("./Assets/eye.png"),
    "eye_closed_left": pg.image.load("./Assets/closed_eye_left.png"),
    "eye_closed_right": pg.image.load("./Assets/closed_eye_right.png"),
    "eye_calm_up": pg.image.load("./Assets/eye_calm_up.png"),
    "eye_calm_down": pg.image.load("./Assets/eye_calm_down.png"),
    "pupil": pg.image.load("./Assets/pupil.png"),

    # Mouth Assets
    "mouth_neutral": pg.image.load("./Assets/neutral_mouth.png"),
    "mouth_sad": pg.image.load("./Assets/sad_mouth.png"),
    "mouth_happy": pg.image.load("./Assets/happy_mouth.png"),

    # Eyeborw Assets
    "eyebrow_angry_left": pg.image.load("./Assets/angry_eyebrow_left.png"),
    "eyebrow_angry_right": pg.image.load("./Assets/angry_eyebrow_right.png"),
    "eyebrow_calm_left": pg.image.load("./Assets/calm_eyebrow_left.png"),
    "eyebrow_calm_right": pg.image.load("./Assets/calm_eyebrow_right.png"),

    # Other
    "blush": pg.image.load("./Assets/blush.png"),
}

# Size of the assets
sizes = {}
for feature_name in features:
    current_feature_value = features[feature_name]
    sizes[feature_name] = pg.Vector2(
        current_feature_value.get_width()/2, current_feature_value.get_height()/2)

# Interpolation Functions


def easeOutExpo(x: float):
    if x >= 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


def lerp(A: int, B: int, t: float):
    return A + t * (B - A)


def lerpVector(A: pg.Vector2, B: pg.Vector2, t: float):
    return pg.Vector2(lerp(A.x, B.x, t), lerp(A.y, B.y, t))


def lerpValue(A: int, B: int, t: float):
    return A if t < 0.5 else B


def lerpEmotion(A: dict, B: dict, t: float):
    resultingEmotion = {}

    for feature_name in A:
        featureA = A[feature_name]
        featureB = B[feature_name]
        interpolated_feature = lerpValue(featureA, featureB, t) if type(
            featureA) is int else lerpVector(featureA, featureB, t)
        resultingEmotion[feature_name] = interpolated_feature
    return resultingEmotion

# Drawing the emotions


def drawEmotion(emotion: dict):
    # Drawing the blush
    if emotion["blush_enabled"]:
        blush_pos = emotion["blush_position"]
        screen.blit(features["blush"],
                    blush_pos - sizes["blush"] + origin)
        screen.blit(features["blush"],
                    pg.Vector2(blush_pos.x * -1, blush_pos.y) - sizes["blush"] + origin)

    # Drawing the eyes
    eye_pos = emotion["eye_position"]
    eye_type = emotion["eye_type"]
    if eye_type == 0:
        screen.blit(features["eye"],
                    eye_pos - sizes["eye"] + origin)
        screen.blit(features["eye"],
                    pg.Vector2(eye_pos.x * -1, eye_pos.y) - sizes["eye"] + origin)
    elif eye_type == 1:
        screen.blit(features["eye_closed_left"],
                    eye_pos - sizes["eye_closed_right"] + origin)
        screen.blit(features["eye_closed_right"],
                    pg.Vector2(eye_pos.x * -1, eye_pos.y) - sizes["eye_closed_right"] + origin)
    elif eye_type == 2:
        screen.blit(features["eye_calm_up"],
                    eye_pos - sizes["eye_calm_up"] + origin)
        screen.blit(features["eye_calm_up"],
                    pg.Vector2(eye_pos.x * -1, eye_pos.y) - sizes["eye_calm_up"] + origin)
    else:
        screen.blit(features["eye_calm_down"],
                    eye_pos - sizes["eye_calm_down"] + origin)
        screen.blit(features["eye_calm_down"],
                    pg.Vector2(eye_pos.x * -1, eye_pos.y) - sizes["eye_calm_down"] + origin)

    # Drawing the pupils
    if eye_type == 0:
        pupil_pos = emotion["pupil_position"]
        screen.blit(features["pupil"],
                    pupil_pos - sizes["pupil"] + origin)
        screen.blit(features["pupil"],
                    pg.Vector2(pupil_pos.x * -1, pupil_pos.y) - sizes["pupil"] + origin)

    # Drawing the mouth

    mouth_pos = emotion["mouth_position"]
    mouth_type = emotion["mouth_type"]
    if mouth_type == 0:
        mouth_asset = "mouth_neutral"
    elif mouth_type == 1:
        mouth_asset = "mouth_happy"
    else:
        mouth_asset = "mouth_sad"
    screen.blit(features[mouth_asset],
                mouth_pos - sizes[mouth_asset] + origin)

    # Drawing the eyebrows
    if emotion["eyebrow_angry_enabled"]:
        eyebrow_pos = emotion["eyebrow_angry_position"]
        screen.blit(features["eyebrow_angry_left"],
                    eyebrow_pos - sizes["eyebrow_angry_left"] + origin)
        screen.blit(features["eyebrow_angry_right"],
                    pg.Vector2(eyebrow_pos.x * -1, eyebrow_pos.y) - sizes["eyebrow_angry_right"] + origin)

    if emotion["eyebrow_calm_enabled"]:
        eyebrow_pos = emotion["eyebrow_calm_position"]
        screen.blit(features["eyebrow_calm_left"],
                    eyebrow_pos - sizes["eyebrow_calm_left"] + origin)
        screen.blit(features["eyebrow_calm_right"],
                    pg.Vector2(eyebrow_pos.x * -1, eyebrow_pos.y) - sizes["eyebrow_calm_right"] + origin)


# Emotion Data
emotions = {
    # Template for other emotions
    "defautlt": {
        "eye_position": pg.Vector2(-200, 0),
        "eye_type": 0,
        "pupil_position": pg.Vector2(-180, 0),

        "mouth_position": pg.Vector2(0, 150),
        "mouth_type": 0,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -150),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -190),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    "smile": {
        "eye_position": pg.Vector2(-200, -20),
        "eye_type": 0,
        "pupil_position": pg.Vector2(-185, -25),

        "mouth_position": pg.Vector2(0, 130),
        "mouth_type": 1,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    "ecxited": {
        "eye_position": pg.Vector2(-180, -20),
        "eye_type": 1,
        "pupil_position": pg.Vector2(-180, -40),

        "mouth_position": pg.Vector2(0, 100),
        "mouth_type": 1,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    "happy": {
        "eye_position": pg.Vector2(-200, -50),
        "eye_type": 2,
        "pupil_position": pg.Vector2(-180, -70),

        "mouth_position": pg.Vector2(0, 120),
        "mouth_type": 1,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    # Used when waiting for a command
    "idle": {
        "eye_position": pg.Vector2(-200, 20),
        "eye_type": 0,
        "pupil_position": pg.Vector2(-180, 30),

        "mouth_position": pg.Vector2(0, 150),
        "mouth_type": 0,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    # Used when his name is called

    "sad": {
        "eye_position": pg.Vector2(-200, 0),
        "eye_type": 0,
        "pupil_position": pg.Vector2(-185, 15),

        "mouth_position": pg.Vector2(0, 150),
        "mouth_type": 2,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },


    "angry": {
        "eye_position": pg.Vector2(-200, 0),
        "eye_type": 0,
        "pupil_position": pg.Vector2(-180, 10),

        "mouth_position": pg.Vector2(0, 160),
        "mouth_type": 2,

        "eyebrow_angry_enabled": 1,
        "eyebrow_angry_position": pg.Vector2(-90, -150),
        "eyebrow_calm_enabled": 0,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 350),
    },

    "blush": {
        "eye_position": pg.Vector2(-200, -20),
        "eye_type": 2,
        "pupil_position": pg.Vector2(-180, -10),

        "mouth_position": pg.Vector2(0, 140),
        "mouth_type": 1,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 1,
        "eyebrow_calm_position": pg.Vector2(-330, -170),

        "blush_enabled": 1,
        "blush_position": pg.Vector2(-300, 150),
    },

    "pensive": {
        "eye_position": pg.Vector2(-200, 30),
        "eye_type": 3,
        "pupil_position": pg.Vector2(-180, 10),

        "mouth_position": pg.Vector2(0, 160),
        "mouth_type": 0,

        "eyebrow_angry_enabled": 0,
        "eyebrow_angry_position": pg.Vector2(-90, -190),
        "eyebrow_calm_enabled": 1,
        "eyebrow_calm_position": pg.Vector2(-300, -150),

        "blush_enabled": 0,
        "blush_position": pg.Vector2(-300, 150),
    },

}

last_emotion = "blush"
current_emotion = "pensive"


def changeEmotion(newEmotion):
    global last_emotion, current_emotion, current_frame

    if not newEmotion == current_emotion:
        last_emotion = current_emotion
        current_emotion = newEmotion
        current_frame = 0


animation_length = 120  # frames
current_frame = 0


def flipEmotion():
    global last_emotion, current_emotion, current_frame
    temp = last_emotion
    last_emotion = current_emotion
    current_emotion = temp
    current_frame = 0


def drawDebugInfo():
    pass


running = True


def runFaceDisplay():
    global running, current_frame, animation_length

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

        # clear the screen
        screen.fill(background_color)

        # draw to the screen
        interpolated_emotion = lerpEmotion(
            emotions[last_emotion], emotions[current_emotion], easeOutExpo(current_frame/animation_length))

        drawEmotion(emotion=interpolated_emotion)

        # flip() updates the screen to make our changes visible
        pg.display.flip()

        if current_frame < animation_length:
            current_frame += 1

        # how many updates per second
        clock.tick(60)

    pg.quit()


faceThread = threading.Thread(target=runFaceDisplay())
faceThread.start()
