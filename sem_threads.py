import math
import time

# Função para verificar se um número é primo
def eh_primo(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limite = int(math.sqrt(n)) + 1
    for i in range(5, limite, 2):
        if n % i == 0:
            return False
    return True

# Função para encontrar todos os primos dentro de um intervalo
def encontrar_primos_sequencial(inicio, fim):
    primos = []
    for num in range(inicio, fim):
        if eh_primo(num):
            primos.append(num)
    return primos

# Definição dos limites do intervalo de busca por primos
limite_inferior = 10**5   # Início do intervalo (100.000)
limite_superior = 10**6   # Fim do intervalo (1.000.000)

# Medindo tempo de execução
inicio = time.time()
resultado = encontrar_primos_sequencial(limite_inferior, limite_superior)
fim = time.time()

# Exibir resultados
print(f"Primos encontrados: {len(resultado)}")
print(f"Tempo de execução sem utilizar Threads: {fim - inicio:.4f} segundos")
