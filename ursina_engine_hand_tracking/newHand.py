from ursina import *
import cv2
import mediapipe as mp

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(max_num_hands=2)

# ---------------- URSINA ----------------
app = Ursina()
cube = Entity(model='cube', scale=3, color=color.azure)

# ---------------- STATE ----------------
held_by = None
prev_pos = None
smooth_pos = None

PINCH_THRESHOLD = 0.035
MOVE_MULT = 10
ROT_MULT = 200
SMOOTHING = 0.8   # ↑ arttıkça daha stabil

# ---------------- UPDATE ----------------
def update():
    global held_by, prev_pos, smooth_pos

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hands_data = []

    if results.multi_hand_landmarks:
        for i, hand in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            thumb = hand.landmark[4]
            index = hand.landmark[8]
            wrist = hand.landmark[0]
            mcp = hand.landmark[5]

            pinch = abs(index.x - thumb.x)

            palm_x = (wrist.x + mcp.x) / 2
            palm_y = (wrist.y + mcp.y) / 2

            hands_data.append({
                "label": label,
                "pinch": pinch,
                "palm": (palm_x, palm_y),
                "index": (index.x, index.y)
            })

    grabbing = [h for h in hands_data if h["pinch"] < PINCH_THRESHOLD]

    if grabbing:
        active = next((h for h in grabbing if h["label"] == held_by), grabbing[0])
        held_by = active["label"]

        x, y = active["palm"]

        # --- smoothing ---
        if smooth_pos is None:
            smooth_pos = (x, y)
            prev_pos = smooth_pos
            return

        sx = smooth_pos[0] * SMOOTHING + x * (1 - SMOOTHING)
        sy = smooth_pos[1] * SMOOTHING + y * (1 - SMOOTHING)

        dx = sx - prev_pos[0]
        dy = sy - prev_pos[1]

        dx = clamp(dx, -0.05, 0.05)
        dy = clamp(dy, -0.05, 0.05)

        cube.x += dx * MOVE_MULT
        cube.y -= dy * MOVE_MULT

        cube.rotation_y -= dx * ROT_MULT
        cube.rotation_x += dy * ROT_MULT

        smooth_pos = (sx, sy)
        prev_pos = smooth_pos

    else:
        held_by = None
        prev_pos = None
        smooth_pos = None

    cv2.imshow("Hand Control", frame)

# ---------------- EXIT ----------------
def input(key):
    if key == 'escape':
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

app.run()
