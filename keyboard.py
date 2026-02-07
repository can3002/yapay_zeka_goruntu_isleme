import cv2
import numpy as np

# Boş bir tuval (keyboard için)
keyboard = np.zeros((1000, 1500, 3), np.uint8)
keys_set_1 = {0: "Q", 1: "W", 2:"E", 3:"R", 4:"T"}
def letter(letter_index, letter):
    # dikdörtgen ayarları
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 200
        y = 0
    elif letter_index == 2:
        x = 400
        y = 0
    elif letter_index == 3:
        x = 600
        y = 0
    elif letter_index == 4:
        x = 800
        y = 0
    width = 200
    height = 200
    th = 3
    cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), 3)

    # yazı ayarları
    font_letter = cv2.FONT_HERSHEY_PLAIN
    text = letter  # dışarıdan gelen parametre kullanılacak
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)


# Örnek kullanım
letter(0, 0, "A")
letter(200, 0, "B")
letter(400, 0, "C")

cv2.imshow("Keyboard", keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
