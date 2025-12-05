import pandas as pd
import numpy as np

print("Loading data...")
# 1. Load & prepare daily series
df = pd.read_csv("finance_economics_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])
sp = df[df["Stock Index"] == "S&P 500"].sort_values("Date")
sp["Close_SP500"] = sp["Close Price"]
sp["Return_SP500"] = sp["Close_SP500"].pct_change()

macro = df.groupby("Date").agg({
    "GDP Growth (%)": "mean",
    "Interest Rate (%)": "mean"
}).rename(columns={"GDP Growth (%)": "GDP_Growth",
                   "Interest Rate (%)": "Interest_Rate"})

daily = sp.set_index("Date").join(macro, how="left")[[
    "Close_SP500", "Return_SP500", "GDP_Growth", "Interest_Rate"
]].dropna()

print(f"✓ Data loaded successfully!")
print(f"  Daily data shape: {daily.shape}")
print(f"  Date range: {daily.index.min()} to {daily.index.max()}")

# 2. Calculate statistics
print("\n--- Data Summary ---")
print(f"Close SP500 - Mean: {daily['Close_SP500'].mean():.2f}, Std: {daily['Close_SP500'].std():.2f}")
print(f"Return SP500 - Mean: {daily['Return_SP500'].mean():.4f}, Std: {daily['Return_SP500'].std():.4f}")
print(f"GDP Growth - Mean: {daily['GDP_Growth'].mean():.2f}%")
print(f"Interest Rate - Mean: {daily['Interest_Rate'].mean():.2f}%")

# 3. Correlation analysis
print("\n--- Correlation Matrix ---")
corr = daily[["Close_SP500", "Return_SP500", "GDP_Growth", "Interest_Rate"]].corr()
print(corr)

# 4. Manual Linear Regression (without sklearn)
print("\n--- Linear Regression Forecast ---")

# Create lagged features
feature_cols = ["Close_SP500", "Return_SP500", "GDP_Growth", "Interest_Rate"]
X = daily[feature_cols].values
y = daily["Close_SP500"].values

# Simple scaling manually
X_mean = X.mean(axis=0)
X_std = X.std(axis=0) + 1e-8
X_scaled = (X - X_mean) / X_std

# Create sequences
window = 30
X_seq, y_seq = [], []
for i in range(len(X_scaled) - window):
    X_seq.append(X_scaled[i:i+window].flatten())
    y_seq.append(y[i+window])
X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

# Train-test split
split = int(len(X_seq) * 0.8)
X_train, X_test = X_seq[:split], X_seq[split:]
y_train, y_test = y_seq[:split], y_seq[split:]

# Simple linear regression using normal equations
X_train_with_bias = np.column_stack([np.ones(len(X_train)), X_train])
try:
    beta = np.linalg.lstsq(X_train_with_bias, y_train, rcond=None)[0]
    y_pred = np.dot(np.column_stack([np.ones(len(X_test)), X_test]), beta)
    
    # Calculate metrics
    mae = np.mean(np.abs(y_test - y_pred))
    rmse = np.sqrt(np.mean((y_test - y_pred)**2))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"Linear Regression Results:")
    print(f"  Training set size: {len(X_train)}")
    print(f"  Test set size: {len(X_test)}")
    print(f"  MAE: {mae:.3f}")
    print(f"  RMSE: {rmse:.3f}")
    print(f"  MAPE: {mape:.2f}%")
except Exception as e:
    print(f"  Error: {e}")

# 5. ARIMA-like forecast (simple exponential smoothing)
print("\n--- Simple Exponential Smoothing Forecast ---")
series = daily["Close_SP500"].values
split = int(len(series) * 0.8)
train, test = series[:split], series[split:]

# Simple exponential smoothing
alpha = 0.3
forecast = []
last_value = train[0]
for val in train:
    last_value = alpha * val + (1 - alpha) * last_value
forecast_val = last_value
for _ in test:
    forecast.append(forecast_val)
forecast = np.array(forecast)

ses_mae = np.mean(np.abs(test - forecast))
ses_rmse = np.sqrt(np.mean((test - forecast)**2))
print(f"Simple Exponential Smoothing Results:")
print(f"  MAE: {ses_mae:.3f}")
print(f"  RMSE: {ses_rmse:.3f}")

# 6. Monthly aggregation
print("\n--- Monthly Data Summary ---")
monthly = daily[["Close_SP500", "GDP_Growth", "Interest_Rate"]]\
    .resample("ME").agg({"Close_SP500":"last",
                        "GDP_Growth":"mean",
                        "Interest_Rate":"mean"})
print(f"Monthly data shape: {monthly.shape}")
if len(monthly) > 0:
    print(f"Monthly Close SP500 - Min: {monthly['Close_SP500'].min():.2f}, Max: {monthly['Close_SP500'].max():.2f}")

print("\n✓ All code executed successfully!")
