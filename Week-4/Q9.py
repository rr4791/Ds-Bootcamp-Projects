import pandas as pd

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    # Merge employee with department to get department names
    df = employee.merge(
        department,
        left_on="departmentId",
        right_on="id",
        how="left"
    )

    # Rank salaries within each department (dense rank handles duplicates correctly)
    df["salary_rank"] = (
        df.groupby("departmentId")["salary"]
        .rank(method="dense", ascending=False)
    )

    # Keep only top 3 salaries per department
    result = df[df["salary_rank"] <= 3]

    # Select and rename columns as required
    result = result[["name_y", "name_x", "salary"]]
    result.columns = ["Department", "Employee", "Salary"]

    return result
