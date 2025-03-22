import threading # Importa o módulo threading para criar threads
import math      # Importa a biblioteca math para cálculos matemáticos
import time      # Importa a biblioteca time para medir o tempo de execução

# Lista compartilhada para armazenar os números primos encontrados
primos = []
lock = threading.Lock()

# Função para verificar se um número é primo
def eh_primo(n):
    if n < 2:  # números menores que 2 não são primos
        return False
    if n in (2, 3): # números 2 e 3 são primos
        return True
    if n % 2 == 0 or n % 3 == 0: # elimina os múltiplos de 2 e de 3 
        return False
    limite = int(math.sqrt(n)) + 1 # estabelece o limite para verificar os números, até a raiz quadrada de n
    for i in range(5, limite, 2): # começa a verificação em 5 até a variável limite, incrementando de 2 em 2 para excluir os números pares.
        if n % i == 0:
            return False
    return True

# Função que cada thread executará para encontrar primos em um intervalo
def encontrar_primos(inicio, fim):
    global primos # Indica que estamos acessando a variável global 'primos'
    temp = [] # Lista temporária para armazenar os primos encontrados por essa thread
    for num in range(inicio, fim): # percorre todos os números dentro de intervalo e verifica se são primos
        if eh_primo(num):
            temp.append(num) # se for primo é adicionado à lista temporária temp
    
    # Bloqueia o acesso à lista compartilhada antes de modificar
    with lock: # permite que apenas uma thread modifique a lista primos, evitando condições de corrida
        primos.extend(temp)

# Função principal para gerenciar as threads, divide o trabalho entre as threads
def calcular_primos_paralelo(limite_inferior, limite_superior, num_threads):
    global primos
    primos = [] # zera a lista global

    threads = [] # cria um lista de threads para armazenar as threads criadas
    intervalo = (limite_superior - limite_inferior) // num_threads # quantos números cada thread irá verificar
    
    for i in range(num_threads):
        inicio = limite_inferior + i * intervalo # define início do intervalo de cada thread
        fim = limite_inferior + (i + 1) * intervalo if i != num_threads - 1 else limite_superior
        t = threading.Thread(target=encontrar_primos, args=(inicio, fim))# cria a thread t que executará a função encontrar_primos e passa os argumentos de inicio e fim
        threads.append(t) # adiciona a thread t à lista de threads
        t.start() # inicia a execução da thread t
        #print(f'Thread {i} em execução')

    for t in threads:
        t.join() # .join faz com que o programa espere todas as threads terminarem sua execução antes de continuar


    return primos

# Parâmetros da busca
# Definição dos limites do intervalo de busca por primos
limite_inferior = 10**5   # Início do intervalo (100.000)
limite_superior = 10**6   # Fim do intervalo (1.000.000)
num_threads = 8

# Medindo tempo de execução
inicio = time.time()
resultado = calcular_primos_paralelo(limite_inferior, limite_superior, num_threads)
fim = time.time()

print(f"Primos encontrados: {len(resultado)}")
print(f"Tempo de execução utilizando Threads: {fim - inicio:.4f} segundos")

