# Stable Scheduler: Teacher-Auditorium Matching (In Progress)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/) This project implements a scheduling system using a variation of the **Gale-Shapley stable matching algorithm**. It aims to find stable assignments between teachers and auditoriums based on their respective preferences and constraints. In this implementation, **teachers propose** to auditoriums.

## Core Concepts

The system models the following entities:

* **`Teacher`**: Represents a teacher with a specific `Group` they teach and a preferred time of day (`TimePeriod`).
* **`Group`**: Represents a class or group of students with a specific size, categorized into `SMALL`, `MEDIUM`, or `LARGE`.
* **`Auditorium`**: Represents a room with a specific `capacity`, also categorized by `SizeCategory`, available during a specific `TimeSlot` on a given `day`.
* **`TimeSlot`**: Defines a specific start and end time (e.g., 09:00-11:00) and determines the corresponding `TimePeriod`.
* **`TimePeriod`**: Broad time categories (`MORNING`, `MIDDAY`, `AFTERNOON`) used for teacher preferences.
* **`SizeCategory`**: Categories based on capacity or student numbers (`SMALL`, `MEDIUM`, `LARGE`).
* **`Preference`**: Enum used internally to rank matches (`HIGH`, `MEDIUM`, `LOW`).

## How it Works: The Matching Logic

The goal is to create a **stable matching**, meaning no teacher and auditorium would both prefer each other over their current assignment (or lack thereof).

1.  **Teacher Preferences (Ranking Auditoriums):**
    * Teachers evaluate potential auditoriums based on a combined score (`get_teacher_preference_score`).
    * **Primary Factor: Time Preference:** A strong preference is given if the auditorium's `TimeSlot` falls within the teacher's preferred `TimePeriod`.
        * Match with preferred `TimePeriod`: `time_score = 3` (High)
        * Adjacent periods (TODO: Currently not implemented, defaults to Low): `time_score = 1` (Medium)
        * Non-preferred periods: `time_score = 0` (Low)
    * **Secondary Factor: Group Size Fit:** How well the teacher's `Group` size fits the `Auditorium`'s `SizeCategory` (based on the *auditorium's* preference for that group size).
        * Auditorium prefers this group size highly: `size_score = 1.0`
        * Auditorium has medium preference: `size_score = 0.5`
        * Auditorium has low preference: `size_score = 0`
    * **Constraints:**
        * The teacher's `group.num_students` must be less than or equal to `auditorium.capacity`.
        * The proposed `auditorium.time_slot` must not conflict with the teacher's existing schedule (`is_schedule_conflict`).
    * Teachers rank valid auditoriums from highest total score (`time_score + size_score`) to lowest.

2.  **Auditorium Preferences (Evaluating Teachers):**
    * Auditoriums evaluate teachers proposing to them (`is_teacher_better_match`).
    * **Primary Factor: Size Category Match:** Auditoriums prefer teachers whose `Group` `SizeCategory` matches their own `SizeCategory` (`_calculate_preferences`). Preference levels (`HIGH` > `MEDIUM` > `LOW`) are assigned based on this match.
    * **Tie-Breaker: Occupancy Efficiency:** If two proposing teachers fall into the same preference category (e.g., both are `MEDIUM` preference), the auditorium prefers the teacher whose group size is *closer* to the auditorium's capacity without exceeding it. This minimizes wasted space and promotes fuller rooms.
    * **Constraint:** The proposing teacher's group must fit (`num_students <= capacity`).

3.  **Gale-Shapley Algorithm (`gale_shapley_matching`):**
    * Unmatched teachers propose sequentially to their highest-ranked available auditorium (that they haven't proposed to yet).
    * If the auditorium is free, it tentatively accepts the proposal.
    * If the auditorium is already assigned, it compares the new proposing teacher with the currently assigned teacher based on *its own* preferences (Size Category Match + Occupancy Tie-breaker).
        * If the new teacher is preferred, the old teacher becomes unassigned, and the new teacher is tentatively assigned.
        * Otherwise, the new teacher is rejected and must propose to their next preferred auditorium.
    * This continues until all teachers are either assigned or have exhausted all possible valid proposals.

## Output

The `gale_shapley_matching` function returns:

1.  `teacher_matches`: A dictionary mapping the full name of matched teachers to their assigned `Auditorium` object.
2.  `unmatched_teachers`: A set containing the full names of teachers who could not be assigned an auditorium.

## Backlog / Future Improvements

* **Auditorium Time Preferences:** Implement a way for auditoriums to specify preferred time slots or periods, influencing their acceptance criteria.
* **Teacher Adjacent Time Preference:** Implement logic where teachers might have a `MEDIUM` preference for time periods adjacent to their `HIGH` preference period.
* **Testing:** Conduct thorough testing with larger and more complex datasets to evaluate performance and stability.
* **Usage Examples:** Add clear examples in the README showing how to set up teachers, auditoriums, and run the matching process.
* **Configuration:** Allow easier configuration of scoring weights and preference logic.