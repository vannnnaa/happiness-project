import math

def calculate_sum(terms=100000):
    total = 0.0
      # Пример последовательности k(n)
    for n in range(1, terms + 1):
        total += 1/(2**n) * (1/(1 + 2**(1/2**n)))
    return round(total, 5)

result = calculate_sum()
print(f"Сумма ряда: {result:.5f}")