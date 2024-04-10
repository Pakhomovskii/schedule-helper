import uuid
from enum import Enum


class SizeCategory(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class TimePeriod(Enum):
    MORNING = "Morning"
    MIDDAY = "Midday"
    AFTERNOON = "Afternoon"


class Preference(Enum):
    HIGH = 1
    MEDIUM = 0
    LOW = -1


class Teacher:
    def __init__(self, name, surname, group, time_preference, schedule=None):
        self.id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.group = group
        self.time_preference = time_preference
        self.schedule = schedule or []

    @classmethod
    def calculate_preferences(cls, time):
        match time:
            case time if time == "Morning":
                return {
                    TimePeriod.MORNING: Preference.HIGH,
                    TimePeriod.AFTERNOON: Preference.LOW,
                    TimePeriod.MIDDAY: Preference.LOW,
                }
            case time if time == "Midday":
                return {
                    TimePeriod.MIDDAY: Preference.HIGH,
                    TimePeriod.AFTERNOON: Preference.LOW,
                    TimePeriod.MORNING: Preference.LOW,
                }
            case time if time == "Afternoon":
                return {
                    TimePeriod.AFTERNOON: Preference.HIGH,
                    TimePeriod.MORNING: Preference.LOW,
                    TimePeriod.MIDDAY: Preference.LOW,
                }


class Group:
    def __init__(self, name, students):
        self.id = uuid.uuid4()
        self.name = name
        self.size_category = self.get_size_category(students)
        self.size = self.size_category.value

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

    @classmethod
    def get_slot_period(cls, start_time, end_time):
        match start_time, end_time:
            case end_time if end_time < 12:
                return TimePeriod.MORNING
            case start_time, end_time if end_time >= 12 and start_time < 15:
                return TimePeriod.MIDDAY
            case start_time if start_time >= 15:
                return TimePeriod.AFTERNOON


class Auditorium:
    def __init__(self, name, capacity, day, time_slot):
        self.name = name
        self.capacity = capacity
        self.day = day
        self.preferences = self.calculate_preferences(capacity)
        self.time_slot = time_slot
        self.size_category = self.get_size_category(capacity)

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

    @classmethod
    def get_size_category(cls, capacity):
        if capacity <= 10:
            return SizeCategory.SMALL
        elif capacity <= 20:
            return SizeCategory.MEDIUM
        else:
            return SizeCategory.LARGE

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


def get_teacher_preference_score(teacher, auditorium):
    # Prioritize time match, with some consideration for matching capacity size
    time_score = 3 if teacher.time_preference == auditorium.time_slot.start_time else 1
    size_score = 1 if teacher.group.size_category == auditorium.size_category else 0.5
    return time_score + size_score


def is_auditorium_suitable(teacher, auditorium, auditorium_matches):
    # We can use a strict rule here if necessary.
    # For example group.size_category == auditorium.size_category
    return not is_schedule_conflict(teacher, auditorium) and len(auditorium_matches[auditorium.name]) == 0


def is_teacher_better_match(new_teacher, auditorium, old_teacher):
    # An auditorium ALWAYS prefers being full if possible
    size_mapping = {
        SizeCategory.SMALL: 10,
        SizeCategory.MEDIUM: 20,
        SizeCategory.LARGE: 30
    }
    if old_teacher is None:
        return True
    # Otherwise, prefer the teacher with the closer size match
    new_size_diff = abs(auditorium.capacity - size_mapping[new_teacher.group.size_category])
    old_size_diff = abs(auditorium.capacity - size_mapping[old_teacher.group.size_category])
    return new_size_diff < old_size_diff


def gale_shapley_matching(teachers, auditoriums):
    unmatched_teachers = set(teachers.keys())
    teacher_matches = {}
    auditorium_matches = {auditorium.name: set() for auditorium in auditoriums}

    while unmatched_teachers:
        teacher_name = unmatched_teachers.pop()
        teacher = teachers[teacher_name]

        for preferred_auditorium in sorted(
                list(auditoriums),
                key=lambda aud: get_teacher_preference_score(teacher, aud),
                reverse=True,
        ):
            if is_auditorium_suitable(teacher, preferred_auditorium, auditorium_matches):
                teacher_matches[teacher_name] = preferred_auditorium
                auditorium_matches[preferred_auditorium.name].add(teacher_name)
                break
            else:
                current_matched_teacher_names = auditorium_matches[preferred_auditorium.name]
                for current_matched_teacher_name in current_matched_teacher_names:
                    current_matched_teacher = teachers[current_matched_teacher_name]

                    if is_teacher_better_match(teacher, preferred_auditorium, current_matched_teacher):
                        unmatched_teachers.add(current_matched_teacher_name)
                        teacher_matches[teacher_name] = preferred_auditorium
                        auditorium_matches[preferred_auditorium.name] = {teacher_name}
                        break

    return teacher_matches, unmatched_teachers
