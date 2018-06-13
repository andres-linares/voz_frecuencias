# -*- coding: utf-8 -*-

import pygame, sys, random, time, pickle
from pygame.locals import *
from numpy import *
import threading
import pickle
import pyaudio
from array import array
from queue import Queue, Full
import numpy as np



#@@@@@INICIALIZACION DE FUNCION@@@@@#

#INICIALIZACION DE VARIABLES
def inicializacion():
  global puntaje, snake_x, snake_y, min, max_x, max_y, direccion, dificultad
  puntaje = 0
  snake_x = [170, 155, 140, 125, 110, 95]
  snake_y = [170]*6
  min = 35
  max_x = 420
  max_y = 291
  direccion = 'derecha'
  dificultad = 0.05
  generar_objeto(snake_x[0],snake_y[0])

  
#GENERAR OBJETO
def generar_objeto(snake_x, snake_y):
  global manzana_x, manzana_y, craneo_x, craneo_y
  manzana_x = random.randint(min, max_x-15)
  manzana_y = random.randint(min, max_y-15)
  craneo_x = random.randint(min, max_x-15)
  craneo_y = random.randint(min, max_y-15)
  
  #ahora verificamos que el craneo no se aparezca demasiado cerca de la serpiente para evitar morir de una vez
  while craneo_x >= snake_x-75 and craneo_x <= snake_x+75 or craneo_x >= manzana_x-5 and craneo_x <= manzana_x+20:
    craneo_x = random.randint(min, max_x-15)
  while craneo_y >= snake_y-75 and craneo_y <= snake_y+75 or craneo_y >= manzana_y-5 and craneo_y <= manzana_y+20:
    craneo_y = random.randint(min, max_y-15)

#VER EN PANTALLA
def mostrar():
  puntos = font.render('Puntaje: %d' % (puntaje), True, BLANCO)
  turno = -1
  with open('record/turno.txt', 'r') as archivo:
    turno = int(archivo.read())
  if turno == 1:
    el_jugador = 'Andrés'
  else:
    el_jugador = 'Vanessa'
  turno_jugador = font.render('Turno: %s' % (el_jugador), True, BLANCO)
  surface.blit(sfondo, (0, 0))  
  surface.blit(puntos, (35, 8))
  surface.blit(turno_jugador, (330, 8))
  
  for i in range(1,len(snake_x)):
    surface.blit(snake, (snake_x[i], snake_y[i]))
  if snake_x[0] >= max_x or snake_x[0] < min or snake_y[0] >= max_y or snake_y[0] < min:
    game_over() 
  surface.blit(snake_testa, (snake_x[0], snake_y[0]))
  surface.blit(manzana, (manzana_x, manzana_y))
  surface.blit(craneo, (craneo_x, craneo_y))
  pygame.display.update()
  fpsClock.tick(FPS)
  
#VERIFICAR COLISION CON MANZANA O CRANEO
def colision(snake,objeto):
  colision = 0
  for i in snake:
    for j in objeto:
      if i == j:
        colision = 1
  return colision

def terminar_sesion():
  time.sleep(6)
  pygame.event.clear()
  turno = -1
  with open('record/turno.txt', 'r') as archivo:
    turno = int(archivo.read())
  if turno == 1:
    with open('record/turno.txt', 'w') as archivo:
      archivo.write(str(2))
  else:
    with open('record/turno.txt', 'w') as archivo:
      archivo.write(str(1))
  inicializacion()


#GRABAR RECORD EN EL ARCHIVO DE TEXTO
def escribir():
  record = open("record/record.txt","r")    #Abre el archivo record.txt de solo lectura y lo asigna a la variable de registro
  mejor_puntaje = int(record.read())      #Abre el archivo y lee el mejor puntaje
  record.close()                #cierra el archivo abierto previamente
  #comprueba si el puntaje actual es más alto que el registro actual
  if puntaje > mejor_puntaje:
    record = open("record/record.txt","w")  #Abro el archivo record.txt en modo de escritura y lo asigno a la variable de registro
    record.write(str(puntaje))          #Convierto la variable "puntaje" en una cadena y escribo el contenido en el archivo record.txt
    record.close()              #cierra el archivo abierto previamente
    surface.blit(nuevo_record, (0, 0))
    pygame.display.update()
    terminar_sesion()
    

