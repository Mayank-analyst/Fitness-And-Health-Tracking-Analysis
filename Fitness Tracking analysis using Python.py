#IMPORTING DATASET 

import pandas as pd

df = pd.read_csv("C:\\Users\\Mayank Bisht\\Documents\\Data analyst Projects\\Fitness and Health tracking Analysis(EDA)\\fitness_messy_dataset.csv")

# CHECKING THE DATASET

print(df.head())

print(df.shape)



# INSPECTING THE DATASET

print(df.info())

print(df.isnull().sum())



# CLEANING THE DATASET 

 #1. Fixing column names

df.columns = df.columns.str.lower().str.strip() 

#2. Fixing data types

df['user_id'] = df['user_id'].astype('Int64')   
df['date'] = pd.to_datetime(df['date'], errors='coerce') 

#3. Filling missing values with median/mean for numerical columns

# Median for stable metrics
median_cols = ['age', 'steps', 'height_cm', 'weight_kg', 'sleep_hours', 'heart_rate']

for col in median_cols:
    df[col] = df[col].fillna(df[col].median())

# Mean for continuous metrics
mean_cols = ['calories_burned', 'water_intake_liters', 'workout_duration_minutes']

for col in mean_cols:
    df[col] = df[col].fillna(df[col].mean())

# Fixing categorical inconsistent values in Gender column
  
df['gender'] = df['gender'].str.strip().str.lower()

df['gender'] = df['gender'].map({
    'f': 'Female',
    'female': 'Female',
    'male': 'Male'
}).fillna('Unknown')

#4. Filling missing values for categorical columns with Unknown

df = df.dropna(subset=['user_id'])

df['gender'] = df['gender'].fillna('Unknown')
df['workout_type'] = df['workout_type'].fillna('Unknown')
df['date'] = df['date'].fillna(method='ffill')



# EXPLORATORY DATA ANALYSIS (EDA)


#1. KPIs

print("Total Users:", df['user_id'].nunique())
print("Total Workouts:", len(df))
print("Avg Steps:", df['steps'].mean())
print("Avg Calories:", df['calories_burned'].mean())
print("Avg Sleep:", df['sleep_hours'].mean())
print("Avg Water Intake:", df['water_intake_liters'].mean())

#2. Workout Analysis

workout_analysis = df.groupby('workout_type')['calories_burned'].mean().sort_values(ascending=False)
print("\nAverage Calories Burned by Workout Type:\n", workout_analysis)

#3. Sleep vs Activity

df['activity_level'] = pd.cut(df['steps'], bins=[0, 5000, 10000, float('inf')], labels=['Low', 'Medium', 'High'])
print("\nAverage Sleep Hours by Activity Level:\n", df.groupby('activity_level')['sleep_hours'].mean())

#4. Hourly Activity

hourly_activity = df.groupby(df['date'].dt.hour)['steps'].mean()
print("\nAverage Steps by Hour of Day:\n", hourly_activity)

#5. Daily Trend

daily_trend = df.groupby(df['date'].dt.date)['steps'].mean()
print("\nAverage Steps by Date:\n", daily_trend)

#6. Correlation Analysis

correlation = df[['steps', 'calories_burned', 'sleep_hours', 'water_intake_liters', 'heart_rate']].corr()
print("\nCorrelation Matrix:\n", correlation)                                                                                            

#7. Top Users

top_users = df.groupby('user_id')[['steps', 'calories_burned']].sum().sort_values(by='calories_burned', ascending=False).head()
print("\nTop Users by Calories Burned:\n", top_users)


# EXPORTING CLEAN DATA AS CSV

df.to_csv("C:\\Users\\Mayank Bisht\\Documents\\Data analyst Projects\\Fitness and Health tracking Analysis(EDA)\\fitness_cleaned_dataset.csv", index=False)
