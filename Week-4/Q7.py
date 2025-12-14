import pandas as pd

def gameplay_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    first_login = (
        activity.groupby("player_id", as_index=False)["event_date"]
        .min()
        .rename(columns={"event_date": "first_date"})
    )

    merged = activity.merge(first_login, on="player_id", how="left")

    next_day = pd.to_datetime(merged["first_date"]) + pd.Timedelta(days=1)
    logged_next_day = merged[pd.to_datetime(merged["event_date"]) == next_day]["player_id"].nunique()

    total_players = activity["player_id"].nunique()

    fraction = round(logged_next_day / total_players, 2)

    return pd.DataFrame({"fraction": [fraction]})
