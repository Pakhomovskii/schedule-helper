### Schedule helper (in progress)
___
This application implements a variation of the Gale-Shapley algorithm to create stable schedules for teachers and
auditoriums. Teachers prioritize their preferred time slots, while auditoriums aim for optimal occupancy based on group 
sizes.

try it here [app](https://pakhomovskii-schedule-helper-main-ijejkw.streamlit.app/)

#### Explanation:
Stable Matching: This application finds a stable matching between teachers' preferences and auditoriums' availability 
and capacity constraints. Teacher Preferences: Teachers prioritize convenient time slots. Auditorium Preferences:
Auditoriums prefer being fully occupied and give preference to groups that match their capacity 
(small, medium, or large).
```python
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
```

the rest of preferences might be diffrent depends on univeriyt intresrest I made it like SizeCategory.SMALL:
Preference.LOW for medium and big auditorims becouse it is difficult for students to find a sit.
___

Lets look close to the code bellow:
```python
def get_teacher_preference_score(teacher, auditorium):
    # Prioritize time match, with some consideration for matching capacity size
    time_score = 3 if teacher.time_preference == auditorium.time_slot.start_time else 1
    size_score = 1 if teacher.group.size_category == auditorium.size_category else 0.5
    return time_score + size_score
```
If a teacher's time_preference aligns perfectly with an auditorium's time_slot, it assigns
a high score (time_score = 3). This indicates that time is a significant factor in determining a teacher's preference.

If a teacher's group.size_category matches the
auditorium.size_category, it assigns a moderate score (size_score = 1). 
Otherwise, it assigns a slightly lower score (size_score = 0.5)

The function adds the time_score and size_score to
give a final preference score. This combined score helps the algorithm rank 
auditoriums in order of desirability for each teacher.

___
#### Additional notes:
- Prioritizing Full Auditoriums: An auditorium will always try to accommodate a teacher if it has space, 
ensuring optimal usage of resources.
- 

#### Backlog:
- Time Preferences for Auditoriums: Implement a feature for auditoriums to specify preferred time slots.
- Needs test with a bigger data
- 
