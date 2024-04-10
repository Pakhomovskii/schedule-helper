# Schedule helper (in progress)
The variation of Gale-Shapley algorithm to create stable schedule for teachers

try it here [app](https://pakhomovskii-schedule-helper-main-ijejkw.streamlit.app/)

#### Explanation

THe main idea to find stable matching between preferences teachers and avaliable auditoriums that also have there own preferdnces
For teachers the main goal to find best time whereas for Universite and its auditoriums it is important to privide optimal upload for auditorium 
that is why we have SizeCategory.SMALL for capacity <= 10 and SizeCategory.MEDIUM will be high if the group between 10 and 20 

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

the rest of preferences might be diffrent depends on univeriyt intresrest I made it  like SizeCategory.SMALL: Preference.LOW
for medium and big  auditorims becouse it is difficult for students to find a sit.

#### Additional notes
- An auditorium ALWAYS prefers being full if possible
- 

#### Backlog
- Add time choose for auditoriums, so teachers can pick time for auditorium
- 
