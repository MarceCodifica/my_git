import time
from functools import lru_cache

# 1. Um gerador infinito usando yield
def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 2. Um decorador de medição de tempo profissional
def medir_tempo(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        print(f"⚡ {funcao.__name__} levou {fim - inicio:.6f} segundos.")
        return resultado
    return wrapper

# 3. Aplicando os conceitos
@medir_tempo
@lru_cache(maxsize=128)  # Memoization avançada nativa do Python
def buscar_fibonacci(n):
    gerador = fibonacci_gen()
    for _ in range(n):
        next(gerador)
    return next(gerador)

# Teste
print(f"Resultado: {buscar_fibonacci(100)}")
print(f"Resultado (Segunda vez, vindo do cache): {buscar_fibonacci(100)}")
