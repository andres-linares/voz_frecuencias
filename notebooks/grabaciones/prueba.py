import threading
from array import array
from queue import Queue, Full
import pickle
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import pandas as pd

CHUNK_SIZE = 512
MIN_VOLUME = 32000
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10


def main():
	stream = pyaudio.PyAudio().open(
			format=pyaudio.paInt16,
			channels=1,
			rate=16000,
			input=True,
			frames_per_buffer=512,
	)
	stopped = threading.Event()
	q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE))) #Cola con tamaño máximo de 10 chunks
	a = None
	listen_t = threading.Thread(target=listen, args=(stopped, q, stream))
	listen_t.start()
	record_t = threading.Thread(target=record, args=(stopped, q, a))
	record_t.start()

	try:
			while True:
					listen_t.join(0.1)
					record_t.join(0.1)
	except KeyboardInterrupt:
			stopped.set()

	listen_t.join()
	record_t.join()

def anadir(nparray):
	tamano = 95232
	recibido = len(nparray)
	faltante = tamano - recibido
	#print("El tamaño recibido es: {}".format(len(nparray)))
	complemento = np.zeros(faltante)
	nparray = np.append(nparray, complemento)
	#print("El nuevo tamaño es: {}".format(len(nparray)))
	return nparray




def record(stopped, q, a):
	grabando = False
	contador = 0
	segundos = 0.4
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
			if vol >= MIN_VOLUME:
					if grabando == False:
						print("\nComenzando a grabar...")
					grabando = True
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
					print("Termina la grabación...")
					print("Comienza la clasificación...")
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

					respuesta = clasificador_andres.predict(np.array(filtros).reshape(1, -1))[0]
					print("Termina la clasificación")
					print(respuesta)

					#Agregar datos al clasificador

					respuesta = input('Digite la respuesta correcta: ')
					if respuesta != 'no':
						solucion = pd.read_csv('{}.csv'.format(respuesta), index_col=0)
						filtros.append(respuesta)
						muestra = pd.DataFrame(columns=[
						    '20-100 Hz',
						    '100-200 Hz',
						    '200-300 Hz',
						    '300-400 Hz',
						    '400-500 Hz',
						    '500-600 Hz',
						    '600-700 Hz',
						    '700-800 Hz',
						    '800-900 Hz',
						    '900-1000 Hz',
						    '1000-1100 Hz',
						    '1100-1200 Hz',
						    '1200-1300 Hz',
						    '1300-1400 Hz',
						    '1400-1500 Hz',
						    '1500-1600 Hz',
						    '1600-1700 Hz',
						    '1700-1800 Hz',
						    '1800-1900 Hz',
						    '1900-2000 Hz',
						    'Palabra'
						])
						muestra.loc[0] = filtros
						nuevo = pd.concat([solucion, muestra], ignore_index=True)
						nuevo.to_csv('{}.csv'.format(respuesta))
						print(nuevo.shape)

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


def listen(stopped, q, stream):
	while True:
			if stopped.wait(timeout=0):
					break
			try:
					pedazo = stream.read(512)
					q.put(array('h', pedazo))
			except Full:
					pass  # discard


if __name__ == '__main__':
		main()