#PAUSA
def pausa():
  surface.blit(pausa_img, (0, 0))
  pygame.display.update()
    
#GAME OVER
def game_over():
  for i in range(0,len(snake_x)):
    surface.blit(snake, (snake_x[i], snake_y[i]))
  surface.blit(snake_testa, (snake_x[0], snake_y[0]))
  escribir()
  surface.blit(gameover_img, (0, 0))
  pygame.display.update()
  terminar_sesion()

def extraer_caracteristicas(transformacion):
  escalador = (len(transformacion) / 2) / (16000 / 2)
  filtros = []
  filtros.append(sum(transformacion[int(20 * escalador): int(100 * escalador)]))
  filtros.append(sum(transformacion[int(100 * escalador): int(200 * escalador)]))
  filtros.append(sum(transformacion[int(200 * escalador): int(300 * escalador)]))
  filtros.append(sum(transformacion[int(300 * escalador): int(400 * escalador)]))
  filtros.append(sum(transformacion[int(400 * escalador): int(500 * escalador)]))
  filtros.append(sum(transformacion[int(500 * escalador): int(600 * escalador)]))
  filtros.append(sum(transformacion[int(600 * escalador): int(700 * escalador)]))
  filtros.append(sum(transformacion[int(700 * escalador): int(800 * escalador)]))
  filtros.append(sum(transformacion[int(800 * escalador): int(900 * escalador)]))
  filtros.append(sum(transformacion[int(900 * escalador): int(1000 * escalador)]))
  filtros.append(sum(transformacion[int(1000 * escalador): int(1100 * escalador)]))
  filtros.append(sum(transformacion[int(1100 * escalador): int(1200 * escalador)]))
  filtros.append(sum(transformacion[int(1200 * escalador): int(1300 * escalador)]))
  filtros.append(sum(transformacion[int(1300 * escalador): int(1400 * escalador)]))
  filtros.append(sum(transformacion[int(1400 * escalador): int(1500 * escalador)]))
  filtros.append(sum(transformacion[int(1500 * escalador): int(1600 * escalador)]))
  filtros.append(sum(transformacion[int(1600 * escalador): int(1700 * escalador)]))
  filtros.append(sum(transformacion[int(1700 * escalador): int(1800 * escalador)]))
  filtros.append(sum(transformacion[int(1800 * escalador): int(1900 * escalador)]))
  filtros.append(sum(transformacion[int(1900 * escalador): int(2000 * escalador)]))
  return filtros

def podar(nparray):
  min = 0
  max = -1
  for i in range(0, len(nparray)):
      if nparray[i] >= 0.4:
          min = i - 5000
          break
  for i in range(len(nparray) - 1, 0, -1):
      if nparray[i] >= 0.4:
          max = i + 5000
          break
  for i in range(0, len(nparray)):
      if i < min or i > max:
          nparray[i] = 0
  return min, max

def listen():
  clasificador_nombre = None
  with open('clasificadores/clasificador_nombres.clf', 'rb') as archivo:
    clasificador_nombre = pickle.load(archivo)
  stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    output=True,
    frames_per_buffer=512)
  print("diga su nombre:")
  frames = []
  for i in range(0, int(16000 / 512 * 3)):
    data = stream.read(512)
    frames.append(data)
  for frame in frames:
    stream.write(frame, 512)
  raw_data = zeros(int(16000 / 512 * 3) * 512)
  for frame in frames:
    raw_data = append(raw_data, array('h', frame))
  raw_data = raw_data / max(abs(raw_data))
  v_min, v_max = podar(raw_data)
  transformacion = abs(fft.fft(raw_data))
  respuesta = clasificador_nombre.predict(
      np.array(
          extraer_caracteristicas(transformacion)).reshape(1, -1))[0]
  if respuesta == 'andres/andres':
    with open('record/turno.txt', 'w') as archivo:
      archivo.write(str(1))
  else:
    with open('record/turno.txt', 'w') as archivo:
      archivo.write(str(2))



