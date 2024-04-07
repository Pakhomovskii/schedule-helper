from datetime import time
import streamlit as st
from gale_shapley_matching import Group, Auditorium, TimeSlot, gale_shapley_matching, Teacher

if __name__ == "__main__":

    groups = {
        "Calculus Study Group (5 students)": Group("Calculus Study Group", 5),
        "Chemistry Club (12 students)": Group("Chemistry Club", 12),
        "History Seminar (28 students)": Group("History Seminar", 28),
    }

    auditoriums = {
        "Classroom 101 (capacity 8)": Auditorium(
            "Classroom 101", 8, "Tuesday", TimeSlot(time(10, 0), time(11, 30))
        ),
        "Lecture Hall B (capacity 20)": Auditorium(
            "Lecture Hall B", 20, "Monday", TimeSlot(time(13, 0), time(15, 30))
        ),
        "Main Auditorium (capacity 35)": Auditorium(
            "Main Auditorium", 35, "Wednesday", TimeSlot(time(9, 0), time(10, 30))
        ),
    }

    st.title("Teacher Preferences for Auditoriums and Groups")

    tab1, tab2, tab3 = st.tabs(["Pr. Jonson", "Pr. Williams", "Pr. Lee"])

    teachers = ["Emily Johnson", "Bob Williams", "Sarah Lee"]

    teacher_preferences = {}

    for i, tab in enumerate([tab1, tab2, tab3]):
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

            teacher_preferences[teachers[i]] = {
                "group": group_choice,
                "auditorium": auditorium_choice,
            }

    if st.button("Finalize Choices and Match"):

        teachers_dict = {}
        for teacher_name, prefs in teacher_preferences.items():
            group_name = prefs['group']
            teacher_group = groups[group_name]

            name, surname = teacher_name.split()
            teacher_obj = Teacher(name, surname, teacher_group)

            teachers_dict[teacher_name] = teacher_obj

        matches, unmatched_teachers = gale_shapley_matching(teachers_dict, auditoriums)
        st.subheader("Matching Results")
        for teacher, matched_auditorium in matches.items():
            st.write(f"{teacher} -> {matched_auditorium}")

        if unmatched_teachers:
            st.subheader("Unmatched Teachers")
            for teacher in unmatched_teachers:
                st.write(f"- {teacher}")
