import logging
from datetime import time
import streamlit as st
from gale_shapley_matching import Group, Auditorium, TimeSlot, gale_shapley_matching, Teacher, TimePeriod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    groups = {
        "Calculus Study Group (5 students)": Group("Calculus Study Group", 5),
        "Radio Engineering Club (12 students)": Group("Radio Engineering Club", 12),
        "OOP in Python Seminar (28 students)": Group("OOP in Python Seminar", 28),
        "Algorithms Class (15 students)": Group("Algorithms Class", 15),
        "Facultative Seminar (15 students)": Group("Facultative Seminar", 15),
    }

    auditoriums_list = [
        Auditorium("Classroom 101 10-11 am", 8, "Monday", TimeSlot(time(10, 0), time(11, 30))),
        Auditorium("Lecture Hall B 13-15 pm", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))),
        Auditorium("Main Auditorium 9-10 am", 35, "Monday", TimeSlot(time(9, 0), time(10, 30))),
        Auditorium("Classroom 102 Auditorium 12-13:00 pm", 35, "Monday", TimeSlot(time(12, 0), time(13, 30))),
        Auditorium("Classroom 103 Auditorium 16-17:30 pm", 20, "Monday", TimeSlot(time(16, 0), time(17, 30))),
    ]

    auditoriums = {auditorium.name: auditorium for auditorium in auditoriums_list}

    st.title("Teacher Preferences for Auditoriums and Groups")

    tab1, tab2, tab3, tab4 = st.tabs(["Dr. Mahmoudreza Babaei", "Dr. Ghadeer Marwan", "William Morrison", "Dr. Alexandr Bell"])

    teachers = ["Mahmoudreza Babaei", "Ghadeer Marwan", "William Morrison", "Alexandr Bell"]

    teacher_preferences = {}

    for i, tab in enumerate([tab1, tab2, tab3, tab4]):
        with tab:
            st.write(f"Preferences for {teachers[i]}")

            group_choice = st.selectbox(
                f"Choose your group (Teacher {i + 1})",
                list(groups.keys()),
                key=f"group{i}",
            )

            auditorium_choice = st.selectbox(
                f"Choose your preferred auditorium (Teacher {i + 1})",
                list(auditoriums.keys()),
                key=f"auditorium{i}",
            )

            time_preference = st.selectbox(
                f"Choose your preferred time slot (Teacher {i + 1})",
                list(TimePeriod),
                key=f"time_preference{i}"
            )

            teacher_preferences[teachers[i]] = {
                "group": group_choice,
                "auditorium": auditorium_choice,
                "time_preference": time_preference
            }

    if st.button("Finalize Choices and Match"):

        teachers_dict = {}
        for teacher_name, prefs in teacher_preferences.items():
            group_name = prefs['group']
            teacher_group = groups[group_name]

            name, surname = teacher_name.split()
            time_preference = prefs["time_preference"]
            teacher_obj = Teacher(name, surname, teacher_group, time_preference)

            teachers_dict[teacher_name] = teacher_obj

        matches, unmatched_teachers = gale_shapley_matching(teachers_dict, auditoriums.values())
        logger.info(
            f"matches: {matches}"
        )
        logger.info(
            f"teacher_preferences: {teacher_preferences}"
        )

        st.subheader("Matching Results")
        for teacher, matched_auditorium in matches.items():
            st.write(f"{teacher} -> {matched_auditorium}")

        if unmatched_teachers:
            st.subheader("Unmatched Teachers")
            for teacher in unmatched_teachers:
                st.write(f"- {teacher}")
