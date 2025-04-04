# test_matching.py

import unittest
from datetime import time
from gale_shapley_matching import (
    TimeSlot, Auditorium, Group, Teacher, TimePeriod, SizeCategory, Preference,
    is_schedule_conflict, get_teacher_preference_score, is_teacher_better_match,
    gale_shapley_matching # Assuming overlap was defined or import if needed
)

# Dummy overlap function if not imported from original file
def overlap(ts1: TimeSlot, ts2: TimeSlot) -> bool:
    return ts1.start_time < ts2.end_time and ts2.start_time < ts1.end_time

class TestTimeSlot(unittest.TestCase):

    def test_period_calculation(self):
        self.assertEqual(TimeSlot(time(9, 0), time(10, 30)).period, TimePeriod.MORNING)
        self.assertEqual(TimeSlot(time(11, 59), time(13, 0)).period, TimePeriod.MORNING)
        self.assertEqual(TimeSlot(time(12, 0), time(13, 30)).period, TimePeriod.MIDDAY)
        self.assertEqual(TimeSlot(time(14, 59), time(16, 0)).period, TimePeriod.MIDDAY)
        self.assertEqual(TimeSlot(time(15, 0), time(16, 30)).period, TimePeriod.AFTERNOON)
        self.assertEqual(TimeSlot(time(17, 0), time(18, 0)).period, TimePeriod.AFTERNOON)

    def test_overlap(self):
        slot1 = TimeSlot(time(10, 0), time(11, 0))
        slot2 = TimeSlot(time(10, 30), time(11, 30)) # Overlaps
        slot3 = TimeSlot(time(11, 0), time(12, 0)) # Adjacent, no overlap
        slot4 = TimeSlot(time(9, 0), time(10, 0))  # Adjacent, no overlap
        slot5 = TimeSlot(time(9, 0), time(11, 0))  # Contains slot1

        self.assertTrue(slot1.overlaps(slot2))
        self.assertTrue(slot2.overlaps(slot1))
        self.assertFalse(slot1.overlaps(slot3))
        self.assertFalse(slot3.overlaps(slot1))
        self.assertFalse(slot1.overlaps(slot4))
        self.assertFalse(slot4.overlaps(slot1))
        self.assertTrue(slot1.overlaps(slot5))
        self.assertTrue(slot5.overlaps(slot1))

    def test_invalid_times(self):
         with self.assertRaises(ValueError):
             TimeSlot(time(11, 0), time(10, 0)) # End before start
         with self.assertRaises(TypeError):
             TimeSlot("10:00", "11:00") # Incorrect type


class TestGroupAndAuditorium(unittest.TestCase):

    def test_size_category(self):
        self.assertEqual(Group("G1", 5).size_category, SizeCategory.SMALL)
        self.assertEqual(Group("G2", 10).size_category, SizeCategory.SMALL)
        self.assertEqual(Group("G3", 11).size_category, SizeCategory.MEDIUM)
        self.assertEqual(Group("G4", 20).size_category, SizeCategory.MEDIUM)
        self.assertEqual(Group("G5", 21).size_category, SizeCategory.LARGE)
        self.assertEqual(Group("G6", 100).size_category, SizeCategory.LARGE)

        ts = TimeSlot(time(9,0), time(10,0))
        self.assertEqual(Auditorium("A1", 8, "Mon", ts).size_category, SizeCategory.SMALL)
        self.assertEqual(Auditorium("A2", 15, "Mon", ts).size_category, SizeCategory.MEDIUM)
        self.assertEqual(Auditorium("A3", 25, "Mon", ts).size_category, SizeCategory.LARGE)

    def test_auditorium_preferences(self):
        ts = TimeSlot(time(9,0), time(10,0))
        aud_small = Auditorium("AS", 8, "Mon", ts) # Small
        aud_medium = Auditorium("AM", 15, "Mon", ts) # Medium
        aud_large = Auditorium("AL", 25, "Mon", ts) # Large

        self.assertEqual(aud_small.preferences[SizeCategory.SMALL], Preference.HIGH)
        self.assertEqual(aud_small.preferences[SizeCategory.MEDIUM], Preference.LOW)

        self.assertEqual(aud_medium.preferences[SizeCategory.MEDIUM], Preference.HIGH)
        self.assertEqual(aud_medium.preferences[SizeCategory.SMALL], Preference.MEDIUM) # Example logic
        self.assertEqual(aud_medium.preferences[SizeCategory.LARGE], Preference.LOW)

        self.assertEqual(aud_large.preferences[SizeCategory.LARGE], Preference.HIGH)
        self.assertEqual(aud_large.preferences[SizeCategory.MEDIUM], Preference.MEDIUM) # Example logic


