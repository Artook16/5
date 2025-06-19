import math
import timeit
from itertools import combinations
import random


def generate_triangles_algorithmic(points):
    triangles = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                triangles.append((points[i], points[j], points[k]))
    return triangles


def generate_triangles_itertools(points):
    return list(combinations(points, 3))


def calculate_area(a, b, c):
    return 0.5 * abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def generate_optimal_triangles(points, min_area=1.0):
    optimal_triangles = []
    max_area = 0
    best_triangle = None
    n = len(points)
    
    sorted_points = sorted(points)
    
    for i in range(n):
        a = sorted_points[i]
        for j in range(i + 1, n):
            b = sorted_points[j]
            max_possible_area = 0.5 * abs(b[0] - a[0]) * (max(p[1] for p in sorted_points[j+1:]) - a[1]) if j+1 < n else 0
            if max_possible_area < min_area:
                continue 
            
            for k in range(j + 1, n):
                c = sorted_points[k]
                area = calculate_area(a, b, c)
                
                if area >= min_area:
                    triangle = (a, b, c)
                    optimal_triangles.append(triangle)
                    if area > max_area:
                        max_area = area
                        best_triangle = triangle
                        
                    if area > 2 * min_area and k + 1 < n:
                        k += min(3, n - k - 1)
    
    return optimal_triangles, best_triangle, max_area


def measure_time(func, points):
    return timeit.timeit(lambda: func(points), number=10)


def generate_random_points(k, x_range=(-10, 10), y_range=(-10, 10)):
    return [
        (round(random.uniform(*x_range), 1), round(random.uniform(*y_range), 1))
        for _ in range(k)
    ]


def main():
    k = int(input("Введите количество точек K: "))
    min_area = float(input("Введите минимальную площадь треугольника (для оптимизации): "))

    points = generate_random_points(k)
    print(f"\nСгенерировано {k} случайных точек на плоскости.\n")

    triangles_alg = generate_triangles_algorithmic(points)
    triangles_it = generate_triangles_itertools(points)

    print("Первые 5 треугольников (алгоритмический метод):")
    for t in triangles_alg[:5]:
        print(t)

    print("\nПервые 5 треугольников (itertools.combinations):")
    for t in triangles_it[:5]:
        print(t)

    print(f"\nВсего треугольников: {len(triangles_alg)}\n")

    time_alg = measure_time(generate_triangles_algorithmic, points)
    time_it = measure_time(generate_triangles_itertools, points)

    print(f"Время выполнения (алгоритмический метод): {time_alg:.6f} сек")
    print(f"Время выполнения (itertools.combinations): {time_it:.6f} сек")

    if time_alg < time_it:
        print("→ Алгоритмический метод быстрее.\n")
    else:
        print("→ Метод itertools быстрее.\n")

    optimal_triangles, best_triangle, max_area = generate_optimal_triangles(points, min_area)

    print(f"Найдено {len(optimal_triangles)} треугольников с площадью >= {min_area}.\n")

    if optimal_triangles:
        print("Все подходящие треугольники:")
        for triangle in optimal_triangles:
            area = calculate_area(*triangle)
            print(f"{triangle}, площадь = {area:.2f}")

        print(f"\nНаиболее оптимальный треугольник (максимальная площадь = {max_area:.2f}):")
        print(best_triangle)
        print("Критерий оптимальности: максимальная площадь среди всех подходящих треугольников.")
    else:
        print("Не найдено треугольников, удовлетворяющих минимальной площади.")


if __name__ == "__main__":
    main()
