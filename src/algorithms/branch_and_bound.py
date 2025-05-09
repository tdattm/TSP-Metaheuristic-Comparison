import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from util import path_cost

class BranchAndBound:
    def __init__(self, cities):
        self.cities = cities
        self.n = len(cities)
        self.best_route = None
        self.best_cost = float('inf')
        self.distance_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self):
        matrix = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    matrix[i][j] = self.cities[i].distance(self.cities[j])
                else:
                    matrix[i][j] = float('inf')
        return matrix

    def _lower_bound(self, visited, current):
        # Tính cận dưới: tổng khoảng cách tối thiểu từ các thành phố chưa thăm
        unvisited = [i for i in range(self.n) if i not in visited]
        lb = 0
        for i in unvisited:
            min_dist = min(self.distance_matrix[i][j] for j in range(self.n) if j != i)
            lb += min_dist
        for i in visited:
            min_dist = min(self.distance_matrix[i][j] for j in unvisited) if unvisited else 0
            lb += min_dist
        return lb / 2  # Chia 2 vì mỗi cạnh được tính hai lần

    def _branch_and_bound(self, current, visited, path, current_cost, frames, output_dir, frame_count):
        if len(visited) == self.n:
            # Hoàn thành lộ trình, kiểm tra chi phí về điểm đầu
            cost_to_start = self.distance_matrix[current][path[0]]
            total_cost = current_cost + cost_to_start
            if total_cost < self.best_cost:
                self.best_cost = total_cost
                self.best_route = path[:]
                # Lưu frame cho GIF
                if output_dir and frame_count[0] < 50:  # Giới hạn 50 frame
                    plt.figure(figsize=(8, 6))
                    x_list, y_list = [], []
                    route_cities = [self.cities[i] for i in path]
                    for city in route_cities:
                        x_list.append(city.x)
                        y_list.append(city.y)
                    x_list.append(route_cities[0].x)
                    y_list.append(route_cities[0].y)
                    plt.plot(x_list, y_list, 'ro')
                    plt.plot(x_list, y_list, 'g-')
                    plt.title(f'Branch and Bound TSP (Cost: {total_cost:.2f})')
                    frame_path = f'{output_dir}/bnb_step_{frame_count[0]}.png'
                    plt.savefig(frame_path)
                    plt.close()
                    frames.append(imageio.imread(frame_path))
                    os.remove(frame_path)
                    frame_count[0] += 1
            return

        for next_city in range(self.n):
            if next_city not in visited:
                new_cost = current_cost + self.distance_matrix[current][next_city]
                lb = new_cost + self._lower_bound(visited + [next_city], next_city)
                if lb < self.best_cost:
                    path.append(next_city)
                    self._branch_and_bound(next_city, visited + [next_city], path, new_cost, frames, output_dir, frame_count)
                    path.pop()

    def run(self, output_dir=None):
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        frames = []
        frame_count = [0]  # Sử dụng list để thay đổi giá trị trong đệ quy
        self._branch_and_bound(0, [0], [0], 0, frames, output_dir, frame_count)
        
        # Lưu GIF
        if output_dir and frames:
            imageio.mimsave(f'{output_dir}/bnb_process.gif', frames, fps=5)
        
        # Lưu PNG kết quả cuối
        if output_dir and self.best_route:
            plt.figure(figsize=(8, 6))
            x_list, y_list = [], []
            route_cities = [self.cities[i] for i in self.best_route]
            for city in route_cities:
                x_list.append(city.x)
                y_list.append(city.y)
            x_list.append(route_cities[0].x)
            y_list.append(route_cities[0].y)
            plt.plot(x_list, y_list, 'ro')
            plt.plot(x_list, y_list, 'g-')
            plt.title(f'Branch and Bound Final TSP Route')
            plt.savefig(f'{output_dir}/final_route.png')
            plt.close()

        return [self.cities[i] for i in self.best_route], self.best_cost