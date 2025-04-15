import random

class GeneticScheduler:
    def __init__(self, courses, rooms, start_times):
        self.courses = courses
        self.rooms = rooms
        self.start_times = start_times

    def initialize_population(self, size):
        population = []
        for _ in range(size):
            individual = []
            for course in self.courses:
                individual.append({
                    "course": course["course"],
                    "teacher": course["teacher"],
                    "sks": course["sks"],
                    "room": random.choice(self.rooms),
                    "start_time": random.choice(self.start_times)
                })
            population.append(individual)
        return population

    def fitness(self, individual):
        penalty = 0
        teacher_times = {}
        room_times = {}

        for entry in individual:
            duration = entry['sks'] * 45
            start = entry['start_time']
            end = start + duration

            for t in range(start, end, 15):
                if (entry['teacher'], t) in teacher_times:
                    penalty += 1
                else:
                    teacher_times[(entry['teacher'], t)] = True

                if (entry['room'], t) in room_times:
                    penalty += 1
                else:
                    room_times[(entry['room'], t)] = True

        return 1 / (1 + penalty)

    def select_parents(self, population, fitness_scores):
        total = sum(fitness_scores)
        probs = [f / total for f in fitness_scores]
        parents = random.choices(population, weights=probs, k=2)
        return parents[0], parents[1]

    def crossover(self, p1, p2):
        point = random.randint(1, len(p1) - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]

    def mutate(self, individual, mutation_rate=0.1):
        for entry in individual:
            if random.random() < mutation_rate:
                entry['room'] = random.choice(self.rooms)
            if random.random() < mutation_rate:
                entry['start_time'] = random.choice(self.start_times)
        return individual

    def evolve(self, generations=100, population_size=50):
        population = self.initialize_population(population_size)
        history = []
        log = []

        for gen in range(1, generations + 1):
            scores = [self.fitness(ind) for ind in population]
            best = max(zip(scores, population), key=lambda x: x[0])
            history.append(best[0])
            log.append({"Generasi": gen, "Fitness": round(best[0], 4), "Jadwal": best[1]})

            new_pop = []
            while len(new_pop) < population_size:
                p1, p2 = self.select_parents(population, scores)
                c1, c2 = self.crossover(p1, p2)
                new_pop.append(self.mutate(c1))
                if len(new_pop) < population_size:
                    new_pop.append(self.mutate(c2))
            population = new_pop

        final_best = max(population, key=lambda ind: self.fitness(ind))
        return final_best, history, log
