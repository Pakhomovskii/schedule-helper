### Schedule helper (in progress)
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

#### Additional notes:
- Prioritizing Full Auditoriums: An auditorium will always try to accommodate a teacher if it has space, 
ensuring optimal usage of resources.
- 

#### Backlog:
- Time Preferences for Auditoriums: Implement a feature for auditoriums to specify preferred time slots.
- 
