import pygame, sys, sqlite3
from pygame.locals import *



#Variable Globales
FPS = 200
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
ANCHO = 10
LARGO = 50
SEPARACION = 20
NEGRO = (0,0,0)
BLANCO = (255,255,255)

class Pong:
    def pintarTerreno(self):
        Surface.fill((0,0,0))
        pygame.draw.line(Surface, BLANCO,
                         ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (ANCHO/4))

    def pintarPalas(self, pala):
        if pala.bottom > WINDOWHEIGHT:
            pala.bottom = WINDOWHEIGHT
        elif pala.top < 0:
            pala.top = 0
        pygame.draw.rect(Surface, BLANCO, pala)

    def pintarBola(self, bola):
        pygame.draw.rect(Surface, BLANCO, bola)

    def moverBola(self, bola, dirX, dirY):
        bola.x += dirX
        bola.y += dirY
        return bola

    def colisionBola(self, bola, dirX, dirY):
        if bola.top == 0 or bola.bottom == WINDOWHEIGHT:
            dirY = dirY * -1
        if bola.left == 0 or bola.right == WINDOWWIDTH:
            dirX = dirX * -1
        return dirX, dirY


    def IA(self, bola, dirX, pala2):
        #If ball is moving away from paddle, center bat
        if dirX == -1:
            if pala2.centery < (WINDOWHEIGHT/2):
                pala2.y += 1
            elif pala2.centery > (WINDOWHEIGHT/2):
                pala2.y -= 1
        #if ball moving towards bat, track its movement.
        elif dirX == 1:
            if pala2.centery < bola.centery:
                pala2.y += 1
            else:
                pala2.y -=1
        return pala2

    def colisionPala(self, bola, pala1, pala2, dirX):
        if dirX == -1 and pala1.right == bola.left and pala1.top < bola.top and pala1.bottom > bola.bottom:
            return -1
        elif dirX == 1 and pala2.left == bola.right and pala2.top < bola.top and pala2.bottom > bola.bottom:
            return -1
        else: return 1

    def calcularPuntuacion(self, bola, pala1, pala2, dirX, puntuacion):
        cursor.execute('''SELECT MAX(points) from highscores''')
        hs = cursor.fetchone()
        highscore = hs[0]
        if bola.left == 0:
            cursor.execute('''INSERT INTO highscores(points) VALUES(?)''', (puntuacion,))
            return 0, highscore
        elif dirX == -1 and pala1.right == bola.left and pala1.top < bola.top and pala1.bottom > bola.bottom:
            puntuacion += 5
            return puntuacion, highscore
        elif bola.right == WINDOWWIDTH:
            puntuacion += 50
            return puntuacion, highscore
        else:return puntuacion, highscore

    def mostrarPuntuacion(self, puntuacion):
        newsurf = Font.render('Score = %s' %(puntuacion), True, BLANCO)
        newrect = newsurf.get_rect()
        newrect.topleft = (WINDOWWIDTH - 80, 15)
        Surface.blit(newsurf, newrect)

    def mostrarHighscore(self, highscore):
        newsurf = Font.render('Highscore = %s' %(highscore), True, BLANCO)
        newrect = newsurf.get_rect()
        newrect.topleft = (WINDOWWIDTH - 80, 30)
        Surface.blit(newsurf, newrect)



def main():
    pong = Pong()
    db = sqlite3.connect("data.mydb")
    pygame.init()
    global Surface, Font, FontSize, cursor
    FontSize = 10
    Font = pygame.font.Font('freesansbold.ttf', FontSize)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS highscores(id INTEGER PRIMARY KEY, points INTEGER)''')

    Clock = pygame.time.Clock()
    Surface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    bolaX = WINDOWWIDTH/2 - ANCHO/2
    bolaY = WINDOWHEIGHT/2 - ANCHO/2
    playerOnePosition = (WINDOWHEIGHT - LARGO) /2
    playerTwoPosition = (WINDOWHEIGHT - LARGO) /2

    dirX = -1
    dirY = -1

    dirUP = 0
    dirDOWN = 0

    puntuacion = 0
    highscore = 0

    pala1 = pygame.Rect(SEPARACION,playerOnePosition, ANCHO,LARGO)
    pala2 = pygame.Rect(WINDOWWIDTH - SEPARACION - ANCHO, playerTwoPosition, ANCHO,LARGO)
    bola = pygame.Rect(bolaX, bolaY, ANCHO, ANCHO)


    pong.pintarTerreno()
    pong.pintarPalas(pala1)
    pong.pintarPalas(pala2)
    pong.pintarBola(bola)


    while True:
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    dirDOWN = 1
                elif event.key == K_UP:
                    dirUP = 1
                elif event.key == K_ESCAPE:
                    db.commit()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_c:
                    cursor.execute('''DELETE FROM highscores ''')
            if event.type == KEYUP:
                dirUP = 0
                dirDOWN = 0


        if dirUP == 1:
            pala1.y -= 3
        if dirDOWN == 1:
            pala1.y += 3

        bola = pong.moverBola(bola,dirX,dirY)
        dirX,dirY = pong.colisionBola(bola,dirX,dirY)
        puntuacion,highscore = pong.calcularPuntuacion(bola, pala1, pala2, dirX, puntuacion)
        dirX *= pong.colisionPala(bola,pala1,pala2,dirX)
        pala2 = pong.IA(bola, dirX, pala2)



        pong.pintarTerreno()
        pong.pintarPalas(pala1)
        pong.pintarPalas(pala2)
        pong.pintarBola(bola)
        pong.mostrarPuntuacion(puntuacion)
        pong.mostrarHighscore(highscore)
        pygame.display.update()
        Clock.tick(FPS)

if __name__ == '__main__':
    main()


