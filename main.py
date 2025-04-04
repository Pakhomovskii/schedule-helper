import logging
from datetime import time
import os
from dotenv import load_dotenv


from gale_shapley_matching import (
    TimeSlot,
    Auditorium,
    Group,
    Teacher,
    gale_shapley_matching,
    TimePeriod,
)


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

### here we can test other data
    groups_data = {
        "Calculus": Group("Calculus Study Group", 5), # Small
        "Radio Eng": Group("Radio Engineering Club", 12), # Medium
        "OOP Python": Group("OOP in Python Seminar", 28), # Large
        "Algorithms": Group("Algorithms Class", 15), # Medium
        "Facultative": Group("Facultative Seminar", 15), # Medium
        "Quantum Physics": Group("Quantum Physics Intro", 9), # Small
    }

    # auditorium
    auditoriums_list = [
  
        Auditorium("Classroom 101", 8, "Monday", TimeSlot(time(10, 0), time(11, 30))), # Small, Morning
        Auditorium("Lecture Hall B", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))), # Medium, Midday
        Auditorium("Main Auditorium", 35, "Monday", TimeSlot(time(9, 0), time(10, 30))), # Large, Morning
        Auditorium("Classroom 102", 35, "Monday", TimeSlot(time(12, 0), time(13, 30))), # Large, Midday
        Auditorium("Classroom 103", 20, "Monday", TimeSlot(time(16, 0), time(17, 30))), # Medium, Afternoon
        Auditorium("Small Room 5", 10, "Tuesday", TimeSlot(time(9, 0), time(10, 0))), # Small, Morning (на другой день)
    ]

    # Teachers
    teachers_dict = {
        "Mahmoudreza Babaei": Teacher("Mahmoudreza", "Babaei", groups_data["Calculus"], TimePeriod.MORNING),
        "Ghadeer Marwan": Teacher("Ghadeer", "Marwan", groups_data["Radio Eng"], TimePeriod.AFTERNOON),
        "William Morrison": Teacher("William", "Morrison", groups_data["OOP Python"], TimePeriod.MORNING),
        "Alexandr Bell": Teacher("Alexandr", "Bell", groups_data["Algorithms"], TimePeriod.MIDDAY),
        
        
        "Maria Curie": Teacher("Maria", "Curie", groups_data["Quantum Physics"], TimePeriod.MORNING),
        "John Doe": Teacher("John", "Doe", groups_data["Facultative"], TimePeriod.MIDDAY),
    }


    matches, unmatched = gale_shapley_matching(teachers_dict, auditoriums_list)
    logger.info(f"Matching process complete.")


    print("\n--- Matching Results ---")
    print("Matches:")
    if matches:
        for teacher_name, auditorium in sorted(matches.items()):
            print(f"- {teacher_name} -> {auditorium}")
    else:
        print("No matches found.")

    if unmatched:
        print("Unmatched Teachers:")
        for teacher_name in sorted(list(unmatched)):
            print(f"- {teacher_name}")
    else:
        print("All teachers were matched.")

    print("------------------------\n")


if __name__ == "__main__":
    main()
