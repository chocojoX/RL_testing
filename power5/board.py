import numpy as np
import cv2
import copy

class Power5_Board(object):
    def __init__(self, size=10, square_size=60):
        self.size = size
        self.length = square_size*size
        self.square_size = square_size
        self.border_color = [0, 0, 40]
        self.border_width = 2
        self.background = self.generate_background()


    def draw_circle(self, pos, color = (250, 250, 250)):
        x,y = pos
        x = x+1; y=y+1
        pt = (int((x-0.5)*self.square_size), int((y-0.5)*self.square_size))
        cv2.circle(self.background, pt, int(self.square_size*0.3), color, 3)
        return True


    def draw_cross(self, pos, color = (250, 250, 250)):
        x,y = pos
        x = x+1; y=y+1
        # pt = (int((x-0.5)*self.square_size), int((y-0.5)*self.square_size))
        x0 = int(self.square_size*(x-0.1*np.sqrt(2)))
        x1 = int(self.square_size*(x-1+0.1*np.sqrt(2)))
        y0 = int(self.square_size*(y-0.1*np.sqrt(2)))
        y1 = int(self.square_size*(y-1+0.1*np.sqrt(2)))
        cv2.line(self.background, (x0, y0), (x1,y1), color, 3)
        cv2.line(self.background, (x1, y0), (x0,y1), color, 3)
        return True


    def generate_background(self):
        bg = np.zeros((self.length, self.length, 3)).astype(np.uint8)
        bg[:,:,2] += 70
        bg[:,:,1] += 20
        for x in range(1, self.size):
            cv2.line(bg, (self.square_size*x, 0), (self.square_size*x, self.length), self.border_color, self.border_width)
        for y in range(10):
            cv2.line(bg, (0, self.square_size*y), (self.length, self.square_size*y), self.border_color, self.border_width)
        return bg


if __name__=="__main__":
    a = Power5_Board()
    a.draw_circle(a.background, (1,2))
    a.draw_cross(a.background, (2,2))
    cv2.imshow("game", a.background)
    cv2.waitKey(0)
