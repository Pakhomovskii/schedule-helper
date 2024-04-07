import uuid


class SizeCategory:
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class Preference:
    HIGH = 1
    MEDIUM = 0
    LOW = -1


class Teacher:
    def __init__(self, name, surname, group, schedule=None):
        self.id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.group = group
        self.schedule = schedule or []


class Group:
    def __init__(self, name, students):
        self.id = uuid.uuid4()
        self.name = name
        self.size_category = self.get_size_category(students)

    @classmethod
    def get_size_category(cls, students):
        match students:
            case students if students <= 10:
                return SizeCategory.SMALL
            case students if students <= 20:
                return SizeCategory.MEDIUM
            case _:  # Default case for students > 20
                return SizeCategory.LARGE


class TimeSlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


class Auditorium:
    def __init__(self, name, capacity, day, time_slot):
        self.name = name
        self.capacity = capacity
        self.day = day
        self.preferences = self.calculate_preferences(capacity)
        self.time_slot = time_slot  # Now stores a TimeSlot

    @classmethod
    def calculate_preferences(cls, capacity):
        match capacity:
            case capacity if capacity <= 10:
                return {
                    SizeCategory.SMALL: Preference.HIGH,
                    SizeCategory.MEDIUM: Preference.MEDIUM,
                    SizeCategory.LARGE: Preference.LOW,
                }
            case capacity if capacity <= 20:
                return {
                    SizeCategory.SMALL: Preference.LOW,
                    SizeCategory.MEDIUM: Preference.HIGH,
                    SizeCategory.LARGE: Preference.MEDIUM,
                }
            case _:  # Default case for capacity > 20
                return {
                    SizeCategory.SMALL: Preference.LOW,
                    SizeCategory.MEDIUM: Preference.MEDIUM,
                    SizeCategory.LARGE: Preference.HIGH,
                }


def overlap(time_slot1, time_slot2):
    return (
        time_slot1.start_time < time_slot2.end_time
        and time_slot2.start_time < time_slot1.end_time
    )


def is_schedule_conflict(teacher, auditorium):
    return auditorium.day in [aud.day for aud in teacher.schedule] and any(
        overlap(auditorium.time_slot, aud.time_slot) for aud in teacher.schedule
    )


def gale_shapley_matching(teachers, auditoriums):
    unmatched_teachers = set(teachers.keys())
    teacher_matches = {}
    auditorium_matches = {auditorium: None for auditorium in auditoriums.keys()}

    while unmatched_teachers:
        teacher_name = unmatched_teachers.pop()
        teacher = teachers[teacher_name]
        teacher_group_size_category = teacher.group.size_category

        for preferred_auditorium in sorted(
            auditoriums,
            key=lambda aud: auditoriums[aud].preferences[teacher_group_size_category],
            reverse=True,
        ):
            auditorium_preference = auditoriums[preferred_auditorium].preferences
            if auditorium_matches[preferred_auditorium] is None:
                if not is_schedule_conflict(teacher, auditoriums[preferred_auditorium]):
                    teacher_matches[teacher_name] = preferred_auditorium
                    auditorium_matches[preferred_auditorium] = teacher_name
                    break
            else:
                current_matched_teacher_name = auditorium_matches[preferred_auditorium]
                current_matched_teacher = teachers[current_matched_teacher_name]
                current_matched_teacher_group_size_category = (
                    current_matched_teacher.group.size_category
                )

                if (
                    auditorium_preference[teacher_group_size_category]
                    > auditorium_preference[current_matched_teacher_group_size_category]
                ):
                    unmatched_teachers.add(current_matched_teacher_name)
                    teacher_matches[teacher_name] = preferred_auditorium
                    auditorium_matches[preferred_auditorium] = teacher_name
                    break

    return teacher_matches, unmatched_teachers
