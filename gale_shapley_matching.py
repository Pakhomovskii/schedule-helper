# gale_shapley_matching.py

import uuid
import logging
from datetime import time, datetime
from enum import Enum
from typing import List, Dict, Tuple, Optional, Set, Any


class SizeCategory(Enum):
    SMALL = "Small (<=10)"
    MEDIUM = "Medium (11-20)"
    LARGE = "Large (>20)"


class TimePeriod(Enum):
    MORNING = "Morning (<12:00)"
    MIDDAY = "Midday (12:00-14:59)"
    AFTERNOON = "Afternoon (>=15:00)"


class Preference(Enum):
    HIGH = 1
    MEDIUM = 0
    LOW = -1


class TimeSlot:
    def __init__(self, start_time: time, end_time: time):
        if not isinstance(start_time, time) or not isinstance(end_time, time):
            raise TypeError("start_time and end_time must be datetime.time objects")
        if start_time >= end_time:
            raise ValueError(f"Start time {start_time} must be before end time {end_time}")
        self.start_time = start_time
        self.end_time = end_time
        self.period = self._get_slot_period()  # Calculate period on initialization

    def _get_slot_period(self) -> TimePeriod:
        """Determines the TimePeriod based on the start time."""
        start_hour = self.start_time.hour
        if start_hour < 12:
            return TimePeriod.MORNING
        elif 12 <= start_hour < 15:
            return TimePeriod.MIDDAY
        else:  # start_hour >= 15
            return TimePeriod.AFTERNOON

    def __str__(self) -> str:
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} ({self.period.value})"

    def overlaps(self, other: 'TimeSlot') -> bool:
        """Checks if this time slot overlaps with another."""
        return self.start_time < other.end_time and other.start_time < self.end_time


class Group:
    def __init__(self, name: str, num_students: int):
        if num_students <= 0:
            raise ValueError("Number of students must be positive.")
        self.id = uuid.uuid4()
        self.name = name
        self.num_students = num_students
        self.size_category = self._get_size_category(num_students)

    @staticmethod
    def _get_size_category(students: int) -> SizeCategory:
        if students <= 10:
            return SizeCategory.SMALL
        elif students <= 20:
            return SizeCategory.MEDIUM
        else:  # students > 20
            return SizeCategory.LARGE

    def __str__(self) -> str:
        return f"{self.name} ({self.num_students} students, {self.size_category.value})"


class Auditorium:
    def __init__(self, name: str, capacity: int, day: str, time_slot: TimeSlot):
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity
        self.day = day  # Assuming simple day string for now
        self.time_slot = time_slot
        self.size_category = self._get_size_category(capacity)
        # Preferences based on how well *group sizes* fit this auditorium's category
        self.preferences = self._calculate_preferences(self.size_category)

    @staticmethod
    def _get_size_category(capacity: int) -> SizeCategory:
        # Consistent with Group size category logic for easier comparison
        if capacity <= 10:
            return SizeCategory.SMALL
        elif capacity <= 20:
            return SizeCategory.MEDIUM
        else:  # capacity > 20
            return SizeCategory.LARGE

    @staticmethod
    def _calculate_preferences(aud_size_category: SizeCategory) -> Dict[SizeCategory, Preference]:
        """How much this auditorium prefers groups of different size categories."""
        prefs = {}
        # Prefers groups that match its own size category perfectly
        prefs[aud_size_category] = Preference.HIGH

        # Example preference logic (can be customized)
        if aud_size_category == SizeCategory.SMALL:
            prefs[SizeCategory.MEDIUM] = Preference.LOW
            prefs[SizeCategory.LARGE] = Preference.LOW
        elif aud_size_category == SizeCategory.MEDIUM:
            prefs[SizeCategory.SMALL] = Preference.MEDIUM  # Might accept small groups
            prefs[SizeCategory.LARGE] = Preference.LOW  # Less preferred
        elif aud_size_category == SizeCategory.LARGE:
            prefs[SizeCategory.SMALL] = Preference.LOW
            prefs[SizeCategory.MEDIUM] = Preference.MEDIUM  # Might accept medium groups

        # Ensure all categories are present
        for cat in SizeCategory:
            if cat not in prefs:
                # Default preference if not explicitly set (e.g., Large aud for Large group was HIGH)
                if cat == aud_size_category: continue  # Already set to HIGH
                # Assign a default low/medium preference if needed, adjust logic as required
                prefs[cat] = Preference.MEDIUM  # Example default

        return prefs

    def __str__(self) -> str:
        return f"{self.name} (Cap: {self.capacity}, {self.size_category.value}, Day: {self.day}, Slot: {self.time_slot})"

    def __hash__(self):
        # Needed to use Auditorium objects as dictionary keys
        return hash(self.id)

    def __eq__(self, other):
        # Needed for comparing Auditorium objects
        if not isinstance(other, Auditorium):
            return NotImplemented
        return self.id == other.id


