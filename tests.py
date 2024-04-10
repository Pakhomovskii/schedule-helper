from datetime import time

from gale_shapley_matching import TimeSlot, Auditorium, Group, Teacher, gale_shapley_matching, TimePeriod

group1 = Group("Calculus Study Group", 5)  # small group
group2 = Group("Chemistry Club", 12)  # medium group
group3 = Group("History Seminar", 28)  # large group
group4 = Group("Math main Seminar", 29)  # large group

# teachers with single groups only
teacher1 = Teacher("Emily", "Johnson", group1, TimePeriod.MORNING)
teacher2 = Teacher("Bob", "Williams", group2, TimePeriod.AFTERNOON)
teacher3 = Teacher("Sarah", "Lee", group3, TimePeriod.MORNING)
teacher4 = Teacher("Sarah2", "Lee2", group4, TimePeriod.MIDDAY)

auditorium1 = Auditorium(
    "Classroom 101", 8, "Tuesday", TimeSlot(time(10, 0), time(11, 30))
)
auditorium2 = Auditorium(
    "Lecture Hall B", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))
)
auditorium3 = Auditorium(
    "Main Auditorium", 35, "Wednesday", TimeSlot(time(9, 0), time(10, 30))
)

auditorium4 = Auditorium(
    "Main Auditorium", 35, "Wednesday", TimeSlot(time(9, 0), time(10, 30))
)

auditorium5 = Auditorium(
    "Main2 Auditorium", 35, "Wednesday", TimeSlot(time(15, 0), time(10, 30))
)

teachers = {
    "teacher1": teacher1,
    "teacher2": teacher2,
    "teacher3": teacher3,
    "teacher4": teacher4,
}

auditoriums = {
    "auditorium1": auditorium1,
    "auditorium2": auditorium2,
    "auditorium3": auditorium3,
    "auditorium4": auditorium4,
    "auditorium5": auditorium5,
}

matches, unmatched_teachers = gale_shapley_matching(teachers, auditoriums.values())

print("Matches:")
for teacher, auditorium in matches.items():
    print(f"{teacher} -> {auditorium}")

print("\nUnmatched Teachers:")
for teacher in unmatched_teachers:
    print(teacher)
