import simpy
import random
import math

# Triangular-Verteilung für Behandlungszeiten
def triangular_dist(minimum, mode, maximum):
    return random.triangular(minimum, mode, maximum)

# Patiententypen und ihre Prozesse
def patient(env, patient_id, patient_type, registration, cw1, cw2, x_ray, plaster, stats, cw_limit):
    arrival_time = env.now  # Record arrival time

    # Registrierung
    with registration.request() as req:
        yield req
        reg_time = triangular_dist(0.2, 0.5, 1.0)
        yield env.timeout(reg_time)

    # Zuweisung zu CW1 oder CW2
    casualty_ward = cw1 if random.random() < 0.6 else cw2
    with casualty_ward.request() as req:
        yield req
        if casualty_ward == cw2 and len(cw2.queue) < cw_limit:
            cw_time = triangular_dist(2.8, 4.1, 6.3)
        else:
            cw_time = triangular_dist(1.5, 3.2, 5.0)
        yield env.timeout(cw_time)

    # Weiteres Vorgehen abhängig vom Patiententyp
    if patient_type == 1:  # X-ray erforderlich
        with x_ray.request() as req:
            yield req
            x_time = triangular_dist(2.0, 2.8, 4.1)
            yield env.timeout(x_time)
        # Rückkehr zu CW
        with casualty_ward.request() as req:
            yield req
            yield env.timeout(cw_time)
    elif patient_type == 2:  # Gips entfernen
        with plaster.request() as req:
            yield req
            plaster_time = triangular_dist(3.0, 3.8, 4.7)
            yield env.timeout(plaster_time)
    elif patient_type == 3:  # Gips erneuern und Röntgen
        with x_ray.request() as req:
            yield req
            x_time = triangular_dist(2.0, 2.8, 4.1)
            yield env.timeout(x_time)
        with plaster.request() as req:
            yield req
            plaster_time = triangular_dist(3.0, 3.8, 4.7)
            yield env.timeout(plaster_time)
        with x_ray.request() as req:
            yield req
            yield env.timeout(x_time)
        with casualty_ward.request() as req:
            yield req
            yield env.timeout(cw_time)
    # Typ 4 benötigt keine zusätzlichen Schritte (nur CW)

    departure_time = env.now
    total_time = departure_time - arrival_time
    stats["patients"].append({"id": patient_id, "type": patient_type, "total_time": total_time})



def generate_patients(env, num_patients, registration, cw1, cw2, x_ray, plaster, stats, cw_limit):
    for i in range(num_patients):
        interarrival_time = random.expovariate(1 / 0.3)
        yield env.timeout(interarrival_time)
        patient_type = random.choices([1, 2, 3, 4], weights=[35, 20, 5, 40], k=1)[0]
        env.process(patient(env, i, patient_type, registration, cw1, cw2, x_ray, plaster, stats, cw_limit))



# Simulationsumgebung
def run_simulation(num_patients=250, cw_limit=5):
    env = simpy.Environment()

    # Ressourcen definieren
    registration = simpy.Resource(env, capacity=1)
    cw1 = simpy.Resource(env, capacity=2)
    cw2 = simpy.Resource(env, capacity=2)
    x_ray = simpy.Resource(env, capacity=2)
    plaster = simpy.Resource(env, capacity=1)

    # Statistics dictionary
    stats = {"patients": []}

    env.process(generate_patients(env, num_patients, registration, cw1, cw2, x_ray, plaster, stats, cw_limit))

    # Simulation starten
    env.run()

    # Print statistics
    print_statistics(stats, cw_limit)

def print_statistics(stats, cw_limit):
    total_patients = len(stats["patients"])
    print(f"Total patients processed: {total_patients}")
    print(f"Maximum size of CW2 queue: {cw_limit}")

    # Group patients by type
    types = {1: [], 2: [], 3: [], 4: []}
    for patient in stats["patients"]:
        types[patient["type"]].append(patient["total_time"])

    for patient_type, times in types.items():
        if times:
            avg_time = sum(times) / len(times)
            print(f"Type {patient_type}: {len(times)} patients, Avg. time = {avg_time:.2f} minutes")
        else:
            print(f"Type {patient_type}: 0 patients")

    # Overall average time
    all_times = [patient["total_time"] for patient in stats["patients"]]
    overall_avg_time = sum(all_times) / total_patients
    print(f"Overall average treatment time: {overall_avg_time:.2f} minutes")

    # Standard deviation
    for patient in stats["patients"]:
        temp = [math.pow((patient["total_time"] - overall_avg_time),2)]
    standard_deviation = math.sqrt(sum(temp)/(total_patients-1))
    print(f"Standard deviation treatment time: {standard_deviation:.2f} minutes")

# Hauptprogramm
if __name__ == "__main__":
    run_simulation()