class Teacher:
    def __init__(self, name: str, surname: str, group: Group, time_preference: TimePeriod,
                 schedule: Optional[List[Auditorium]] = None):
        self.id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.full_name = f"{name} {surname}"
        self.group = group
        self.time_preference = time_preference  # Teacher's preferred TimePeriod
        # Schedule stores assigned Auditoriums (which include TimeSlots)
        self.schedule: List[Auditorium] = schedule or []

    @staticmethod
    def calculate_time_preferences(pref: TimePeriod) -> Dict[TimePeriod, Preference]:
        """ How much a teacher prefers teaching in each time period, based on their main preference. """
        prefs = {p: Preference.LOW for p in TimePeriod}  # Default to low
        prefs[pref] = Preference.HIGH  # Strong preference for their chosen period
        # preference for adjacent slots if desired # TODO
        # Example: If pref is MIDDAY, maybe MORNING/AFTERNOON are MEDIUM?
        return prefs

    def __str__(self) -> str:
        return f"{self.full_name} (Group: {self.group.name}, Prefers: {self.time_preference.value})"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Teacher):
            return NotImplemented
        return self.id == other.id


# --- Matching Logic Helper Functions ---

def is_schedule_conflict(teacher: Teacher, auditorium: Auditorium) -> bool:
    """Checks if assigning the auditorium conflicts with the teacher's existing schedule."""
    for assigned_aud in teacher.schedule:
        if assigned_aud.day == auditorium.day and assigned_aud.time_slot.overlaps(auditorium.time_slot):
            return True
    return False


def get_teacher_preference_score(teacher: Teacher, auditorium: Auditorium) -> float:
    """
    Calculates a score representing how much a teacher prefers an auditorium.
    Higher score means higher preference.
    Returns -1.0 if the teacher's group doesn't fit.
    """
    # CRITICAL: Teacher must fit in the auditorium
    if teacher.group.num_students > auditorium.capacity:
        return -1.0  # Impossible match, lowest score

    # 1. Time Preference Score (Primary)
    auditorium_period = auditorium.time_slot.period
    time_match_preference = Teacher.calculate_time_preferences(teacher.time_preference).get(auditorium_period,
                                                                                            Preference.LOW)

    # Convert Preference enum to a numerical score (e.g., HIGH=3, MEDIUM=1, LOW=0)
    time_score = 0
    if time_match_preference == Preference.HIGH:
        time_score = 3
    elif time_match_preference == Preference.MEDIUM:
        time_score = 1
    # LOW gives time_score = 0

    # 2. Size Fit Score (Secondary) - How well the group fits the auditorium
    # Using the auditorium's preference for the teacher's group size category
    size_match_preference = auditorium.preferences.get(teacher.group.size_category, Preference.LOW)
    size_score = 0
    if size_match_preference == Preference.HIGH:
        size_score = 1.0
    elif size_match_preference == Preference.MEDIUM:
        size_score = 0.5
    # LOW gives size_score = 0

    # Combine scores (prioritizing time)
    # Adjust weighting as needed
    return time_score + size_score


def is_teacher_better_match(
        new_teacher: Teacher,
        auditorium: Auditorium,
        current_teacher: Teacher
) -> bool:
    """
    Checks if the new_teacher is a better match for the auditorium than the current_teacher.
    This reflects the *auditorium's* preference.
    """
    # CRITICAL: New teacher must fit
    if new_teacher.group.num_students > auditorium.capacity:
        return False  # Cannot be a better match if they don't fit

    # Preference based on how well the group size fits the auditorium category
    new_teacher_fit = auditorium.preferences.get(new_teacher.group.size_category, Preference.LOW)
    current_teacher_fit = auditorium.preferences.get(current_teacher.group.size_category, Preference.LOW)

    # Compare preference levels (HIGH > MEDIUM > LOW)
    if new_teacher_fit.value > current_teacher_fit.value:
        return True
    elif new_teacher_fit.value < current_teacher_fit.value:
        return False
    else:
        # Tie-breaking (optional): If preferences are equal, maybe prefer fuller?
        # Example: Prefer teacher whose group size is closer to capacity, but not over.
        new_size_diff = auditorium.capacity - new_teacher.group.num_students
        current_size_diff = auditorium.capacity - current_teacher.group.num_students
        # Prefer smaller positive difference (closer to capacity without exceeding)
        if new_size_diff >= 0 and current_size_diff >= 0:
            return new_size_diff < current_size_diff  # Smaller difference is better
        elif new_size_diff >= 0:  # Only new teacher fits perfectly or leaves less space
            return True
        elif current_size_diff >= 0:  # Only current teacher fits perfectly or leaves less space
            return False
        else:  # Neither fits perfectly, stick with current (or use another tie-breaker)
            return False
        # Simpler tie-breaker: keep the current teacher if preferences are equal
        # return False