class TestTeacherHelpers(unittest.TestCase):

    def setUp(self):
        # Create reusable objects for tests
        self.g1 = Group("Group Small", 8)
        self.g2 = Group("Group Medium", 15)
        self.g3 = Group("Group Large", 25)

        self.t1 = Teacher("Teacher", "A", self.g1, TimePeriod.MORNING) # Prefers Morning, Small group
        self.t2 = Teacher("Teacher", "B", self.g2, TimePeriod.MIDDAY)  # Prefers Midday, Medium group
        self.t3 = Teacher("Teacher", "C", self.g3, TimePeriod.AFTERNOON) # Prefers Afternoon, Large group
        self.t4 = Teacher("Teacher", "D", self.g1, TimePeriod.MIDDAY) # Prefers Midday, Small group

        self.ts_morn = TimeSlot(time(9, 0), time(10, 30)) # Morning
        self.ts_mid = TimeSlot(time(12, 0), time(13, 30)) # Midday
        self.ts_aft = TimeSlot(time(15, 0), time(16, 30)) # Afternoon

        # Auditoriums with varying capacity and time
        self.aud_s_morn = Auditorium("Aud S Morn", 10, "Mon", self.ts_morn) # Small, Morning
        self.aud_m_mid = Auditorium("Aud M Mid", 20, "Mon", self.ts_mid)   # Medium, Midday
        self.aud_l_aft = Auditorium("Aud L Aft", 30, "Mon", self.ts_aft)   # Large, Afternoon
        self.aud_l_morn = Auditorium("Aud L Morn", 30, "Mon", self.ts_morn) # Large, Morning
        self.aud_s_mid = Auditorium("Aud S Mid", 10, "Mon", self.ts_mid) # Small, Midday

    def test_schedule_conflict(self):
        # Add aud_s_morn to t1's schedule
        self.t1.schedule.append(self.aud_s_morn)

        # Conflict: Same day, overlapping time
        aud_conflict = Auditorium("Conflict", 10, "Mon", TimeSlot(time(10, 0), time(11, 0)))
        self.assertTrue(is_schedule_conflict(self.t1, aud_conflict))

        # No Conflict: Same day, non-overlapping time
        aud_no_conflict_time = Auditorium("No Conflict Time", 10, "Mon", TimeSlot(time(11, 0), time(12, 0)))
        self.assertFalse(is_schedule_conflict(self.t1, aud_no_conflict_time))

        # No Conflict: Different day, same time
        aud_no_conflict_day = Auditorium("No Conflict Day", 10, "Tue", self.ts_morn)
        self.assertFalse(is_schedule_conflict(self.t1, aud_no_conflict_day))

        # No Conflict: Empty schedule
        self.assertFalse(is_schedule_conflict(self.t2, self.aud_m_mid))

    def test_teacher_preference_score(self):
         # t1 (Small, Prefers Morning) proposing to various auditoriums
         score_t1_aud_s_morn = get_teacher_preference_score(self.t1, self.aud_s_morn) # Perfect match: Time HIGH, Size HIGH
         score_t1_aud_l_morn = get_teacher_preference_score(self.t1, self.aud_l_morn) # Time HIGH, Size LOW
         score_t1_aud_s_mid = get_teacher_preference_score(self.t1, self.aud_s_mid)   # Time LOW, Size HIGH
         score_t1_aud_m_mid = get_teacher_preference_score(self.t1, self.aud_m_mid)   # Time LOW, Size MEDIUM (Aud pref for Small)

         self.assertGreater(score_t1_aud_s_morn, score_t1_aud_l_morn) # Prefers correct size if time matches
         self.assertGreater(score_t1_aud_s_morn, score_t1_aud_s_mid)   # Prefers correct time if size matches
         self.assertGreater(score_t1_aud_l_morn, score_t1_aud_s_mid) # Time match more important than size match here

         # Test capacity limit
         aud_too_small = Auditorium("Too Small", 5, "Mon", self.ts_morn)
         score_t2_aud_too_small = get_teacher_preference_score(self.t2, aud_too_small) # t2 group size 15 > 5 capacity
         self.assertEqual(score_t2_aud_too_small, -1.0) # Should return -1 if doesn't fit

    def test_is_teacher_better_match(self):
         # Scenario: aud_m_mid (Medium Cap 20) is currently held by t4 (Small Group 8, Pref Midday)
         # Should t2 (Medium Group 15, Pref Midday) replace t4?

         # Auditorium Preference: Medium Aud prefers Medium Group (HIGH) over Small Group (MEDIUM)
         self.assertTrue(is_teacher_better_match(self.t2, self.aud_m_mid, self.t4))

         # Scenario: aud_l_morn (Large Cap 30) held by t1 (Small Group 8, Pref Morning)
         # Should t3 (Large Group 25, Pref Afternoon) replace t1?
         # Auditorium Preference: Large Aud prefers Large Group (HIGH) over Small Group (LOW)
         self.assertTrue(is_teacher_better_match(self.t3, self.aud_l_morn, self.t1))

         # Scenario: aud_m_mid (Medium Cap 20) held by t2 (Medium Group 15, Pref Midday)
         # Should t4 (Small Group 8, Pref Midday) replace t2?
         # Auditorium Preference: Medium Aud prefers Medium Group (HIGH) over Small Group (MEDIUM)
         self.assertFalse(is_teacher_better_match(self.t4, self.aud_m_mid, self.t2))

         # Test capacity limit for replacement
         # aud_s_morn (Small Cap 10) held by t1 (Small Group 8)
         # Should t2 (Medium Group 15) replace t1? -> No, t2 doesn't fit
         self.assertFalse(is_teacher_better_match(self.t2, self.aud_s_morn, self.t1))


