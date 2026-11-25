# Employee Survey Data Pipeline

A Python project that cleans and analyzes employee survey data. It standardizes
department and office names, parses salary and date values, marks invalid or
out-of-range values as missing, calculates summary statistics, and creates
visualizations.

## Clone the project

In Git Bash, replace `OWNER` and `REPOSITORY` with the GitHub account and
repository name:

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
```

## Set up and run

From the project folder, create and activate a virtual environment, then install
the dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python main.py
```

The script reads `Data/messy_employee_survey.csv`, prints data and analysis
summaries, and writes:

- `output/clean_employees.csv` — the cleaned survey data
- `output/visualizations/visualization.png` — salary, satisfaction, and
  headcount charts

## What it analyzes

- Average salary by department
- Average satisfaction by department and office location
- Headcount by office location
- Correlation between years of experience and salary