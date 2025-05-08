import random
import os
import matplotlib.pyplot as plt
import imageio
from util import path_cost

class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = []

    def clear_velocity(self):
        self.velocity.clear()

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)

class PSO:
    def __init__(self, iterations, population_size, gbest_probability=1.0, pbest_probability=1.0, cities=None):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    def random_route(self):
        return random.sample(self.cities, len(self.cities))

    def initial_population(self):
        random_population = [self.random_route() for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]

    def greedy_route(self, start_index):
        unvisited = self.cities[:]
        del unvisited[start_index]
        route = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        return route

    def run(self, output_dir=None):
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        self.gcost_iter.append(self.gbest.pbest_cost)
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Danh sách lưu các frame cho GIF
        cost_frames = []
        route_frames = []
        
        for t in range(self.iterations):
            self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
            self.gcost_iter.append(self.gbest.pbest_cost)

            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                gbest = self.gbest.pbest[:]
                new_route = particle.route[:]

                for i in range(len(self.cities)):
                    if new_route[i] != particle.pbest[i]:
                        swap = (i, particle.pbest.index(new_route[i]), self.pbest_probability)
                        temp_velocity.append(swap)
                        new_route[swap[0]], new_route[swap[1]] = new_route[swap[1]], new_route[swap[0]]

                for i in range(len(self.cities)):
                    if new_route[i] != gbest[i]:
                        swap = (i, gbest.index(new_route[i]), self.gbest_probability)
                        temp_velocity.append(swap)
                        gbest[swap[0]], gbest[swap[1]] = gbest[swap[1]], gbest[swap[0]]

                particle.velocity = temp_velocity

                for swap in temp_velocity:
                    if random.random() <= swap[2]:
                        new_route[swap[0]], new_route[swap[1]] = new_route[swap[1]], new_route[swap[0]]

                particle.route = new_route
                particle.update_costs_and_pbest()

            # Lưu frame cho GIF mỗi 20 thế hệ
            if output_dir and t % 20 == 0:
                # Vẽ biểu đồ chi phí
                plt.figure(figsize=(8, 6))
                plt.plot(self.gcost_iter, 'g-')
                plt.title(f'PSO Cost over Iterations (Iter {t})')
                plt.xlabel('Generation')
                plt.ylabel('Distance')
                cost_path = f'{output_dir}/cost_iter_{t}.png'
                plt.savefig(cost_path)
                plt.close()
                cost_frames.append(imageio.imread(cost_path))
                os.remove(cost_path)

                # Vẽ lộ trình
                plt.figure(figsize=(8, 6))
                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(self.gbest.pbest[0].x)
                y_list.append(self.gbest.pbest[0].y)
                plt.plot(x_list, y_list, 'ro')
                plt.plot(x_list, y_list, 'g-')
                plt.title(f'PSO TSP Iteration {t}')
                route_path = f'{output_dir}/route_iter_{t}.png'
                plt.savefig(route_path)
                plt.close()
                route_frames.append(imageio.imread(route_path))
                os.remove(route_path)

        # Lưu GIF
        if output_dir and cost_frames:
            imageio.mimsave(f'{output_dir}/cost_process.gif', cost_frames, fps=5)
        if output_dir and route_frames:
            imageio.mimsave(f'{output_dir}/route_process.gif', route_frames, fps=5)

        # Lưu PNG kết quả cuối cùng
        if output_dir:
            # Biểu đồ chi phí cuối
            plt.figure(figsize=(8, 6))
            plt.plot(self.gcost_iter, 'g-')
            plt.title('PSO Final Cost over Iterations')
            plt.xlabel('Generation')
            plt.ylabel('Distance')
            plt.savefig(f'{output_dir}/final_cost.png')
            plt.close()

            # Lộ trình cuối
            plt.figure(figsize=(8, 6))
            x_list, y_list = [], []
            for city in self.gbest.pbest:
                x_list.append(city.x)
                y_list.append(city.y)
            x_list.append(self.gbest.pbest[0].x)
            y_list.append(self.gbest.pbest[0].y)
            plt.plot(x_list, y_list, 'ro')
            plt.plot(x_list, y_list, 'g-')
            plt.title('PSO Final TSP Route')
            plt.savefig(f'{output_dir}/final_route.png')
            plt.close()

        return self.gbest.pbest, self.gbest.pbest_cost

    # def run(self):
    #     self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
    #     for t in range(self.iterations):
    #         self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
    #         self.gcost_iter.append(self.gbest.pbest_cost)

    #         for particle in self.particles:
    #             particle.clear_velocity()
    #             temp_velocity = []
    #             gbest = self.gbest.pbest[:]
    #             new_route = particle.route[:]

    #             for i in range(len(self.cities)):
    #                 if new_route[i] != particle.pbest[i]:
    #                     swap = (i, particle.pbest.index(new_route[i]), self.pbest_probability)
    #                     temp_velocity.append(swap)
    #                     new_route[swap[0]], new_route[swap[1]] = new_route[swap[1]], new_route[swap[0]]

    #             for i in range(len(self.cities)):
    #                 if new_route[i] != gbest[i]:
    #                     swap = (i, gbest.index(new_route[i]), self.gbest_probability)
    #                     temp_velocity.append(swap)
    #                     gbest[swap[0]], gbest[swap[1]] = gbest[swap[1]], gbest[swap[0]]

    #             particle.velocity = temp_velocity

    #             for swap in temp_velocity:
    #                 if random.random() <= swap[2]:
    #                     new_route[swap[0]], new_route[swap[1]] = new_route[swap[1]], new_route[swap[0]]

    #             particle.route = new_route
    #             particle.update_costs_and_pbest()