class TestGaleShapleyMatching(unittest.TestCase):

    def test_simple_match(self):
        # One teacher, one suitable auditorium
        g = Group("Simple Group", 5)
        t = Teacher("Simple", "Teacher", g, TimePeriod.MORNING)
        ts = TimeSlot(time(9,0), time(10,0))
        a = Auditorium("Simple Aud", 10, "Mon", ts)

        matches, unmatched = gale_shapley_matching({"Simple Teacher": t}, [a])
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(unmatched), 0)
        self.assertEqual(matches["Simple Teacher"], a)
        self.assertEqual(t.schedule, [a]) # Check internal schedule update

    def test_no_match_capacity(self):
        # Teacher group too large for auditorium
        g = Group("Big Group", 20)
        t = Teacher("Big", "Teacher", g, TimePeriod.MORNING)
        ts = TimeSlot(time(9,0), time(10,0))
        a = Auditorium("Small Aud", 10, "Mon", ts) # Capacity too small

        matches, unmatched = gale_shapley_matching({"Big Teacher": t}, [a])
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(unmatched), 1)
        self.assertIn("Big Teacher", unmatched)
        self.assertEqual(t.schedule, [])

    def test_no_match_conflict(self):
        # Teacher has schedule conflict
        g = Group("Busy Group", 5)
        t = Teacher("Busy", "Teacher", g, TimePeriod.MORNING)
        ts1 = TimeSlot(time(9,0), time(10,0))
        ts2 = TimeSlot(time(9,30), time(10,30)) # Overlapping time
        a1 = Auditorium("Aud 1", 10, "Mon", ts1)
        a2 = Auditorium("Aud 2", 10, "Mon", ts2) # Conflict with a1 if assigned

        t.schedule.append(a1) # Pre-assign a1

        matches, unmatched = gale_shapley_matching({"Busy Teacher": t}, [a1, a2]) # Try matching t to a2
        # Since t already has a1 scheduled, it cannot be matched to a2 due to conflict
        # The algorithm should see the conflict and not match t to a2.
        # If t was already matched to a1 outside the run, the result depends on how pre-scheduled items are handled.
        # Assuming we run with t *initially* unmatched but having a schedule:
        t.schedule = [a1] # Reset schedule for test clarity
        matches, unmatched = gale_shapley_matching({"Busy Teacher": t}, [a2])
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(unmatched), 1)
        self.assertIn("Busy Teacher", unmatched)


    def test_preference_order_and_replacement(self):
        # Setup requires careful preference definition leading to replacement
        g_small = Group("Small", 8)
        g_medium = Group("Medium", 15)

        # Teacher A prefers Morning, Small group
        t_a = Teacher("Teacher", "A", g_small, TimePeriod.MORNING)
        # Teacher B prefers Morning, Medium group
        t_b = Teacher("Teacher", "B", g_medium, TimePeriod.MORNING)

        # Aud M is Medium capacity (20), Morning. Prefers Medium groups over Small.
        aud_m = Auditorium("Aud M", 20, "Mon", TimeSlot(time(9, 0), time(10, 0)))
        # Aud S is Small capacity (10), Morning. Prefers Small groups.
        aud_s = Auditorium("Aud S", 10, "Mon", TimeSlot(time(10, 0), time(11, 0)))

        teachers = {"Teacher A": t_a, "Teacher B": t_b}
        auditoriums = [aud_m, aud_s]

        t_a = Teacher("Replace", "A", g_small, TimePeriod.MORNING)
        t_b = Teacher("Replace", "B", g_medium, TimePeriod.MORNING)
        aud_m = Auditorium("Replace Aud M", 20, "Mon", TimeSlot(time(9, 0), time(10, 0)))
        aud_s = Auditorium("Replace Aud S", 10, "Mon", TimeSlot(time(10, 0), time(11, 0))) # Added for A to potentially match later

        teachers_replace = {"Replace A": t_a, "Replace B": t_b}
        auditoriums_replace = [aud_m, aud_s] # Order might influence proposal order if scores are equal

        matches, unmatched = gale_shapley_matching(teachers_replace, auditoriums_replace)

        self.assertEqual(len(matches), 2)
        self.assertEqual(len(unmatched), 0)
        self.assertEqual(matches["Replace B"], aud_m) # B should end up in Aud M
        self.assertEqual(matches["Replace A"], aud_s) # A should end up in Aud S
        self.assertIn(aud_m, t_b.schedule)
        self.assertIn(aud_s, t_a.schedule)
        self.assertNotIn(aud_m, t_a.schedule) # Ensure A was removed from Aud M's schedule


if __name__ == "__main__":
    unittest.main()