# --- Gale-Shapley Algorithm Implementation ---

def gale_shapley_matching(
        teachers: Dict[str, Teacher],  # Use teacher full_name as key
        auditoriums: List[Auditorium]
) -> Tuple[Dict[str, Auditorium], Set[str]]:
    """
    Performs Gale-Shapley matching where teachers propose to auditoriums.

    Args:
        teachers: Dictionary of teachers (key: full_name, value: Teacher object).
        auditoriums: List of available Auditorium objects.

    Returns:
        A tuple containing:
        - teacher_matches: Dictionary mapping teacher full_name to their assigned Auditorium object.
        - unmatched_teachers: Set of full_names of teachers who couldn't be matched.
    """
    unmatched_teacher_names: List[str] = list(teachers.keys())

    teacher_matches: Dict[str, Auditorium] = {}
    auditorium_matches: Dict[Auditorium, str] = {aud: None for aud in
                                                 auditoriums}  # Stores current assignment A -> T_name

    proposal_attempts: Dict[str, Set[Auditorium]] = {name: set() for name in
                                                     teachers}  # Track proposals to avoid loops/redundancy

    while unmatched_teacher_names:
        teacher_name = unmatched_teacher_names.pop(0)  # Process one teacher at a time
        teacher = teachers[teacher_name]

        # --- Teacher ranks suitable auditoriums ---
        possible_auditoriums = []
        for aud in auditoriums:
            # Must fit, no schedule conflict, and teacher hasn't proposed here yet
            if (teacher.group.num_students <= aud.capacity and
                    not is_schedule_conflict(teacher, aud) and
                    aud not in proposal_attempts[teacher_name]):
                score = get_teacher_preference_score(teacher, aud)
                if score >= 0:  # Only consider valid matches (score >= 0)
                    possible_auditoriums.append((score, aud))

        # Sort potential auditoriums by teacher's preference (highest score first)
        possible_auditoriums.sort(key=lambda x: x[0], reverse=True)

        # --- Teacher proposes down their ranked list ---
        made_match = False
        for score, preferred_auditorium in possible_auditoriums:
            proposal_attempts[teacher_name].add(preferred_auditorium)  # Mark proposal attempt

            current_match_name = auditorium_matches.get(preferred_auditorium)

            if current_match_name is None:
                # Auditorium is free: Assign teacher
                teacher_matches[teacher_name] = preferred_auditorium
                auditorium_matches[preferred_auditorium] = teacher_name
                teacher.schedule.append(preferred_auditorium)  # Add to teacher's internal schedule
                made_match = True
                break  # Teacher is matched, move to next unmatched teacher

            else:
                # Auditorium is occupied: Check if auditorium prefers this new teacher
                current_matched_teacher = teachers[current_match_name]
                if is_teacher_better_match(teacher, preferred_auditorium, current_matched_teacher):
                    # New teacher is better: Replace old teacher
                    # Assign new teacher
                    teacher_matches[teacher_name] = preferred_auditorium
                    auditorium_matches[preferred_auditorium] = teacher_name
                    teacher.schedule.append(preferred_auditorium)

                    # Unassign old teacher
                    del teacher_matches[current_match_name]
                    current_matched_teacher.schedule.remove(preferred_auditorium)  # Remove from old teacher's schedule
                    unmatched_teacher_names.append(current_match_name)  # Old teacher becomes unmatched again

                    made_match = True
                    break  # Teacher is matched, move to next unmatched teacher
                # Else: Auditorium prefers current teacher, proposing teacher remains unmatched (for now) and tries next auditorium

        if not made_match and teacher_name not in teacher_matches:
            # If teacher went through all suitable options and wasn't matched, they remain technically unmatched
            # but already popped from list. We'll collect final unmatched set at the end.
            pass

    # Determine final set of unmatched teachers
    final_unmatched_teachers = {name for name in teachers if name not in teacher_matches}

    return teacher_matches, final_unmatched_teachers
