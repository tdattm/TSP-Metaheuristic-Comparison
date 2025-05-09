import os
import itertools
import matplotlib.pyplot as plt
import imageio
from util import path_cost

class BruteForce:
    def __init__(self, cities):
        self.cities = cities
        self.best_route = None
        self.best_cost = float('inf')

    def run(self, output_dir=None):
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        frames = []
        count = 0
        max_frames = 50  # Giới hạn số frame để tránh quá tải
        
        # Thử tất cả các hoán vị
        for perm in itertools.permutations(self.cities):
            current_cost = path_cost(perm)
            if current_cost < self.best_cost:
                self.best_route = list(perm)
                self.best_cost = current_cost
                
                # Lưu frame cho GIF mỗi khi tìm thấy lộ trình tốt hơn
                if output_dir and count < max_frames:
                    plt.figure(figsize=(8, 6))
                    x_list, y_list = [], []
                    for city in perm:
                        x_list.append(city.x)
                        y_list.append(city.y)
                    x_list.append(perm[0].x)
                    y_list.append(perm[0].y)
                    plt.plot(x_list, y_list, 'ro')
                    plt.plot(x_list, y_list, 'g-')
                    plt.title(f'Brute Force TSP (Cost: {current_cost:.2f})')
                    frame_path = f'{output_dir}/brute_force_step_{count}.png'
                    plt.savefig(frame_path)
                    plt.close()
                    frames.append(imageio.imread(frame_path))
                    os.remove(frame_path)
                    count += 1

        # Lưu GIF
        if output_dir and frames:
            imageio.mimsave(f'{output_dir}/brute_force_process.gif', frames, fps=5)
        
        return self.best_route, self.best_cost