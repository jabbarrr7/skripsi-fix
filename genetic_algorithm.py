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
    
        for entry in individual:
            teacher = entry['teacher']
            timeslot = entry['timeslot']
            sks = entry['sks']
            
            start_time = timeslot
            end_time = timeslot + sks - 1  # contoh: mulai slot 2, 2 sks → slot 2–3
    
            if teacher not in teacher_schedule:
                teacher_schedule[teacher] = []
            
            # Bandingkan dengan semua jadwal yang sudah ada untuk guru itu
            for scheduled in teacher_schedule[teacher]:
                scheduled_start, scheduled_end = scheduled
                # Tambahkan waktu istirahat 1 slot (45 menit = 1 slot)
                if not (end_time + 1 < scheduled_start or start_time > scheduled_end + 1):
                    penalty += 1
            
            teacher_schedule[teacher].append((start_time, end_time))

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
