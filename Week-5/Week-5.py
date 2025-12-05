# T1.py — Minimal pipeline (pandas, numpy, matplotlib only)

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

EXCEL_PATH = r"C:\Users\ADMIN\OneDrive\Desktop\DSBC\finance_economics_dataset.csv"
OUT_DIR = str(Path(EXCEL_PATH).parent)
USE_MONTHLY = False  # set True to also produce a monthly df

def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise SystemExit(f"Could not read CSV: {e}")
    date_col = next((c for c in df.columns if "date" in str(c).lower()), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(by=date_col).reset_index(drop=True)
        print("Time range:", df[date_col].min(), "->", df[date_col].max())
    print("Shape:", df.shape)
    print(df.dtypes)
    print(df.head(5))
    return df

def detect_key_variables(df: pd.DataFrame) -> dict:
    keys = {
        "GDP": ["gdp", "gdp growth", "gross domestic"],
        "Inflation": ["inflation", "cpi", "consumer price"],
        "Interest": ["interest", "rate", "fed", "treasury"],
        "Stock": ["stock", "index", "open", "close", "high", "low", "volume", "dow", "s&p", "nasdaq"],
        "Unemployment": ["unemployment"],
        "Retail/Spending": ["retail", "spending", "consumer"],
        "Commodities": ["oil", "gold", "crude"],
        "FX": ["forex", "usd", "eur", "jpy"],
    }
    out = {}
    for k, words in keys.items():
        cols = [c for c in df.columns if any(w in str(c).lower() for w in words)]
        if cols: out[k] = cols
    print("Detected variables:", out)
    return out

def missing_report(df: pd.DataFrame, out_dir: str) -> pd.DataFrame:
    miss = df.isna().sum().to_frame("MissingCount")
    miss["MissingPct"] = (miss["MissingCount"] / len(df) * 100).round(2)
    miss = miss.sort_values("MissingPct", ascending=False)
    miss.to_csv(os.path.join(out_dir, "missing_summary.csv"))
    plt.figure(figsize=(10, 4))
    miss["MissingPct"].plot(kind="bar")
    plt.ylabel("Missing (%)"); plt.title("Missingness by Column"); plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "missingness.png")); plt.close()
    print("Missing saved → missing_summary.csv, missingness.png")
    return miss

def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.infer_objects(copy=False)
    df = df.interpolate(method="linear")
    df = df.ffill().bfill()
    obj_cols = df.select_dtypes(include="object").columns
    for c in obj_cols:
        if df[c].isna().any():
            mode_vals = df[c].mode(dropna=True)
            if not mode_vals.empty:
                df[c] = df[c].fillna(mode_vals.iloc[0])
    print("Post-clean missing:", int(df.isna().sum().sum()))
    return df

def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    after = df.duplicated().sum()
    print(f"Duplicates: {before} → {after}")
    return df

def outlier_cap(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number])
    if num.empty:
        print("No numeric columns for outlier step."); return df
    Q1, Q3 = num.quantile(0.25), num.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    out_counts = ((num.lt(lower)) | (num.gt(upper))).sum().sort_values(ascending=False)
    print("Outliers (IQR) counts:\n", out_counts[out_counts > 0])
    capped = num.clip(lower=lower, upper=upper, axis=1)
    df[capped.columns] = capped
    print("Outliers capped.")
    return df

def boxplot_sample(df: pd.DataFrame, out_dir: str) -> None:
    cols_wanted = ['GDP Growth (%)','Inflation Rate (%)','Interest Rate (%)']
    cols = [c for c in cols_wanted if c in df.columns]
    if not cols: 
        print("Boxplot skipped (sample cols not found)."); return
    data = [df[c].dropna().values for c in cols]
    plt.figure(figsize=(12, 6))
    plt.boxplot(data, vert=False, labels=cols)
    plt.title("Boxplots after Outlier Capping (Sample Economic Indicators)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "boxplots_sample.png")); plt.close()
    print("Saved → boxplots_sample.png")

def anomaly_scan(df: pd.DataFrame, out_dir: str) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number])
    if num.empty:
        print("No numeric columns for anomaly step."); return pd.DataFrame()
    pct = num.pct_change()
    mu, sigma = pct.mean(), pct.std(ddof=0).replace(0, np.nan)
    z = (pct - mu) / sigma
    anomalies = (z.abs() > 4).sum().sort_values(ascending=False)
    out = anomalies[anomalies > 0].to_frame("AnomalyCount")
    out.to_csv(os.path.join(out_dir, "anomaly_summary.csv"))
    print("Anomalies saved → anomaly_summary.csv")
    return out

def corr_plot(df: pd.DataFrame, out_dir: str) -> None:
    num = df.select_dtypes(include=[np.number])
    if num.empty:
        print("No numeric columns for correlation plot."); return
    corr = num.corr(numeric_only=True)
    plt.figure(figsize=(8, 6))
    plt.imshow(corr, interpolation="nearest")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90, fontsize=7)
    plt.yticks(range(len(corr.columns)), corr.columns, fontsize=7)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "correlation_matrix.png")); plt.close()
    print("Saved → correlation_matrix.png")

def optional_resample(df: pd.DataFrame, use_monthly: bool):
    date_col = next((c for c in df.columns if "date" in str(c).lower()), None)
    if not use_monthly or not date_col: 
        return None
    out = (df.set_index(date_col)
             .resample("M").mean(numeric_only=True)
             .reset_index())
    print("Monthly shape:", out.shape)
    return out

def main():
    df = load_data(EXCEL_PATH)
    detect_key_variables(df)
    missing_report(df, OUT_DIR)
    df = clean_missing(df)
    df = handle_duplicates(df)
    df = outlier_cap(df)
    boxplot_sample(df, OUT_DIR)
    anomaly_scan(df, OUT_DIR)
    corr_plot(df, OUT_DIR)
    df_monthly = optional_resample(df, USE_MONTHLY)

    print("\nFinal info:")
    print(df.info())
    print(df.describe().T)

    print("\nArtifacts:")
    for f in ["missing_summary.csv","missingness.png","anomaly_summary.csv","correlation_matrix.png","boxplots_sample.png"]:
        p = os.path.join(OUT_DIR, f)
        if os.path.exists(p): print(p)

if __name__ == "__main__":
    main()