def anadir(nparray):
  tamano = 95232
  recibido = len(nparray)
  faltante = tamano - recibido
  complemento = np.zeros(faltante)
  nparray = np.append(nparray, complemento)
  return nparray


def listen2(stopped, q, stream):
  while True:
    if stopped.wait(timeout=0):
        break
    try:
        pedazo = stream.read(512)
        q.put(array('h', pedazo))
    except Full:
        pass  # discard

def record(stopped, q, a):
  grabando = False
  contador = 0
  segundos = 0.5
  segundos_extra = 0.1
  raw_data = np.array(0)
  clasificador_andres = None
  with open('clasificadores/clasificador_andres.clf', 'rb') as archivo:
    clasificador_andres = pickle.load(archivo)

  cola = Queue(maxsize=int(16000 / 512 * segundos_extra))

  maximo = int(16000 / 512 * segundos)

  while True:
    if stopped.wait(timeout=0):
        break
    chunk = q.get()
    vol = max(chunk)
    if vol >= 18000:
        if grabando == False:
          print("\nComienza a grabar...")
        grabando = True
        #print("TRESHOLD")
    else:
      pass
    if grabando:
      contador += 1
      #print(contador)
      #print(chunk)
      while not cola.empty():
        raw_data = np.append(raw_data, cola.get())
      raw_data = np.append(raw_data, chunk)
      if contador == maximo:
        print("Termina de grabar...")
        raw_data = anadir(raw_data)
        raw_data = raw_data / max(abs(raw_data))
        transformacion = np.abs(np.fft.fft(raw_data))

        escalador = (len(transformacion) / 2) / (16000 / 2)

        filtros = []
        filtros.append(np.sum(transformacion[int(20 * escalador): int(100 * escalador)]))
        filtros.append(np.sum(transformacion[int(100 * escalador): int(200 * escalador)]))
        filtros.append(np.sum(transformacion[int(200 * escalador): int(300 * escalador)]))
        filtros.append(np.sum(transformacion[int(300 * escalador): int(400 * escalador)]))
        filtros.append(np.sum(transformacion[int(400 * escalador): int(500 * escalador)]))
        filtros.append(np.sum(transformacion[int(500 * escalador): int(600 * escalador)]))
        filtros.append(np.sum(transformacion[int(600 * escalador): int(700 * escalador)]))
        filtros.append(np.sum(transformacion[int(700 * escalador): int(800 * escalador)]))
        filtros.append(np.sum(transformacion[int(800 * escalador): int(900 * escalador)]))
        filtros.append(np.sum(transformacion[int(900 * escalador): int(1000 * escalador)]))
        filtros.append(np.sum(transformacion[int(1000 * escalador): int(1100 * escalador)]))
        filtros.append(np.sum(transformacion[int(1100 * escalador): int(1200 * escalador)]))
        filtros.append(np.sum(transformacion[int(1200 * escalador): int(1300 * escalador)]))
        filtros.append(np.sum(transformacion[int(1300 * escalador): int(1400 * escalador)]))
        filtros.append(np.sum(transformacion[int(1400 * escalador): int(1500 * escalador)]))
        filtros.append(np.sum(transformacion[int(1500 * escalador): int(1600 * escalador)]))
        filtros.append(np.sum(transformacion[int(1600 * escalador): int(1700 * escalador)]))
        filtros.append(np.sum(transformacion[int(1700 * escalador): int(1800 * escalador)]))
        filtros.append(np.sum(transformacion[int(1800 * escalador): int(1900 * escalador)]))
        filtros.append(np.sum(transformacion[int(1900 * escalador): int(2000 * escalador)]))

        print("Comienza a clasificar...")
        respuesta = clasificador_andres.predict(np.array(filtros).reshape(1, -1))[0]
        print("Termina de clasificar...")
        print(respuesta)
        if respuesta=='andres/abajo':
          pygame.event.post(voice_down)
        elif respuesta == 'andres/izquierda':
          pygame.event.post(voice_left)
        elif respuesta == 'andres/arriba':
          pygame.event.post(voice_up)
        elif respuesta == 'andres/derecha':
          pygame.event.post(voice_right)


        """
        plt.title(respuesta)
        plt.subplot(3, 1, 1)
        plt.plot(np.linspace(start=0, stop=3*2, num=len(raw_data)), raw_data)
        plt.xlim(0, segundos + segundos_extra)
        plt.xlabel('Segundos')
        plt.ylabel('Amplitud')
        plt.subplot(3, 1, 2)
        plt.plot(np.linspace(start=20,
                   stop=2000,
                   num=len(transformacion[int(20 * escalador):int(2000 * escalador)])),
          transformacion[int(20 * escalador):int(2000 * escalador)])
        plt.xlim(20, 2000)
        plt.xticks(np.arange(0, 2100, step=100))
        plt.xlabel('Hertz')
        plt.ylabel('Potencia')
        plt.subplot(3, 1, 3)
        plt.bar(range(1, 21), filtros)
        plt.xlim(1, 20)
        plt.xticks(np.arange(1, 21, step=1))
        plt.xlabel('Caracteristicas')
        plt.ylabel('Potencia')
        plt.show()
        """
        

        raw_data = np.array(0)
        contador = 0
        grabando = False
      else:
        cola.put(chunk)
  
