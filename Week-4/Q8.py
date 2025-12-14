import pandas as pd

def project_employees_i(project: pd.DataFrame, employee: pd.DataFrame) -> pd.DataFrame:
    merged = project.merge(employee, on="employee_id", how="inner")
    out = (
        merged.groupby("project_id", as_index=False)["experience_years"]
        .mean()
        .rename(columns={"experience_years": "average_years"})
    )
    out["average_years"] = out["average_years"].round(2)
    return out
