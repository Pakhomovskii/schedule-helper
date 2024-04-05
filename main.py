
class Teacher:
    def __init__(self, name, num_students, preferred_auditoriums):
        self.name = name
        self.num_students = num_students
        self.preferred_auditoriums = preferred_auditoriums


class Auditorium:
    def __init__(self, name, capacity, priorities):
        self.name = name
        self.capacity = capacity
        self.priorities = priorities


def gale_shapley_matching(teachers, auditoriums):
    unmatched_teachers = set(teacher.name for teacher in teachers)
    teacher_matches = {}
    auditorium_matches = {auditorium.name: None for auditorium in auditoriums}
    auditorium_capacities = {auditorium.name: auditorium.capacity for auditorium in auditoriums}

    def get_priority(auditorium, num_students):
        for capacity, priority in auditorium.priorities.items():
            if num_students <= capacity:
                return priority
        return None

    max_iterations = len(teachers) * len(auditoriums)
    iteration = 0

    while unmatched_teachers and iteration < max_iterations:
        teacher_name = unmatched_teachers.pop()
        teacher = next((t for t in teachers if t.name == teacher_name), None)

        for auditorium_name in teacher.preferred_auditoriums:
            auditorium = next((a for a in auditoriums if a.name == auditorium_name), None)
            if auditorium is None:
                continue

            if auditorium_matches[auditorium.name] is None:
                priority = get_priority(auditorium, teacher.num_students)
                if priority is not None:
                    teacher_matches[teacher.name] = auditorium.name
                    auditorium_matches[auditorium.name] = teacher.name
                    auditorium_capacities[auditorium.name] -= teacher.num_students
                    break
            else:
                matched_teacher_name = auditorium_matches[auditorium.name]
                matched_teacher = next((t for t in teachers if t.name == matched_teacher_name), None)
                current_priority = get_priority(auditorium, teacher.num_students)
                matched_priority = get_priority(auditorium, matched_teacher.num_students)

                if current_priority is not None and (
                        matched_priority is None or current_priority > matched_priority
                ):
                    teacher_matches[teacher.name] = auditorium.name
                    auditorium_matches[auditorium.name] = teacher.name
                    auditorium_capacities[auditorium.name] += matched_teacher.num_students
                    auditorium_capacities[auditorium.name] -= teacher.num_students
                    unmatched_teachers.add(matched_teacher_name)
                    break

        iteration += 1

    return teacher_matches, unmatched_teachers


teachers = [
    Teacher("T1", 15, ["A1_10", "A2_10", "A3_10"]),
    Teacher("T2", 25, ["A2_10", "A3_10", "A1_10"]),
    Teacher("T3", 20, ["A3_10", "A1_10", "A2_10"]),
    Teacher("T4", 30, ["A1_10", "A3_10", "A2_10"]),
    Teacher("T5", 10, ["A2_10", "A1_10", "A3_10"])
]

auditoriums = [
    Auditorium("A1_10", 30, {30: "high", 25: "medium", 20: "low"}),
    Auditorium("A2_10", 25, {25: "high", 20: "medium", 15: "low"}),
    Auditorium("A3_10", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A4_10", 30, {30: "high", 25: "medium", 20: "low"}),
    Auditorium("A5_10", 25, {25: "high", 20: "medium", 15: "low"}),
    Auditorium("A1_11", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A2_11", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A3_11", 30, {30: "high", 25: "medium", 20: "low"}),
    Auditorium("A4_11", 25, {25: "high", 20: "medium", 15: "low"}),
    Auditorium("A5_11", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A1_12", 30, {30: "high", 25: "medium", 20: "low"}),
    Auditorium("A2_12", 25, {25: "high", 20: "medium", 15: "low"}),
    Auditorium("A3_12", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A4_12", 20, {20: "high", 15: "medium", 10: "low"}),
    Auditorium("A5_12", 20, {20: "high", 15: "medium", 10: "low"})
]


matches, unmatched_teachers = gale_shapley_matching(teachers, auditoriums)


print("Matches:")
for teacher, auditorium in matches.items():
    print(f"{teacher} -> {auditorium}")

print("\nUnmatched Teachers:")
for teacher in unmatched_teachers:
    print(teacher)


teachers2 = [
    Teacher("T1", 20, ["A1", "A2", "A3", "A4"]),
    Teacher("T2", 30, ["A2", "A3", "A4", "A1"]),
    Teacher("T3", 25, ["A3", "A4", "A1", "A2"]),
    Teacher("T4", 15, ["A4", "A1", "A2", "A3"]),
    Teacher("T5", 35, ["A1", "A2", "A3", "A4"]),
    Teacher("T6", 40, ["A2", "A3", "A4", "A1"])
]

auditoriums2 = [
    Auditorium("A1", 50, {50: "high", 40: "medium", 30: "low"}),
    Auditorium("A2", 45, {45: "high", 35: "medium", 25: "low"}),
    Auditorium("A3", 40, {40: "high", 30: "medium", 20: "low"}),
    Auditorium("A4", 35, {35: "high", 25: "medium", 15: "low"})
]

# Входные данные 3
teachers1 = [
    Teacher("T1", 18, ["A1", "A2", "A3", "A4", "A5"]),
    Teacher("T2", 22, ["A2", "A3", "A4", "A5", "A1"]),
    Teacher("T3", 27, ["A3", "A4", "A5", "A1", "A2"]),
    Teacher("T4", 16, ["A4", "A5", "A1", "A2", "A3"]),
    Teacher("T5", 20, ["A5", "A1", "A2", "A3", "A4"]),
    Teacher("T6", 24, ["A1", "A2", "A3", "A4", "A5"]),
    Teacher("T7", 30, ["A2", "A3", "A4", "A5", "A1"])
]

auditoriums1 = [
    Auditorium("A1", 40, {40: "high", 35: "medium", 30: "low"}),
    Auditorium("A2", 35, {35: "high", 30: "medium", 25: "low"}),
    Auditorium("A3", 30, {30: "high", 25: "medium", 20: "low"}),
    Auditorium("A4", 25, {25: "high", 20: "medium", 15: "low"}),
    Auditorium("A5", 20, {20: "high", 15: "medium", 10: "low"})
]


