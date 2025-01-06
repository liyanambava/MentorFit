import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

data = pd.read_csv(r"C:\Users\LIYANA\OneDrive\Documents\VIT\SEMESTERS\7\SLP\megaGymDataset.csv")

workout_types = ['strength', 'plyometrics', 'cardio', 'stretching', 'powerlifting', 'strongman', 'olympic weightlifting']
body_parts = ['abdominals', 'adductors', 'abductors', 'biceps', 'calves', 'chest', 'forearms', 'glutes', 'hamstrings', 'lats', 'lower back', 'middle back', 'traps', 'neck', 'quadriceps', 'shoulders', 'triceps']
equipment_options = ['bands', 'barbell', 'kettlebells', 'dumbbell', 'machine', 'body only', 'medicine ball', 'exercise ball', 'foam roll', 'e-z curl bar']
levels = ['beginner', 'intermediate', 'expert']

data.dropna(subset=['Title', 'Desc'], inplace=True)

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    return ' '.join(tokens)

data['intent'] = data['Desc']
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['intent'])

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
        filtered_data = filtered_data[filtered_data['Type'] == workout_type]
    if body_part:
        filtered_data = filtered_data[filtered_data['BodyPart'] == body_part]
    if equipment:
        filtered_data = filtered_data[filtered_data['Equipment'] == equipment]
    if level:
        filtered_data = filtered_data[filtered_data['Level'] == level]

    if filtered_data.empty:
        return f"I understand your needs, here’s a workout suggestion for you:\n{best_match['Title']}: {best_match['Desc']}"
    
    routine = "\n\n".join([f"**{row['Title']}**\nReps: {interpret_reps(row['Desc'])}\n\nInstructions: {row['Desc']}" for _, row in filtered_data.iterrows()])
    
    return f"I understand your needs. Here's a personalized workout routine for you:\n\n{routine}"

st.title("MentorFit💪")
st.write("Describe your workout preferences (e.g., 'beginner cardio for abs').")

selected_level = st.sidebar.selectbox("Select your fitness level:", options=levels)

user_input = st.text_input("Enter your workout preferences:")

if st.button("Get Workout Routine"):
    if user_input:
        response = get_workout_routine(user_input, selected_level)
        st.write(response)
    else:
        st.write("Please enter your workout preferences.")
