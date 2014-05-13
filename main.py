import pygame as py
from pygame.locals import QUIT
from random import randrange
from math import sqrt

ANCHO_PANTALLA = 640
ALTO_PANTALLA = 480

class Celula(object):
	
	def __init__(self, x, y):
		self.color = (255, 32, 43)
		self.radio = 5
		self.x, self.y = x, y
		self.vx, self.vy = 0, 0
		self.velocidad = 3
		self.nuevaPosicion = True
		self.nuevaPosicionX = x
		self.nuevaPosicionY = y
		
	def Render(self, screen):
		py.draw.circle(screen, (self.color), (self.x, self.y), self.radio)
		
	def Update(self):
		self.Mover()
		self.Inteligencia()
		
	def Inteligencia(self):
		if self.x >= self.nuevaPosicionX - self.radio and self.x <= self.nuevaPosicionX + self.radio and self.y >= self.nuevaPosicionY - self.radio and self.y <= self.nuevaPosicionY + self.radio:
			self.nuevaPosicion = True
			self.GenerarNuevaPosicion()
		else:
			if self.x < self.nuevaPosicionX - self.radio:
				self.vx = self.velocidad
			elif self.x > self.nuevaPosicionX + self.radio:
				self.vx = -self.velocidad
			else:
				self.vx = 0
			
			if self.y < self.nuevaPosicionY - self.radio:
				self.vy = self.velocidad
			elif self.y > self.nuevaPosicionY + self.radio:
				self.vy = -self.velocidad
			else:
				self.vy = 0
	
	def Mover(self):
		self.x += self.vx
		self.y += self.vy
			
	def GenerarNuevaPosicion(self):
		self.nuevaPosicionX = randrange(0, ANCHO_PANTALLA)
		self.nuevaPosicionY = randrange(0, ALTO_PANTALLA)
		self.nuevaPosicion = False



class Virus(Celula):
	
	def __init__(self, x, y):
		Celula.__init__(self, x, y)
		self.color = (255, 255, 255)
		self.radio = 3

class GlobuloRojo(Celula):
	def __init__(self, x, y):
		Celula.__init__(self, x, y)
		
		self.infectada = False
		
		self.virusProcesado = False
		self.time = 0
		self.tiempoDeIncubacion = 1000
		
	def Update(self):
		Celula.Update(self)
		self.Temporizador()
		
	def Temporizador(self):
		if self.infectada:
			if py.time.get_ticks() - self.time > self.tiempoDeIncubacion:
				self.virusProcesado = True
		else:
			self.time = py.time.get_ticks()


class OrganizadorPatogenos(object):
	def __init__(self):
		self.patogenos = []
	
	def Render(self, screen):
		for patogeno in self.patogenos:
			patogeno.Render(screen)
	
	def Update(self):
		for patogeno in self.patogenos:
			patogeno.Update()
			
class OrganizadorCelulas(object):
	def __init__(self, patogenos):
		self.celulas = []
		self.CrearCelulas()
		self.patogenos = patogenos
		
	def Render(self, screen):
		for celula in self.celulas:
			celula.Render(screen)
			
	def Update(self):
		for celula in self.celulas:
			celula.Update()
			if celula.virusProcesado:
				self.celulas.remove(celula)
				for i in range(2):
					self.patogenos.patogenos.append(Virus(celula.x, celula.y))
			
	def CrearCelulas(self):
		for i in range(20):
			self.celulas.append(GlobuloRojo(randrange(0, ANCHO_PANTALLA), randrange(0, ALTO_PANTALLA)))

class OrganizadorDeColisiones(object):
	
	def Comprobar(self, celulas, patogenos):
		for celula in celulas:
			for patogeno in patogenos:
				distanciaX = (celula.x - patogeno.x) ** 2
				distanciaY = (celula.y - patogeno.y) ** 2
				distancia = sqrt(distanciaX + distanciaY)
				if distancia - patogeno.radio < celula.radio:
					celula.infectada = True
					patogenos.remove(patogeno)
def main():
	py.init()
	screen = py.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
	py.display.set_caption("Simulador inmunologia")
	
	exit = False
	clear = (175, 17, 28)
	fps = py.time.Clock()
	
	patogenos = OrganizadorPatogenos()
	celulas = OrganizadorCelulas(patogenos)
	colisiones = OrganizadorDeColisiones()
	
	
	while not exit:
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
			if py.mouse.get_pressed()[0]:
				x, y = py.mouse.get_pos()
				patogenos.patogenos.append(Virus(x, y))
				
		screen.fill(clear)
		celulas.Render(screen)
		celulas.Update()
		patogenos.Render(screen)
		patogenos.Update()
		colisiones.Comprobar(celulas.celulas, patogenos.patogenos)
		
		py.display.update()
		fps.tick(60)
	return 0
	
if __name__ == "__main__":
	main()
