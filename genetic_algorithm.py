import numpy as np
import random
from datetime import datetime, timedelta
from datetime import datetime
from utils import parse_time_range



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


    def parse_time_range(timeslot):
        try:
            hari, jam = timeslot.split(", ")
            start, end = jam.split("-")
            fmt = "%H:%M"
            return hari.strip(), datetime.strptime(start.strip(), fmt), datetime.strptime(end.strip(), fmt)
        except Exception as e:
            print(f"Error parsing timeslot: {timeslot}", e)
            return None, None, None
    
    def fitness(self, schedule):
        conflicts = 0
        teacher_schedule = []
        room_schedule = []
    
        for entry in schedule:
            teacher = entry['teacher']
            room = entry['room']
            timeslot = entry['timeslot']
    
            day, start, end = parse_time_range(timeslot)
            if not day:
                continue
    
            # Cek konflik dosen
            for t_day, t_start, t_end, t_name in teacher_schedule:
                if t_name == teacher and t_day == day:
                    if (start < t_end and end > t_start):  # overlap
                        conflicts += 1
    
            teacher_schedule.append((day, start, end, teacher))
    
            # Cek konflik ruangan
            for r_day, r_start, r_end, r_name in room_schedule:
                if r_name == room and r_day == day:
                    if (start < r_end and end > r_start):  # overlap
                        conflicts += 1
    
            room_schedule.append((day, start, end, room))
    
        return 1 / (1 + conflicts)
    


    # def fitness(self, schedule):
    #     conflicts = 0
    #     seen = []
    
    #     for s in schedule:
    #         kode_dosen = s["teacher"]
    #         kode_ruangan = s["room"]
    #         kelas = s["class"]
    #         timeslot = s["timeslot"]
    
    #         try:
    #             day, start_time, end_time = parse_timeslot(timeslot)
    #         except:
    #             continue  # skip yang gagal parsing
    
    #         for other in seen:
    #             o_dosen = other["teacher"]
    #             o_ruangan = other["room"]
    #             o_kelas = other["class"]
    #             o_timeslot = other["timeslot"]
    
    #             try:
    #                 o_day, o_start, o_end = parse_timeslot(o_timeslot)
    #             except:
    #                 continue
    
    #             # Jika di hari yang sama
    #             # if day == o_day:
    #             #     # Cek apakah waktu tumpang tindih + aturan istirahat
    #             #     gap = timedelta(minutes=30)
    #             #     if (start_time < o_end + gap) and (end_time + gap > o_start):
    #             #         # Cek konflik dosen
    #             #         if kode_dosen == o_dosen:
    #             #             conflicts += 1
    #             #         # Cek konflik ruangan
    #             #         if kode_ruangan == o_ruangan:
    #             #             conflicts += 1
    #             #         # Cek konflik kelas
    #             #         if kelas == o_kelas:
    #             #             conflicts += 1
    #         # Cek konflik hanya jika entitas yang sama (bukan hanya waktu yang sama)
    #         if kode_dosen == o_dosen and day == o_day:
    #             if (start_time < o_end + gap) and (end_time + gap > o_start):
    #                 conflicts += 1
            
    #         if kode_ruangan == o_ruangan and day == o_day:
    #             if (start_time < o_end + gap) and (end_time + gap > o_start):
    #                 conflicts += 1
            
    #         # Cek jika KELAS YANG SAMA bentrok (ini valid), tapi kalau beda kelas — jangan
    #         if kelas == o_kelas and day == o_day:
    #             if (start_time < o_end + gap) and (end_time + gap > o_start):
    #                 conflicts += 1

    
    #         seen.append(s)
    
    #     return 1 / (1 + conflicts)



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
