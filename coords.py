import cv2

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Clicked at ({x}, {y})')
        with open('clicked_x.txt', 'a') as file:
            file.write(f"{x},")
        with open('clicked_y.txt', 'a') as file:
            file.write(f"{y},")
        cv2.circle(imgS, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image', imgS)
    elif event == cv2.EVENT_RBUTTONDOWN:
        with open('clicked_x.txt', 'a') as file:
            file.write(f"|")
        with open('clicked_y.txt', 'a') as file:
            file.write(f"|")
        cv2.circle(imgS, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow('image', imgS)


if __name__ == '__main__':
    img = cv2.imread('original.png', 1)
    imgS = cv2.resize(img, None, fx=2.0, fy=2.0)
    cv2.imshow('image', imgS)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()