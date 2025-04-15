import numpy as np
import random

class GeneticScheduler:
    def __init__(self, courses, teachers, rooms, timeslots, semesters, classes):
        self.courses = courses
        self.teachers = teachers
        self.rooms = rooms
        self.timeslots = timeslots
        self.semesters = semesters
        self.classes = classes

    def initialize_population(self, size):
        population = []
        for _ in range(size):
            individual = []
            for course_obj in self.courses:
                # Gunakan data tetap dari CSV
                course = course_obj['course']
                teacher = course_obj['teacher']
                sks = int(course_obj['sks'])
                semester = int(course_obj['semester'])
                class_assigned = course_obj['class']
                # Untuk timeslot, acak dari daftar timeslots
                timeslot = random.choice(self.timeslots)
                # Untuk ruangan, acak dari daftar rooms
                room = random.choice(self.rooms)
                individual.append({
                    "course": course,
                    "teacher": teacher,
                    "sks": sks,
                    "semester": semester,
                    "class": class_assigned,
                    "room": room,
                    "timeslot": timeslot
                })
            population.append(individual)
        return population

    def fitness(self, individual):
        penalty = 0
        teacher_schedule = {}
        room_schedule = {}
        # Asumsikan timeslot berupa angka dan durasi dihitung berdasarkan sks
        # Durasi: sks * 45 (menit) dibagi dengan slot (misalnya 1 slot = 45 menit)
        for entry in individual:
            ts = entry['timeslot']
            duration = entry['sks']  # Karena 1 slot = 1 SKS (45 menit)
            # Cek konflik untuk dosen: jika dosen memiliki 2 jadwal yang sama pada slot ts
            teacher_key = (entry['teacher'], ts, entry['semester'], entry['class'])
            if teacher_key in teacher_schedule:
                penalty += 1
            else:
                teacher_schedule[teacher_key] = True

            # Cek konflik untuk ruangan: jika ruangan digunakan lebih dari sekali pada slot yang sama
            room_key = (entry['room'], ts, entry['semester'])
            if room_key in room_schedule:
                penalty += 1
            else:
                room_schedule[room_key] = True

        return 1 / (1 + penalty)

    def select_parents(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [f / total_fitness for f in fitness_scores]
        selected_indices = np.random.choice(len(population), size=2, p=probabilities, replace=False)
        return population[selected_indices[0]], population[selected_indices[1]]

    def crossover(self, parent1, parent2):
        # Single-point crossover per course entry
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, individual, mutation_rate=0.1):
        for entry in individual:
            # Hanya ubah room dan timeslot
            if random.random() < mutation_rate:
                entry['room'] = random.choice(self.rooms)
            if random.random() < mutation_rate:
                entry['timeslot'] = random.choice(self.timeslots)
        return individual

    def evolve(self, generations=100, population_size=50):
        population = self.initialize_population(population_size)
        history = []
        evolution_log = []
        
        for gen in range(1, generations + 1):
            fitness_scores = [self.fitness(ind) for ind in population]
            best_index = np.argmax(fitness_scores)
            best_fitness = fitness_scores[best_index]
            best_individual = population[best_index]
            
            evolution_log.append({
                "Generasi": gen,
                "Fitness": round(best_fitness, 4),
                "Jadwal": best_individual
            })
            history.append(best_fitness)
            
            new_population = []
            while len(new_population) < population_size:
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                if len(new_population) < population_size:
                    new_population.append(self.mutate(child2))
            population = new_population
        
        final_best = max(population, key=lambda ind: self.fitness(ind))
        return final_best, history, evolution_log
