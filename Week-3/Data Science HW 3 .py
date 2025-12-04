#1. Filter the data to include only weekdays (Monday to Friday) and plot a line graph showing the pedestrian counts for each day of the week.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path="/Users/margaramolina/Documents/Python/Data Science/Brooklyn_Bridge_Automated_Pedestrian_Counts_Demonstration_Project_20251014.csv"

#Read and load data
df=pd.read_csv(file_path)

#Make time readable
df["hour_beginning"]=pd.to_datetime(df["hour_beginning"])

#Convert commas to numbers in pedestrian column 
df["Pedestrians"]=df["Pedestrians"].astype(str)
df["Pedestrians"]=df["Pedestrians"].str.replace(',', '')
df["Pedestrians"]=df["Pedestrians"].astype(float)

#Get day and name
df["day_of_week"]=df["hour_beginning"].dt.dayofweek
df["day_name"]=df["hour_beginning"].dt.day_name()

#Take only weekdays 
weekday=df[df["day_of_week"]<5]

#Get totals by day
daily_totals=weekday.groupby("hour_beginning").agg({"Pedestrians":"sum","day_name":"first"}).reset_index()

#Plot
    #Go over each weekday, get data for each and graph
plt.figure(figsize=(12, 6))
for day in ["Monday","Tuesday","Wednesday","Thursday","Friday"]:
    day_data=daily_totals[daily_totals["day_name"] == day]
    plt.plot(day_data["hour_beginning"],day_data["Pedestrians"],label=day,alpha=0.7)

plt.legend()
plt.title("Pedestrian Count")
plt.xlabel("Date")
plt.ylabel("Total Pedestrian Count")
plt.grid(True, alpha=0.3)

#2. Track pedestrian counts on the Brooklyn Bridge for the year 2019 and analyze how different weather conditions influence pedestrian activity in that year. Sort the pedestrian count data by weather summary to identify any correlations( with a correlation matrix) between weather patterns and pedestrian counts for the selected year.
#Get only 2019 data
year=df[df["hour_beginning"].dt.year==2019].copy()

#Sort pedestrians by weather 
weather=year.groupby("weather_summary")["Pedestrians"].mean().sort_values(ascending=True)

#Check weather options and convert to numbers 
options=year["weather_summary"].unique()
weather_to_numbers={weather: x+1 for x, weather in enumerate(options)}
year["weather_numeric"]=year["weather_summary"].map(weather_to_numbers)

#Correlation matrix
correlation_matrix=year[["Pedestrians", "temperature", "precipitation"]].corr()

#Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Pedestrians vs. Weather")

#3. Implement a custom function to categorize time of day into morning, afternoon, evening, and night, and create a new column in the DataFrame to store these categories. Use this new column to analyze pedestrian activity patterns throughout the day.
#Fucntion to divide the day 
def time_during_day(hour):
    if 6<=hour<=12:
        return "Morning"
    if 12<hour<=16:
        return "Afternoon"
    if 16<hour<=20:
        return "Evening"
    else:
        return "Night"
    
#Create a new column 
df["day_classification"]=df["hour_beginning"].dt.hour.apply(time_during_day)


time=df.groupby("day_classification")["Pedestrians"].mean()
print("Average Pedestrian Counts by Time of Day:")
print(time)

# Optional: Plot the results
plt.figure(figsize=(10, 6))
time.plot(kind="bar")
plt.title("Average Pedestrian Activity by Time of Day")
plt.ylabel("Average Pedestrian Count")
plt.show()




    

