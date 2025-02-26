import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
import time

# Download necessary NLTK resources
nltk.download('punkt_tb')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load your dataset
data = pd.read_csv("megaGymDataset.csv")

# Workout categories
workout_types = ['strength', 'plyometrics', 'cardio', 'stretching', 'powerlifting', 'strongman', 'olympic weightlifting']
body_parts = ['abdominals', 'adductors', 'abductors', 'biceps', 'calves', 'chest', 'forearms', 'glutes', 'hamstrings', 'lats', 'lower back', 'middle back', 'traps', 'neck', 'quadriceps', 'shoulders', 'triceps']
equipment_options = ['bands', 'barbell', 'kettlebells', 'dumbbell', 'machine', 'body only', 'medicine ball', 'exercise ball', 'foam roll', 'e-z curl bar']
levels = ['beginner', 'intermediate', 'expert']

# Clean the data
data.dropna(subset=['Title', 'Desc'], inplace=True)

# Text preprocessing
def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    return ' '.join(tokens)

# Intent vectorization
data['intent'] = data['Desc']
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['intent'])

# Reps interpretation
def interpret_reps(description):
    description = description.lower()
    if "low reps" in description:
        return "4-6 reps (strength-focused)"
    elif "moderate reps" in description:
        return "8-12 reps (general fitness)"
    elif "high reps" in description:
        return "15+ reps (endurance-focused)"
    elif re.search(r"\d+\s+reps?", description):
        return re.search(r"\d+\s+reps?", description).group()
    else:
        return "Reps not specified"

# Get workout routine
def get_workout_routine(user_input, selected_level):
    user_input_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    cosine_similarities = cosine_similarity(user_vector, X).flatten()
    
    top_match_index = cosine_similarities.argmax()
    best_match = data.iloc[top_match_index]
    
    workout_type, body_part, equipment, level = None, None, None, None
    
    for w_type in workout_types:
        if w_type in user_input_processed:
            workout_type = w_type.capitalize()
    
    for part in body_parts:
        if part in user_input_processed:
            body_part = part.capitalize()
    
    for equip in equipment_options:
        if equip in user_input_processed:
            equipment = equip.capitalize()
    
    if selected_level:
        level = selected_level.capitalize()
    
    filtered_data = data
    if workout_type:
        filtered_data = filtered_data[filtered_data['Type'].str.lower() == workout_type.lower()]
    if body_part:
        filtered_data = filtered_data[filtered_data['BodyPart'].str.lower() == body_part.lower()]
    if equipment:
        filtered_data = filtered_data[filtered_data['Equipment'].str.lower() == equipment.lower()]
    if level:
        filtered_data = filtered_data[filtered_data['Level'].str.lower() == level.lower()]

    if filtered_data.empty:
        return f"I understand your needs, here’s a workout suggestion for you:\n**{best_match['Title']}**: {best_match['Desc']}"
    
    routine = "\n\n".join([f"**{row['Title']}**\nReps: {interpret_reps(row['Desc'])}\n\nInstructions: {row['Desc']}" for _, row in filtered_data.iterrows()])
    
    return f"I understand your needs. Here's a personalized workout routine for you:\n\n{routine}"

# Timer with start and stop functionality
def start_timer():
    timer_placeholder = st.sidebar.empty()
    
    while st.session_state.time_left > 0:
        if st.session_state.stopped:
            timer_placeholder.success("Timer Stopped 🛑")
            return
        
        mins, secs = divmod(st.session_state.time_left, 60)
        timer_display = f"{mins:02}:{secs:02}"
        timer_placeholder.subheader(f"⏱ Time Left: {timer_display}")
        time.sleep(1)
        st.session_state.time_left -= 1

    timer_placeholder.success("⏰ Time's up! Well done!")

# Streamlit app layout
st.title("MentorFit💪")
st.write("Describe your workout preferences (e.g., 'beginner cardio for abs').")

# Sidebar for level and timer settings
selected_level = st.sidebar.selectbox("Select your fitness level:", options=levels)
timer_duration = st.sidebar.number_input("Set workout/rest timer (minutes):", min_value=0, max_value=60, value=5) * 60

# Timer control states
if 'time_left' not in st.session_state or st.session_state.stopped:
    st.session_state.time_left = timer_duration

if 'stopped' not in st.session_state:
    st.session_state.stopped = False

# Store workout result in session state
if 'workout_result' not in st.session_state:
    st.session_state.workout_result = ""

# Timer buttons side by side
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("✅ Start Timer"):
        st.session_state.stopped = False
        st.session_state.time_left = timer_duration
        start_timer()

with col2:
    if st.button("🛑 Stop Timer"):
        st.session_state.stopped = True
        st.session_state.time_left = 0

# Main workout routine section
user_input = st.text_input("Enter your workout preferences:")

if st.button("Get Workout Routine"):
    if user_input:
        st.session_state.workout_result = get_workout_routine(user_input, selected_level)

# Display the workout result even after rerun
if st.session_state.workout_result:
    st.write(st.session_state.workout_result)
