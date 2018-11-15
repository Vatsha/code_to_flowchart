import pygame
import pickle
from sys import argv
from node import *


## CONSTANTS ##
SCREEN_SIZE = (800, 800)
NODE_SIZE = (130, 50)
NODE_VSPACE = 40
NODE_HSPACE = 90

NODE_COLOR = 0xffffff00
LINE_COLOR = 0xffffff00
GREEN = 0xFF00FF00
WHITE = 0xFFFFFFFF
BLUE = 0xFF0000FF

NODEW, NODEH = NODE_SIZE
pygame.font.init()
FONT = pygame.font.Font(None, 25)

def rhombus(rect):
    x, y, w, h = tuple(map(int, rect))
    return [[x-3*w//4, y], [x, y-h//2], [x+3*w//4, y], [x, y+h//2]]

def parallelogram(rect):
    x, y, w, h = tuple(map(int, rect))
    return [[x-3*w//4, y+h//2], [x-w//2, y-h//2], [x+3*w//4, y-h//2], [x+w//2, y+h//2]]

def connect(screen, obj, pos, npos):
    if id(obj) in drawn:
        pygame.draw.line(screen, WHITE, pos, drawn[id(obj)], 5)
    else:
        pygame.draw.line(screen, LINE_COLOR, pos, npos, 5)
        draw(obj, screen, *npos)

def draw(obj, screen, x, y):
    if not isinstance(obj, Node):
        raise Exception("I don't know how to draw %s" % str(obj))

    if type(obj) in (StartNode, StopNode):
        pygame.draw.ellipse(screen, BLUE, pygame.Rect(x-NODEW/2, y-NODEH/2, NODEW, NODEH))
    elif type(obj) is Node:
        pygame.draw.rect(screen, NODE_COLOR, pygame.Rect(x-NODEW/2, y-NODEH/2, NODEW, NODEH))
    elif type(obj) in (InputNode, OutputNode):
        pygame.draw.polygon(screen, NODE_COLOR, parallelogram((x, y, NODEW, NODEH)))
    elif type(obj) is ConnectorNode:
        pygame.draw.circle(screen, NODE_COLOR, (x,y), NODEH//2)
    elif type(obj) is ConditionalNode:
        pygame.draw.polygon(screen, GREEN, rhombus((x,y,NODEW,NODEH)))
        drawn[id(obj)] = (x, y-NODEH)
        connect(screen, obj.yes, (x, y), (x+NODE_HSPACE+NODEW, y))
        connect(screen, obj.no, (x, y), (x, y+NODE_VSPACE+NODEH))
    drawn[id(obj)] = (x, y-NODEH)
    if obj.next:
        connect(screen, obj.next, (x, y), (x, y+NODE_VSPACE+NODEH))

    text = FONT.render(obj.text, 1, (255, 0, 0))
    screen.blit(text, (x-NODEW//4,y-NODEH//4))
        

drawn = dict()

if len(argv) < 2:
    print("Usage: pythons %s [flowchart file]" % argv[0])
    raise SystemExit()
begin = pickle.load(open(argv[1], "rb"))


assert pygame.init() == (6, 0)

SCREEN = pygame.display.set_mode((800, 800),pygame.RESIZABLE)
pygame.display.set_caption("Flowchart")
SCREEN.fill((0, 0, 0))
draw(begin, SCREEN, 100, 100)

pygame.display.flip()
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

