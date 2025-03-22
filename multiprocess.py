import math  # Importa a biblioteca para operações matemáticas
import time  # Importa a biblioteca para medir o tempo de execução
import multiprocessing  # Importa a biblioteca para multiprocessamento

# Função para verificar se um número é primo
def eh_primo(n):
    """
    Verifica se um número n é primo.
    Retorna True se for primo, False caso contrário.
    """
    if n < 2:  # Números menores que 2 não são primos
        return False
    if n in (2, 3):  # 2 e 3 são primos
        return True
    if n % 2 == 0 or n % 3 == 0:  # Elimina múltiplos de 2 e 3
        return False
    
    # Verificamos divisibilidade apenas até a raiz quadrada de n
    limite = int(math.sqrt(n)) + 1
    for i in range(5, limite, 2):  # Testamos apenas números ímpares a partir de 5
        if n % i == 0:
            return False
    return True  # Se não encontrou divisores, é primo

# Função para encontrar todos os primos dentro de um intervalo
def encontrar_primos(inicio, fim):
    """
    Retorna uma lista de números primos dentro do intervalo [inicio, fim).
    Essa função será executada por múltiplos processos.
    """
    return [num for num in range(inicio, fim) if eh_primo(num)]

# Função principal para dividir a carga de trabalho entre processos
def calcular_primos_multiprocess(limite_inferior, limite_superior, num_processos):
    """
    Divide o intervalo [limite_inferior, limite_superior] entre múltiplos processos
    e calcula os números primos dentro desse intervalo.
    """
    intervalo = (limite_superior - limite_inferior) // num_processos  # Divide o intervalo igualmente

    with multiprocessing.Pool(processes=num_processos) as pool:  # Cria um pool de processos
        # Divide o intervalo entre os processos
        ranges = [(limite_inferior + i * intervalo, 
                   limite_inferior + (i + 1) * intervalo if i != num_processos - 1 else limite_superior) 
                  for i in range(num_processos)]
        
        # Executa a função encontrar_primos() em paralelo com os intervalos definidos
        resultados = pool.starmap(encontrar_primos, ranges)

    # Junta os resultados de todos os processos em uma única lista
    primos = [num for sublist in resultados for num in sublist]
    return primos  # Retornamos a lista de números primos encontrados

# Garantindo compatibilidade com Windows
if __name__ == "__main__":
    """
    O bloco if __name__ == "__main__" é necessário no Windows para evitar
    a criação recursiva de processos ao executar multiprocessing.
    """
    # Definição dos limites do intervalo de busca por primos
    limite_inferior = 10**5   # Início do intervalo (100.000)
    limite_superior = 10**6   # Fim do intervalo (1.000.000)

    # Define o número de processos como o total de núcleos do processador
    num_processos = multiprocessing.cpu_count()

    # Medindo o tempo de execução
    inicio = time.time()
    resultado = calcular_primos_multiprocess(limite_inferior, limite_superior, num_processos)
    fim = time.time()

    # Exibir os resultados
    print(f"Primos encontrados: {len(resultado)}")  # Exibe quantos primos foram encontrados
    print(f"Tempo de execução utilizando multiprocess: {fim - inicio:.4f} segundos")  # Exibe o tempo total gasto na execução
