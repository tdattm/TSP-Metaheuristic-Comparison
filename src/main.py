import os
import sys
import time
import matplotlib.pyplot as plt

# Thêm thư mục gốc của dự án vào sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.algorithms.pso import PSO
from src.algorithms.greedy import Greedy
from src.algorithms.brute_force import BruteForce
from src.algorithms.branch_and_bound import BranchAndBound
from src.algorithms.aco import ACO
from src.util import read_cities, path_cost

def save_results(algorithm_name, route, cost, cities, size):
    output_dir = f'assets/{algorithm_name}_result/size_{size}'
    os.makedirs(output_dir, exist_ok=True)
    
    # Lưu hình ảnh PNG
    plt.figure(figsize=(8, 6))
    x_list, y_list = [], []
    for city in route:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(route[0].x)
    y_list.append(route[0].y)
    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g-')
    plt.title(f'{algorithm_name} TSP Result (Size {size})')
    plt.savefig(f'{output_dir}/route.png')
    plt.close()
    
    # Lưu dữ liệu văn bản
    with open(f'{output_dir}/data.txt', 'w') as f:
        f.write(f'Cost: {cost}\n')
        f.write('Route:\n')
        for city in route:
            f.write(f'{city.x} {city.y}\n')

def compare_results_across_sizes(all_results, sizes):
    os.makedirs('assets', exist_ok=True)
    
    # Biểu đồ thời gian chạy
    plt.figure(figsize=(10, 5))
    for algo in ['PSO', 'Greedy', 'BruteForce', 'BranchAndBound', 'ACO', 'DivideConquer']:
        times = [all_results[size][algo]['time'] if algo in all_results[size] else None for size in sizes]
        plt.plot(sizes, times, marker='o', label=f'{algo} Time')
    plt.title('So sánh thời gian chạy qua các kích thước')
    plt.xlabel('Kích thước (Số thành phố)')
    plt.ylabel('Thời gian (giây)')
    plt.legend()
    plt.grid(True)
    plt.savefig('assets/comparison_time_across_sizes.png')
    plt.close()
    
    # Biểu đồ chi phí
    plt.figure(figsize=(10, 5))
    for algo in ['PSO', 'Greedy', 'BruteForce', 'BranchAndBound', 'ACO', 'DivideConquer']:
        costs = [all_results[size][algo]['cost'] if algo in all_results[size] else None for size in sizes]
        plt.plot(sizes, costs, marker='o', label=f'{algo} Cost')
    plt.title('So sánh chi phí qua các kích thước')
    plt.xlabel('Kích thước (Số thành phố)')
    plt.ylabel('Chi phí')
    plt.legend()
    plt.grid(True)
    plt.savefig('assets/comparison_cost_across_sizes.png')
    plt.close()

if __name__ == "__main__":
    sizes = [8, 16, 20, 22, 32, 40, 48, 51, 64]
    all_results = {size: {} for size in sizes}

    for size in sizes:
        cities = read_cities(size)
        results = {}

        # Chạy PSO
        output_dir = f'assets/pso_result/size_{size}'
        pso = PSO(iterations=1200, population_size=300, gbest_probability=0.02, pbest_probability=0.9, cities=cities)
        start_time = time.time()
        pso_route, pso_cost = pso.run(output_dir=output_dir)
        pso_time = time.time() - start_time
        results['PSO'] = {'cost': pso_cost, 'time': pso_time}
        save_results('pso', pso_route, pso_cost, pso_route, size)

        # Chạy Greedy
        output_dir = f'assets/greedy_result/size_{size}'
        greedy = Greedy(cities)
        start_time = time.time()
        greedy_route, greedy_cost = greedy.run(output_dir=output_dir)
        greedy_time = time.time() - start_time
        results['Greedy'] = {'cost': greedy_cost, 'time': greedy_time}
        save_results('greedy', greedy_route, greedy_cost, greedy_route, size)

        # Chạy Branch and Bound (chỉ cho size < 16)
        if size < 16:
            output_dir = f'assets/branch_and_bound_result/size_{size}'
            bnb = BranchAndBound(cities)
            start_time = time.time()
            bnb_route, bnb_cost = bnb.run(output_dir=output_dir)
            bnb_time = time.time() - start_time
            results['BranchAndBound'] = {'cost': bnb_cost, 'time': bnb_time}
            save_results('branch_and_bound', bnb_route, bnb_cost, bnb_route, size)

        # Chạy Brute Force (chỉ cho size=8)
        if size == 8:
            output_dir = f'assets/brute_force_result/size_{size}'
            brute = BruteForce(cities)
            start_time = time.time()
            brute_route, brute_cost = brute.run(output_dir=output_dir)
            brute_time = time.time() - start_time
            results['BruteForce'] = {'cost': brute_cost, 'time': brute_time}
            save_results('brute_force', brute_route, brute_cost, brute_route, size)

        # Chạy ACO
        output_dir = f'assets/aco_result/size_{size}'
        aco = ACO(cities, n_ants=10, n_iterations=100, alpha=1.0, beta=1.0, evaporation_rate=0.5, Q=1.0)
        start_time = time.time()
        aco_route, aco_cost = aco.run(output_dir=output_dir)
        aco_time = time.time() - start_time
        results['ACO'] = {'cost': aco_cost, 'time': aco_time}
        save_results('aco', aco_route, aco_cost, aco_route, size)

        # # Chạy Divide and Conquer
        # output_dir = f'assets/divide_and_conquer_result/size_{size}'
        # dc = DivideConquer(cities)
        # start_time = time.time()
        # dc_route, dc_cost = dc.run(output_dir=output_dir)
        # dc_time = time.time() - start_time
        # results['DivideConquer'] = {'cost': dc_cost, 'time': dc_time}
        # save_results('divide_and_conquer', dc_route, dc_cost, dc_route, size)

        all_results[size] = results

    # So sánh kết quả qua các kích thước
    compare_results_across_sizes(all_results, sizes)