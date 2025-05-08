import os
import matplotlib.pyplot as plt
import imageio
from util import path_cost

class Greedy:
    def __init__(self, cities):
        self.unvisited = cities[1:]
        self.route = [cities[0]]

    def run(self, output_dir=None):
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        frames = []
        
        while len(self.unvisited):
            index, nearest_city = min(enumerate(self.unvisited), key=lambda item: item[1].distance(self.route[-1]))
            self.route.append(nearest_city)
            del self.unvisited[index]
            
            # Lưu frame cho GIF
            if output_dir:
                plt.figure(figsize=(8, 6))
                x_list, y_list = [], []
                for city in self.route:
                    x_list.append(city.x)
                    y_list.append(city.y)
                plt.plot(x_list, y_list, 'ro')
                plt.plot(x_list, y_list, 'g-')
                # Vẽ các thành phố chưa thăm
                unvisited_x, unvisited_y = [], []
                for city in self.unvisited:
                    unvisited_x.append(city.x)
                    unvisited_y.append(city.y)
                if unvisited_x:
                    plt.plot(unvisited_x, unvisited_y, 'bo')
                plt.title(f'Greedy TSP Step {len(self.route)}')
                frame_path = f'{output_dir}/greedy_step_{len(self.route)}.png'
                plt.savefig(frame_path)
                plt.close()
                frames.append(imageio.imread(frame_path))
                os.remove(frame_path)

        # Lưu GIF
        if output_dir and frames:
            imageio.mimsave(f'{output_dir}/greedy_process.gif', frames, fps=5)
        
        return self.route, path_cost(self.route)

    # def run(self, plot=False):
    #     while len(self.unvisited):
    #         index, nearest_city = min(enumerate(self.unvisited), key=lambda item: item[1].distance(self.route[-1]))
    #         self.route.append(nearest_city)
    #         del self.unvisited[index]
    #     return path_cost(self.route)