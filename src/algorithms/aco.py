import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from util import path_cost

class ACO:
    def __init__(self, cities, n_ants=10, n_iterations=100, alpha=1.0, beta=1.0, evaporation_rate=0.5, Q=1.0):
        self.cities = cities
        self.n_points = len(cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        self.pheromone = np.ones((self.n_points, self.n_points))
        self.best_path = None
        self.best_path_length = np.inf

    def _distance(self, city1, city2):
        return city1.distance(city2)

    def run(self, output_dir=None):
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        frames = []
        
        for iteration in range(self.n_iterations):
            paths = []
            path_lengths = []
            
            for ant in range(self.n_ants):
                visited = [False] * self.n_points
                current_point = np.random.randint(self.n_points)
                visited[current_point] = True
                path = [current_point]
                path_length = 0
                
                while False in visited:
                    unvisited = np.where(np.logical_not(visited))[0]
                    probabilities = np.zeros(len(unvisited))
                    
                    for i, unvisited_point in enumerate(unvisited):
                        dist = self._distance(self.cities[current_point], self.cities[unvisited_point])
                        probabilities[i] = (self.pheromone[current_point, unvisited_point] ** self.alpha) * \
                                          ((1.0 / dist) ** self.beta)
                    
                    probabilities /= np.sum(probabilities)
                    
                    next_point = np.random.choice(unvisited, p=probabilities)
                    path.append(next_point)
                    path_length += self._distance(self.cities[current_point], self.cities[next_point])
                    visited[next_point] = True
                    current_point = next_point
                
                paths.append(path)
                path_lengths.append(path_length)
                
                if path_length < self.best_path_length:
                    self.best_path = path
                    self.best_path_length = path_length
                    
                    # Lưu frame cho GIF mỗi khi tìm thấy lộ trình tốt hơn
                    if output_dir and iteration % 10 == 0:  # Lưu mỗi 10 thế hệ
                        plt.figure(figsize=(8, 6))
                        x_list, y_list = [], []
                        for idx in self.best_path:
                            x_list.append(self.cities[idx].x)
                            y_list.append(self.cities[idx].y)
                        x_list.append(self.cities[self.best_path[0]].x)
                        y_list.append(self.cities[self.best_path[0]].y)
                        plt.plot(x_list, y_list, 'ro')
                        plt.plot(x_list, y_list, 'g-')
                        plt.title(f'ACO TSP Iteration {iteration} (Cost: {self.best_path_length:.2f})')
                        frame_path = f'{output_dir}/aco_iter_{iteration}.png'
                        plt.savefig(frame_path)
                        plt.close()
                        frames.append(imageio.imread(frame_path))
                        os.remove(frame_path)
            
            self.pheromone *= self.evaporation_rate
            
            for path, path_length in zip(paths, path_lengths):
                for i in range(self.n_points - 1):
                    self.pheromone[path[i], path[i + 1]] += self.Q / path_length
                self.pheromone[path[-1], path[0]] += self.Q / path_length
        
        # Lưu GIF
        if output_dir and frames:
            imageio.mimsave(f'{output_dir}/aco_process.gif', frames, fps=5)
        
        # Lưu PNG kết quả cuối
        if output_dir:
            plt.figure(figsize=(8, 6))
            x_list, y_list = [], []
            for idx in self.best_path:
                x_list.append(self.cities[idx].x)
                y_list.append(self.cities[idx].y)
            x_list.append(self.cities[self.best_path[0]].x)
            y_list.append(self.cities[self.best_path[0]].y)
            plt.plot(x_list, y_list, 'ro')
            plt.plot(x_list, y_list, 'g-')
            plt.title('ACO Final TSP Route')
            plt.savefig(f'{output_dir}/final_route.png')
            plt.close()
        
        best_route = [self.cities[idx] for idx in self.best_path]
        return best_route, self.best_path_length