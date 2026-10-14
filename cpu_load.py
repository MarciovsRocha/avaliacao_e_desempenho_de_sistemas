import time

print("Fase 1 - espera inicial")
time.sleep(60) # 1 minuto

print("Fase 2 - consome pouca CPU")
inicio = time.time()
n = 1
while time.time() - inicio < 120:  # 2 minutos
	time.sleep(20) 
	n += 1

print("Fase 3 - consome CPU")
inicio = time.time()
n = 1
while time.time() - inicio < 180:  # 3 minutos
	is_prime = True
	for i in range(2, n**2 + 1):
		if n % i == 0:
			is_prime = False
			break
	n += 1

print("Fase 4 - consome pouca CPU")
inicio = time.time()
n = 1
while time.time() - inicio < 180:  # 3 minutos
	time.sleep(20) 
	n += 1

print("Fase 5 - espera final")
time.sleep(60) # 1 minuto