import pandas as pd

def replace_employee_id(
    employees: pd.DataFrame,
    employee_uni: pd.DataFrame
) -> pd.DataFrame:
    
    result = pd.merge(
        employees,
        employee_uni,
        on="id",
        how="left"
    )

    return result[["unique_id", "name"]]
