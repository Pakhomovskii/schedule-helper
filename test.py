from datetime import time


group1 = Group("Calculus Study Group", 5)  # Small group
group2 = Group("Chemistry Club", 12)  # Medium group
group3 = Group("History Seminar", 28)  # Large group

# Teachers with single groups only
teacher1 = Teacher("Emily", "Johnson", group1)
teacher2 = Teacher("Bob", "Williams", group2)
teacher3 = Teacher("Sarah", "Lee", group3)

auditorium1 = Auditorium(
    "Classroom 101", 8, "Tuesday", TimeSlot(time(10, 0), time(11, 30))
)
auditorium2 = Auditorium(
    "Lecture Hall B", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))
)
auditorium3 = Auditorium(
    "Main Auditorium", 35, "Wednesday", TimeSlot(time(9, 0), time(10, 30))
)

teachers = {
    "teacher1": teacher1,
    "teacher2": teacher2,
    "teacher3": teacher3,
}

auditoriums = {
    "auditorium1": auditorium1,
    "auditorium2": auditorium2,
    "auditorium3": auditorium3,
}

matches, unmatched_teachers = gale_shapley_matching(teachers, auditoriums)

print("Matches:")
for teacher, auditorium in matches.items():
    print(f"{teacher} -> {auditorium}")

print("\nUnmatched Teachers:")
for teacher in unmatched_teachers:
    print(teacher)
