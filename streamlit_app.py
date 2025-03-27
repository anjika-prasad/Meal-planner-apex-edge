import streamlit as st
from PIL import Image
import os
import random
import requests

def generate_meal_plan():
    sample_meals = {
        "Breakfast": ["Oatmeal with berries", "Scrambled eggs with avocado", "Greek yogurt with honey & nuts"],
        "Lunch": ["Grilled chicken salad", "Quinoa & veggie bowl", "Lentil soup with whole grain bread"],
        "Dinner": ["Salmon with steamed vegetables", "Tofu stir-fry with brown rice", "Chickpea curry with roti"]
    }
    return {meal: random.choice(foods) for meal, foods in sample_meals.items()}

def get_grocery_recommendations(meal_plan):
    api_url = "https://api.spoonacular.com/food/ingredients/search"
    api_key = "AIzaSyDm8zX6aS9pOwX8FTxdfK6Nf_Q9aqnoPcA"  # Replace with your actual API key
    grocery_list = {}
    
    for meal, food in meal_plan.items():
        params = {"query": food, "apiKey": api_key}
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                grocery_list[meal] = [item["name"] for item in data["results"]]
            else:
                grocery_list[meal] = ["No groceries found"]
        else:
            grocery_list[meal] = ["Error fetching groceries"]
    
    return grocery_list

def main():
    st.set_page_config(page_title="Personalized Nutrition & Health", layout="wide")
    
    menu = ["Home", "Upload Reports", "Meal Plan", "Grocery Recommendations", "Subscription"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    if choice == "Home":
        st.title("Welcome to Your Personalized Nutrition Tracker")
        st.write("Upload your DNA/microbiome reports and get AI-powered meal plans!")
        st.image("nutrition_banner.jpg", use_column_width=True)
    
    elif choice == "Upload Reports":
        st.title("Upload Your Health Reports")
        uploaded_file = st.file_uploader("Upload your DNA or microbiome report (PDF, CSV, or TXT)", type=["pdf", "csv", "txt"])
        if uploaded_file is not None:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")
    
    elif choice == "Meal Plan":
        st.title("Your Personalized AI-Generated Meal Plan")
        st.write("Based on your health data, here is your meal plan:")
        meal_plan = generate_meal_plan()
        for meal, food in meal_plan.items():
            st.subheader(meal)
            st.write(f"🍽 {food}")
    
    elif choice == "Grocery Recommendations":
        st.title("Smart Grocery Shopping")
        st.write("Here are your grocery recommendations based on your meal plan:")
        meal_plan = generate_meal_plan()
        grocery_list = get_grocery_recommendations(meal_plan)
        
        for meal, items in grocery_list.items():
            st.subheader(meal)
            for item in items:
                st.write(f"🛒 {item}")
    
    elif choice == "Subscription":
        st.title("Upgrade to Premium")
        st.write("Exclusive features coming soon!")
    
if __name__ == "_main_":
    main()
