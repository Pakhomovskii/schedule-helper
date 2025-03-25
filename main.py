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

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

def main():
    # Загрузка переменных окружения из .env (если используется)
    load_dotenv()

    # Определяем группы
    groups = {
        "Calculus Study Group (5 students)": Group("Calculus Study Group", 5),
        "Radio Engineering Club (12 students)": Group("Radio Engineering Club", 12),
        "OOP in Python Seminar (28 students)": Group("OOP in Python Seminar", 28),
        "Algorithms Class (15 students)": Group("Algorithms Class", 15),
        "Facultative Seminar (15 students)": Group("Facultative Seminar", 15),
    }

    # Определяем аудитории
    auditoriums = [
        Auditorium("Classroom 101 10-11 am capacity 8", 8, "Monday", TimeSlot(time(10, 0), time(11, 30))),
        Auditorium("Lecture Hall B 13-15 pm capacity 20", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))),
        Auditorium("Main Auditorium 9-10 am capacity 35", 35, "Monday", TimeSlot(time(9, 0), time(10, 30))),
        Auditorium("Classroom 102 12-13:00 pm capacity 35", 35, "Monday", TimeSlot(time(12, 0), time(13, 30))),
        Auditorium("Classroom 103 16-17:30 pm capacity 20", 20, "Monday", TimeSlot(time(16, 0), time(17, 30))),
    ]

    # Определяем преподавателей и их предпочтения напрямую
    teachers = {
        "Mahmoudreza Babaei": Teacher("Mahmoudreza", "Babaei", groups["Calculus Study Group (5 students)"], TimePeriod.MORNING),
        "Ghadeer Marwan": Teacher("Ghadeer", "Marwan", groups["Radio Engineering Club (12 students)"], TimePeriod.AFTERNOON),
        "William Morrison": Teacher("William", "Morrison", groups["OOP in Python Seminar (28 students)"], TimePeriod.MORNING),
        "Alexandr Bell": Teacher("Alexandr", "Bell", groups["Algorithms Class (15 students)"], TimePeriod.MIDDAY),
    }

    # Выполнение алгоритма сопоставления
    matches, unmatched_teachers = gale_shapley_matching(teachers, auditoriums)
    logger.info(f"Matches: {matches}")
    logger.info(f"Unmatched Teachers: {unmatched_teachers}")

    # Вывод результатов в консоль
    print("Matches:")
    for teacher, auditorium in matches.items():
        print(f"{teacher} -> {auditorium}")

    if unmatched_teachers:
        print("\nUnmatched Teachers:")
        for teacher in unmatched_teachers:
            print(teacher)

if __name__ == "__main__":
    main()
