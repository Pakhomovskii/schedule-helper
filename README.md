### Schedule helper (in progress)
___
This simple project implements a variation of the [Gale-Shapley algorithm](https://en.wikipedia.org/wiki/Gale–Shapley_algorithm) to create stable schedules for teachers and
auditoriums. Teachers prioritize their preferred time slots, while auditoriums aim for optimal occupancy based on group 
sizes.

#### Explanation:
- Stable Matching: This application finds a stable matching between teachers' preferences and auditoriums' availability 
and capacity constraints. 
Teacher Preferences: Teachers prioritize convenient time slots. 
- Auditorium Preferences:
- Auditoriums prefer being fully occupied and give preference to groups that match their capacity 
(small, medium, or large).

If a teacher's time_preference aligns perfectly with an auditorium's time_slot, it assigns
a high score (time_score = 3). This indicates that time is a significant factor in determining a teacher's preference.

If a teacher's group.size_category matches the
auditorium.size_category, it assigns a moderate score (size_score = 1). 
Otherwise, it assigns a slightly lower score (size_score = 0.5)

The function adds the time_score and size_score to
give a final preference score. This combined score helps the algorithm rank 
auditoriums in order of desirability for each teacher.

#### Additional notes:
- Prioritizing Full Auditoriums: An auditorium will always try to accommodate a teacher if it has space, 
ensuring optimal usage of resources.

#### Backlog:
- Time Preferences for Auditoriums: Implement a feature for auditoriums to specify preferred time slots.
- Needs test with a bigger data
