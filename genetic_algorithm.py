import numpy as np
import random

class GeneticScheduler:
    def __init__(self, tasks, teachers, subjects, rooms, timeslots):
        self.tasks = tasks
        self.teachers = teachers
        self.subjects = subjects
        self.rooms = rooms
        self.timeslots = timeslots
        self.population_size = 50
        self.mutation_rate = 0.1
        self.generations = 100

        # Dosen dengan keahlian yang sesuai untuk mata kuliah tertentu
        self.teacher_skills = {
            teacher: random.sample(subjects, k=random.randint(1, len(subjects)))
            for teacher in teachers
        }

    def create_chromosome(self):
        """Membuat satu individu (jadwal acak)"""
        return [
            (
                task,
                random.choice(self.teachers),
                random.choice(self.subjects),
                random.choice(self.rooms),
                random.choice(self.timeslots)
            )
            for task in self.tasks
        ]

    def fitness(self, chromosome):
        """Menghitung skor fitness berdasarkan seberapa baik jadwal"""
        score = 0

        teacher_schedule = {}
        room_schedule = {}

        for task, teacher, subject, room, timeslot in chromosome:
            if (teacher, timeslot) in teacher_schedule:
                score -= 10  # Penalti jika dosen bentrok
            else:
                teacher_schedule[(teacher, timeslot)] = True

            if (room, timeslot) in room_schedule:
                score -= 10  # Penalti jika ruangan bentrok
            else:
                room_schedule[(room, timeslot)] = True

            if subject in self.teacher_skills[teacher]:
                score += 5  # Bonus jika dosen mengajar sesuai keahlian

        return score

    def select_parents(self, population, fitness_scores):
        """Seleksi orang tua dengan roulette wheel"""
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.sample(population, 2)

        probabilities = [f / total_fitness for f in fitness_scores]
        selected = np.random.choice(population, size=2, p=probabilities, replace=False)
        return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        """Two-point crossover"""
        point1, point2 = sorted(np.random.randint(0, len(parent1), 2))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2

    def mutate(self, chromosome):
        """Mutasi dengan mengganti ruangan atau waktu"""
        for i in range(len(chromosome)):
            if np.random.rand() < self.mutation_rate:
                task, teacher, subject, room, timeslot = chromosome[i]
                new_room = random.choice(self.rooms)
                new_timeslot = random.choice(self.timeslots)
                chromosome[i] = (task, teacher, subject, new_room, new_timeslot)
        return chromosome

    def evolve(self):
        """Menjalankan algoritma genetika"""
        population = [self.create_chromosome() for _ in range(self.population_size)]

        for _ in range(self.generations):
            fitness_scores = [self.fitness(chrom) for chrom in population]
            new_population = []

            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))

            population = new_population

        best_chromosome = max(population, key=self.fitness)
        return best_chromosome
