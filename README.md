# MentorFit
# MentorFit 💪  
Your Personal Workout Companion — Get Personalized Routines & Track Time with an In-App Timer!

![MentorFit](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red)

---

## 🏋️‍♀️ **Project Overview**  
**MentorFit** is a workout recommendation app built with **Python** and **Streamlit**.  
It personalizes fitness routines based on your preferences and includes a real-time timer for guided workouts — all in a single interface!  

✨ **Features:**  
- **Personalized Workout Recommendations:** Get routines tailored to your fitness level, body part, equipment, and goals.  
- **Smart Repetition Detection:** Understands workout descriptions to suggest rep counts (strength, endurance, etc.).  
- **Built-In Timer:** Set a timer for your workouts or rests — with start and stop buttons!  
- **Simultaneous Functionality:** The chatbot and timer work independently, so you can run a timer while exploring workouts.  

---

## 📸 **App Preview**  
| **Workout Routine** | **Timer Countdown** |
|---------------------|---------------------|
| ![Workout](https://via.placeholder.com/400x300?text=Workout+Routine) | ![Timer](https://via.placeholder.com/400x300?text=Timer+Countdown) |

---

## ⚡ **Tech Stack**  
- **Frontend & UI:** Streamlit  
- **Backend Logic:** Python  
- **Data Processing:** Pandas, NumPy  
- **Text Analysis:** NLTK (Natural Language Toolkit)  
- **Similarity Search:** Scikit-learn (TF-IDF + Cosine Similarity)  

---

## 🛠️ **Installation & Setup**  
1. **Clone the repository:**  
```bash```
git clone https://github.com/liyanambava/MentorFit.git
cd MentorFit
2. Create a virtual environment:
python -m venv env
source env/bin/activate  # On Mac/Linux
env\Scripts\activate     # On Windows
3. Install dependencies:
pip install -r requirements.txt
4. Download NLTK resources:
import nltk
nltk.download('punkt')
nltk.download('stopwords')
5. Add your dataset:
Place your megaGymDataset.csv file in the project folder.

6. Run the Streamlit app:
streamlit run main.py
