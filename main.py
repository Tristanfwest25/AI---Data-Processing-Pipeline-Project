"""
main.py — Module 2 Project entry point
Run this file to execute your pipeline.

Once you've implemented DataPipeline in pipeline.py, running:
    python main.py
should load, clean, analyze, visualize, and export the data — all without errors.
"""

import os
from pipeline import DataPipeline

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "messy_employee_survey.csv")


def main():
    print("=" * 60)
    print("Employee Survey Data Pipeline")
    print("=" * 60)

   
    pipeline = DataPipeline(DATA_PATH)
    results = pipeline.run()

    
    print("=" * 60)
    print("Summary of results:")
    print("=" * 60)

    print(f"  Top location by headcount: {results['headcount_by_location'].idxmax()}")
    print(f"  Average salary by department: {results['avg_salary_by_dept'].to_dict()}")
    print(f"  Experience-salary correlation: {results['experience_salary_correlation']}")
    print(f"  Average satisfaction by location: {results['avg_satisfaction_by_location'].to_dict()}")
    print(f"  Headcount by location: {results['headcount_by_location'].to_dict()}")
    print(f"  Average satisfaction by department: {results['avg_satisfaction_by_dept'].to_dict()}")


if __name__ == "__main__":
    main()