"""
pipeline.py — Module 2 Project Starter
Your job: implement each method in the DataPipeline class below.
The docstrings describe exactly what each method should do.
"""

import pandas as pd
import csv
import os

class DataPipeline:
    """
    A data processing pipeline for employee survey data.

    Usage (once implemented):
        pipeline = DataPipeline("data/messy_employee_survey.csv")
        results = pipeline.run()
    """

    # Canonical spellings for normalization — use these dicts in your clean() method.
    DEPT_MAP = {
        "engineering": "Engineering",
        "eng":         "Engineering",
        "marketing":   "Marketing",
        "mktg":        "Marketing",
        "sales":       "Sales",
        "hr":          "HR",
        "human resources": "HR",
        "h.r.":        "HR",
        "finance":     "Finance",
        "fin":         "Finance",
    }

    LOC_MAP = {
        "new york":        "New York",
        "nyc":             "New York",
        "chicago":         "Chicago",
        "chi":             "Chicago",
        "austin":          "Austin",
        "austin, tx":      "Austin",
        "atx":             "Austin",
        "seattle":         "Seattle",
        "sea":             "Seattle",
        "remote":          "Remote",
        "work from home":  "Remote",
    }

    def __init__(self, filepath):
        """Load the CSV at `filepath` into self.df (a pandas DataFrame).
        Print how many rows and columns were loaded.

        Hint: use pd.read_csv()
        Wrap the load in try/except to catch FileNotFoundError.

        Args:
            filepath: path to the messy CSV file
        """
        
        try:
            self.df = pd.read_csv(filepath)  # load the CSV into a DataFrame
            print(f"Loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns.")  
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            self.df = pd.DataFrame()

        with pd.option_context(  # temporarily set display options for printing the DataFrame
            "display.max_columns", None,
            "display.width", 120,
            "display.float_format", "{:,.2f}".format,
        ):
            print("\n--- First 5 rows ---")
            print(self.df.head().to_string(index=False))

            print("\n--- Summary statistics ---")
            print(self.df.describe(include="all").to_string())

        print("\n--- Column details ---")
        self.df.info()
        print("\n--- Column data types ---")
        print(self.df.dtypes.to_string())
        
    def clean(self):
        """Clean the DataFrame stored in self.df and print a summary.

        Steps to implement (in order):
        1. Remove rows with duplicate employee_id (keep first occurrence).
           Hint: df.drop_duplicates(subset=["employee_id"], keep="first")

        2. Standardize 'name' — strip whitespace, title case.
           Hint: df["name"].str.strip().str.title()

        3. Normalize 'department' — map messy variants to canonical names.
           Hint: df["department"].str.strip().str.lower().map(self.DEPT_MAP)

        4. Normalize 'office_location' — same pattern as department.
           Hint: use self.LOC_MAP

        5. Convert 'salary' to float — strip "$" and "," first, set negatives to None.
           Hint: write a helper function and use df["salary"].apply(helper)
                 import re; re.sub(r"[$,]", "", str(val)) strips the symbols

        6. Convert 'years_experience' to numeric; set values > 50 to None (outliers).
           Hint: pd.to_numeric(..., errors="coerce")

        7. Convert 'satisfaction_score' to numeric; set values outside 1–10 to None.

        8. Parse 'survey_date' — multiple formats exist (MM/DD/YYYY, YYYY-MM-DD, DD-MM-YYYY).
           Hint: write a helper that tries pd.to_datetime(val, format=fmt) for each format.
                 Formats to try: "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"

        After all steps, reassign self.df = df and print a missing-values summary.

        Returns self so calls can be chained: pipeline.clean().analyze()
        """
        
        self.df = self.df.drop_duplicates(subset=["employee_id"], keep="first")
        self.df["name"] = self.df["name"].str.strip().str.title()
        self.df["department"] = self.df["department"].str.strip().str.lower().map(self.DEPT_MAP)  #normalize department names, looks up canonical names in DEPT_MAP
        self.df["office_location"] = self.df["office_location"].str.strip().str.lower().map(self.LOC_MAP)  #normalize office locations, looks up canonical names in LOC_MAP
        
        def clean_salary(val):
            import re
            val = re.sub(r"[$,]", "", str(val))
            val = float(val)
            if val < 0:
                val = None
            return val
        self.df["salary"] = self.df["salary"].apply(clean_salary)  # clean and normalize salary values
        
        self.df["years_experience"] = pd.to_numeric(self.df["years_experience"], errors="coerce")
        self.df.loc[self.df["years_experience"] > 50, "years_experience"] = None
        self.df["satisfaction_score"] = pd.to_numeric(self.df["satisfaction_score"], errors="coerce")
        self.df.loc[(self.df["satisfaction_score"] < 1) | (self.df["satisfaction_score"] > 10), "satisfaction_score"] = None
        
        def parse_survey_date(val):
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                try:
                    return pd.to_datetime(val, format=fmt)
                except (ValueError, TypeError):
                    continue
            return None
        self.df["survey_date"] = self.df["survey_date"].apply(parse_survey_date)  # parse survey dates with multiple formats
        
        print("--- Missing values summary ---")
        print(self.df.isna().sum())  # print the count of missing values for each column
        return self

    def analyze(self):
        """Compute summary statistics from the cleaned self.df.

        Compute and print:
        1. Average salary by department
           Hint: df.groupby("department")["salary"].mean().round(0)

        2. Average satisfaction score by department

        3. Headcount by office location
           Hint: df["office_location"].value_counts()

        4. Pearson correlation between years_experience and salary
           Hint: drop rows where either is NaN, then Series.corr()

        5. One additional insight of your choice (e.g., satisfaction by location)

        Return a dict with all results so main.py can use them.
        Keys to use: "avg_salary_by_dept", "avg_satisfaction_by_dept",
                     "headcount_by_location", "experience_salary_correlation",
                     "avg_satisfaction_by_location"
        """
        
        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)  
        
        avg_satisfaction_by_dept = self.df.groupby("department")["satisfaction_score"].mean().round(2)
        
        headcount_by_location = self.df["office_location"].value_counts()
        
        experience_salary_correlation = self.df[["years_experience", "salary"]].dropna().corr().loc["years_experience", "salary"]
        
        avg_satisfaction_by_location = self.df.groupby("office_location")["satisfaction_score"].mean().round(2)

        return {
            "avg_salary_by_dept": avg_salary_by_dept,
            "avg_satisfaction_by_dept": avg_satisfaction_by_dept,
            "headcount_by_location": headcount_by_location,
            "experience_salary_correlation": experience_salary_correlation,
            "avg_satisfaction_by_location": avg_satisfaction_by_location
        }

    def visualize(self, output_path="output/charts.png"):
        """Create and save visualizations to `output_path`.

        Required charts:
        - Bar chart: average salary by department
        - Histogram: satisfaction score distribution (bins 1–10)
        Bonus:
        - Horizontal bar: headcount by office location

        Use matplotlib with plt.subplots() for a multi-chart layout.
        Save with plt.savefig(output_path, dpi=120, bbox_inches="tight").
        Call plt.close() after saving.

        Hint: import matplotlib; matplotlib.use("Agg") at top of file
              prevents errors when no display is available.

        Args:
            output_path: where to save the PNG file
        """
       
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axes[1, 1].set_visible(False)
        # Bar chart: average salary by department
        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)
        axes[0, 0].bar(avg_salary_by_dept.index, avg_salary_by_dept.values, color=['red', 'blue', 'green', 'orange', 'purple'])
        axes[0, 0].set_title("Average Salary by Department")
        axes[0, 0].set_ylabel("Salary")

        # Histogram: satisfaction score distribution
        axes[0, 1].hist(self.df["satisfaction_score"].dropna(), bins=10, edgecolor="black")
        axes[0, 1].set_title("Satisfaction Score Distribution")
        axes[0, 1].set_xlabel("Satisfaction Score")
        axes[0, 1].set_ylabel("Frequency") 

        # Horizontal bar: headcount by office location
        headcount_by_location = self.df["office_location"].value_counts()
        axes[1, 0].barh(headcount_by_location.index, headcount_by_location.values, color='green')
        axes[1, 0].set_title("Headcount by Office Location")
        axes[1, 0].set_xlabel("Headcount")

        plt.tight_layout()
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close()

    def export(self, output_path="output/clean_employees.csv"):
        """Save the cleaned self.df to a CSV at `output_path`.

        Create the output directory if it doesn't exist.
        Wrap in try/except.

        Hint: df.to_csv(output_path, index=False)

        Args:
            output_path: path for the exported CSV
        """
        
        try:
            output_dir = os.path.dirname(output_path)  # get the directory part of the output path
            if output_dir:
                os.makedirs(output_dir, exist_ok=True) # create the output directory if it doesn't exist
            self.df.to_csv(output_path, index=False)  # save the cleaned DataFrame to CSV
        except (OSError, ValueError) as e:
            print(f"Error exporting CSV: {e}")

    def run(self):
        """Execute the full pipeline: clean → analyze → visualize → export.

        Build output paths using os.path.join(os.path.dirname(__file__), "output", ...).
        Return the results dict from analyze().
        """
        
        self.clean()
        results = self.analyze()
        output_dir = os.path.join(os.path.dirname(__file__), "output", "visualizations")
        os.makedirs(output_dir, exist_ok=True)
        self.visualize(os.path.join(output_dir, "visualization.png"))
        self.export(os.path.join(os.path.dirname(__file__), "output", "clean_employees.csv"))
        return results
