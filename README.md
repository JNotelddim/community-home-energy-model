# Community Home Energy Model Kit

This repository is a quick-and-dirty project built over the course of a few days
as part of the inaugural run of the [Software Stacks in Climate Tech](https://terra.do/climate-education/cohort-courses/software-stacks-in-climate-tech/)
Course by Terra.do .

## Contributors

[Amy Yang](https://github.com/mongolianprincess) and [Nick Keenan](https://github.com/nickkeenan) welcomed me (Jared McKimm) into their project for the course.

### Instructors & Underlying Course Content
Please note that the underlying code for home energy modeling is mostly from the hex notebook set up by
[Jaime Curtis](https://github.com/jaimemarijke) and [Jason Curtis](https://github.com/jason-curtis).

## Concept
The concept here is a sort of a:
"Climate lunchbox toolkit for Residential communities to identify potential improvements they can enact."

## How it works:

1. Energy modeling
  - Pulls from course assignment on home energy modeling,
  - Expands the modeling to a "neighborhood" scale, modeling given home characteristics, then optimizing some features, then remodeling.
  - Then outputs comparisons: potential energy consumption reduction, cost savings, carbon emissions reductions, etc.
3. Incentives gathering
  - Set up by Nick
  - Aggregates federal, state/provincial, municipal incentives based on household income and family size.

# Running the script:

Install reqs:
```
python3 -m pip install -r requirements.txt
```

Run the thing:
```
python3 src/main.py
```