#@@@@@SETUP@@@@@#

#Decidir turno dependiendo a a la voz:
listen()

stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=512,
)
stopped = threading.Event()
q = Queue(maxsize=int(round(10))) #Cola con tamaño máximo de 10 chunks
a = None


"""
try:
  while True:
      listen_t.join(0.1)
      record_t.join(0.1)
except KeyboardInterrupt:
    stopped.set()

listen_t.join()
record_t.join()
"""



pygame.init()
pygame.mixer.music.load("sonidos/music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)




#CONFIGURAR FPS
FPS = 5
fpsClock = pygame.time.Clock()




#CONFIGURAR FUENTE
font = pygame.font.Font(None, 24)

#CONFIGURAR LAS DIMENSIONES DE LA VENTANA
size_w = 460
size_h = 339

#INICIALIZAR COLORES
BLANCO = (255, 255, 255)
GIALLO = (255, 255, 51)
VERDE = (0, 200, 0)
VERDE_SCURO = (0, 100 , 0)
CELESTE = (0, 255, 255)

#CONFIGURAR LA DIMENSIÓN Y EL NOMBRE DE LA VENTANA
surface = pygame.display.set_mode((size_w, size_h))
pygame.display.set_caption('Culebrita')

#CARGAR IMAGENES
sfondo = pygame.image.load("imagenes/sfondo.png")
gameover_img = pygame.image.load("imagenes/gameover.png")
nuevo_record = pygame.image.load("imagenes/nuevo_record_italiano.png")
manzana = pygame.image.load("imagenes/manzana.png")
craneo = pygame.image.load("imagenes/craneo.png")
pausa_img = pygame.image.load("imagenes/pausa.png")

#CREAR SERPIENTE
snake = pygame.Surface((14, 14))
snake_testa = pygame.Surface((14, 14))
snake.fill(VERDE_SCURO)
snake_testa.fill(VERDE)

#INICIO PROGRAMMA
inicializacion()

VOICE_DOWN = USEREVENT + 1
voice_down = pygame.event.Event(VOICE_DOWN, message='Down')
VOICE_UP = USEREVENT + 2
voice_up = pygame.event.Event(VOICE_UP, message='Down')
VOICE_LEFT = USEREVENT + 3
voice_left = pygame.event.Event(VOICE_LEFT, message='Down')
VOICE_RIGHT = USEREVENT + 4
voice_right = pygame.event.Event(VOICE_RIGHT, message='Down')


listen_t = threading.Thread(target=listen2, args=(stopped, q, stream))
listen_t.start()
record_t = threading.Thread(target=record, args=(stopped, q, a))
record_t.start()



while True:
  dificultad = 0.20 - 0.01 * puntaje
  if dificultad < 0:
	  dificultad = 0
  #time.sleep(dificultad)

  mostrar()
  #Añadir acá los eventos de voces
  for event in pygame.event.get():
    if event.type == QUIT:
      game_over()
    elif event.type == KEYDOWN:
      if ((event.key == K_RIGHT or event.key == K_d) and direccion != 'izquierda'):
        direccion = 'derecha'
      elif ((event.key == K_LEFT or event.key == K_a) and direccion != 'derecha'):
        direccion = 'izquierda'
      elif ((event.key == K_DOWN or event.key == K_s) and direccion != 'arriba'):
        direccion = 'abajo'
      elif ((event.key == K_UP or event.key == K_w) and direccion != 'abajo'):
        direccion = 'arriba'
      elif event.key == K_p:
        direccion = '0'
      elif event.key == K_ESCAPE:
        game_over()
    elif event.type == VOICE_DOWN and direccion != 'arriba':
      direccion = 'abajo'
    elif event.type == VOICE_UP and direccion != 'abajo':
      direccion = 'arriba'
    elif event.type == VOICE_LEFT and direccion != 'derecha':
      direccion = 'izquierda'
    elif event.type == VOICE_RIGHT and direccion != 'izquierda':
      direccion = 'derecha'
  
  if direccion == '0':
    pausa()   
        
  else:
    #ALGORITMO PARA EL MOVIMIENTO DE LA SERPIENTE
    i = len(snake_x)-1
    while i>0:
      snake_x[i] = snake_x[i-1]   #el bloque del cuerpo toma las coordenadas del bloque anterior
      snake_y[i] = snake_y[i-1]
      i -= 1          #disminuir el índice para controlar otro bloque
    i=len(snake_x)-1
    #VERIFICAR SI LA SERPIENTE SE MUERDE  
    while i>2:
      if snake_x[0] == snake_x[i] and snake_y[0] == snake_y[i]:
        game_over()
      i -= 1
    
    #MOVER LA SERPIENTE
    else:
      if direccion == 'derecha':
        snake_x[0] += 15
      elif direccion == 'izquierda':
        snake_x[0] -= 15
      elif direccion == 'abajo':
        snake_y[0] += 15
      elif direccion == 'arriba':
        snake_y[0] -= 15
    
    #RANGO PARA COLISIONES CON OBJETOS
    x = range(snake_x[0],snake_x[0]+14)
    y = range(snake_y[0],snake_y[0]+14)
    x2 = range(manzana_x,manzana_x+18)
    y2 = range(manzana_y,manzana_y+18)
    x3 = range(craneo_x+1,craneo_x+14)
    y3 = range(craneo_y+1,craneo_y+14)
    x_ok = colision(x,x2)
    y_ok = colision(y,y2)
    muerte_x = colision (x,x3)
    muerte_y = colision (y,y3)
    
    if muerte_x == 1 and muerte_y == 1:
      game_over()
    
    if x_ok == 1 and y_ok == 1:
      puntaje +=1
      generar_objeto(snake_x[0],snake_y[0])
      #AGREGAR PIEZA AL CÓDIGO DE LA SERPIENTE
      snake_x.append(snake_x[i])  #Agrego el nuevo bloque en la parte inferior de la serpiente
      snake_y.append(snake_y[i])                               
