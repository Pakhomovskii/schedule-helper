from datetime import time
import logging
from gale_shapley_matching import (
    TimeSlot,
    Auditorium,
    Group,
    Teacher,
    gale_shapley_matching,
    TimePeriod,
)

logging.basicConfig(level=logging.INFO)

# Step 1: Define your groups
group1 = Group("Calculus Study Group", 5)
group2 = Group("Chemistry Club", 12)
group3 = Group("History Seminar", 28)

# Step 2: Define your teachers
teacher1 = Teacher("Emily", "Johnson", group1, TimePeriod.MORNING)
teacher2 = Teacher("Bob", "Williams", group2, TimePeriod.AFTERNOON)
teacher3 = Teacher("Sarah", "Lee", group3, TimePeriod.MORNING)

teachers = {
    "teacher1": teacher1,
    "teacher2": teacher2,
    "teacher3": teacher3,
}

# Step 3: Define your auditoriums
auditorium1 = Auditorium("Classroom 101", 8, "Tuesday", TimeSlot(time(10, 0), time(11, 30)))
auditorium2 = Auditorium("Lecture Hall B", 20, "Monday", TimeSlot(time(13, 0), time(15, 30)))

auditoriums = [auditorium1, auditorium2]

# Step 4: Perform the matching
matches, unmatched_teachers = gale_shapley_matching(teachers, auditoriums)

# Step 5: Print/log the results
print("Matches:")
for teacher, auditorium in matches.items():
    print(f"{teacher} -> {auditorium}")

if unmatched_teachers:
    print("\nUnmatched Teachers:")
    for teacher in unmatched_teachers:
        print(teacher)
