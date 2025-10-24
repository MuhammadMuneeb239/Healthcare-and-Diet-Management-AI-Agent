# food_nutrition_health_assistant.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date
from math import floor

# -------------------------------
# Nutrition dictionary (per 100g)
nutrition_dict = {
    # Fruits
    "apple": {"calories": 52, "protein": 0.3},
    "banana": {"calories": 96, "protein": 1.3},
    "orange": {"calories": 47, "protein": 0.9},
    "grapes": {"calories": 69, "protein": 0.7},
    "mango": {"calories": 60, "protein": 0.8},
    "pineapple": {"calories": 50, "protein": 0.5},
    "strawberry": {"calories": 33, "protein": 0.7},
    "watermelon": {"calories": 30, "protein": 0.6},
    "pear": {"calories": 57, "protein": 0.4},
    "peach": {"calories": 39, "protein": 0.9},
    "kiwi": {"calories": 61, "protein": 1.1},
    "papaya": {"calories": 43, "protein": 0.5},
    "pomegranate": {"calories": 83, "protein": 1.7},
    "blueberry": {"calories": 57, "protein": 0.7},
    "cherry": {"calories": 50, "protein": 1.0},
    "avocado": {"calories": 160, "protein": 2.0},

    # Vegetables
    "carrot": {"calories": 41, "protein": 0.9},
    "potato": {"calories": 77, "protein": 2.0},
    "tomato": {"calories": 18, "protein": 0.9},
    "cucumber": {"calories": 16, "protein": 0.7},
    "broccoli": {"calories": 34, "protein": 2.8},
    "spinach": {"calories": 23, "protein": 2.9},
    "cabbage": {"calories": 25, "protein": 1.3},
    "onion": {"calories": 40, "protein": 1.1},
    "peas": {"calories": 81, "protein": 5.4},
    "corn": {"calories": 86, "protein": 3.2},

    # Staples
    "rice": {"calories": 130, "protein": 2.7},
    "bread": {"calories": 265, "protein": 9.0},
    "pasta": {"calories": 131, "protein": 5.0},
    "oats": {"calories": 389, "protein": 16.9},

    # Proteins
    "chicken": {"calories": 239, "protein": 27.0},
    "beef": {"calories": 250, "protein": 26.0},
    "mutton": {"calories": 294, "protein": 25.0},
    "egg": {"calories": 155, "protein": 13.0},
    "fish": {"calories": 206, "protein": 22.0},
    "tofu": {"calories": 76, "protein": 8.0},
    "lentils": {"calories": 116, "protein": 9.0},
    "beans": {"calories": 347, "protein": 21.0},

    # Fast Foods
    "burger": {"calories": 295, "protein": 17.0},
    "pizza": {"calories": 266, "protein": 11.0},
    "sandwich": {"calories": 250, "protein": 12.0},
    "fries": {"calories": 312, "protein": 3.4},
    "hotdog": {"calories": 290, "protein": 11.0},

    # Drinks / Others
    "milk": {"calories": 42, "protein": 3.4},
    "yogurt": {"calories": 59, "protein": 10.0},
    "cheese": {"calories": 402, "protein": 25.0},
    "ice cream": {"calories": 207, "protein": 3.5},
    "chocolate": {"calories": 546, "protein": 7.8},
    "coffee": {"calories": 2, "protein": 0.1},
    "tea": {"calories": 1, "protein": 0.1}
}

# Small health tips for a few items
health_tips = {
    "apple": "Rich in fiber and Vitamin C — good for digestion.",
    "banana": "High in potassium — great post-workout snack.",
    "chicken": "High in protein — supports muscle repair & growth.",
    "rice": "Good source of carbs — provides energy for workouts.",
    "fish": "Contains omega-3 fatty acids — heart healthy.",
    "mutton": "High in protein and iron — good for strength but calorie-dense.",
    "beef": "Excellent protein & B12 source — helpful for muscle mass.",
    "spinach": "High in iron and micronutrients — great in salads."
}

# Activity factors
activity_factors = {
    "Sedentary (little/no exercise)": 1.2,
    "Light (1-3 days/week)": 1.375,
    "Moderate (3-5 days/week)": 1.55,
    "Active (6-7 days/week)": 1.725,
    "Very Active (hard training/physical job)": 1.9
}

# -------------------------------
# Helpers
def calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calc_bmr(gender: str, weight: float, height: float, age: int) -> float:
    # Mifflin-St Jeor
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def estimate_from_serving(food_key: str, gram: float):
    info = nutrition_dict.get(food_key)
    if not info:
        return 0.0, 0.0
    cal = (info["calories"] / 100.0) * gram
    pro = (info["protein"] / 100.0) * gram
    return cal, pro

def small_health_tip(food_key: str):
    return health_tips.get(food_key.lower(), None)

# -------------------------------
# Streamlit UI settings
st.set_page_config(page_title="Nutrition & Health Assistant", page_icon="🥗", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF6347;'>🥗 Nutrition & Health Assistant</h1>", unsafe_allow_html=True)
st.write("A compact personal nutrition & health helper — food lookup, daily needs, personalized plans, and basic condition-aware tips.")
st.markdown("**Note:** This is an educational tool. Not a substitute for professional medical advice. Consult a healthcare professional for diagnosis or treatment.")

# Tabs
tab_food, tab_personal, tab_health = st.tabs(["🍽️ Food Nutrition", "⚡ Personal Plan & Daily Needs", "🩺 Health Advisor"])

# -------------------------------
# Tab 1: Food Nutrition
with tab_food:
    st.write("### Food nutrition lookup (per 100g) — enter any food name and quantity in grams.")
    a_col, b_col = st.columns([2, 1])
    with a_col:
        food_input = st.text_input("Type food/fruit name:", "")
    with b_col:
        quantity = st.number_input("Quantity (grams):", min_value=1, value=100)

    if st.button("Get Nutrition", key="food_lookup"):
        st.markdown("---")
        food_name = food_input.strip().lower()
        if not food_name:
            st.error("Please enter a food name.")
        else:
            st.subheader(f"🍽️ {food_input.strip().capitalize()}")
            if food_name in nutrition_dict:
                cal_per100 = nutrition_dict[food_name]["calories"]
                pro_per100 = nutrition_dict[food_name]["protein"]
                total_cal = (cal_per100 / 100) * quantity
                total_pro = (pro_per100 / 100) * quantity

                st.success(f"🔥 Calories: **{total_cal:.1f} kcal** — 💪 Protein: **{total_pro:.1f} g** (for {quantity} g)")

                # Session targets fallback
                daily_cals = st.session_state.get("target_cals", 2000)
                daily_protein = st.session_state.get("target_protein", 50)

                cal_pct = (total_cal / daily_cals) * 100 if daily_cals else 0
                pro_pct = (total_pro / daily_protein) * 100 if daily_protein else 0

                st.info(f"📊 This is ~**{cal_pct:.1f}%** of your daily calories and **{pro_pct:.1f}%** of your daily protein target.")

                # Chart
                fig, ax = plt.subplots()
                ax.bar(["Calories (kcal)", "Protein (g)"], [total_cal, total_pro], color=["#FF6347", "#4682B4"])
                ax.set_title("Nutritional Breakdown")
                st.pyplot(fig)

                tip = small_health_tip(food_name)
                if tip:
                    st.markdown(f"💡 **Tip:** {tip}")
            else:
                st.error("❌ Nutrition info not available for this item. Try common names like 'chicken', 'rice', 'apple'.")

# -------------------------------
# Tab 2: Personal Plan & Daily Needs
with tab_personal:
    st.write("### Personal daily needs & a sample diet/workout plan")
    # Input row 1: DOB & gender
    c1, c2 = st.columns(2)
    with c1:
        dob = st.date_input("Date of Birth:", value=date(2003, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
    with c2:
        gender = st.radio("Gender:", ["Male", "Female"])

    # Input row 2: weight & height
    c3, c4 = st.columns(2)
    with c3:
        weight = st.number_input("Weight (kg):", min_value=30.0, max_value=300.0, value=70.0, step=0.5)
    with c4:
        height = st.number_input("Height (cm):", min_value=120.0, max_value=230.0, value=170.0, step=0.5)

    age = calculate_age(dob)

    goal = st.selectbox("Goal:", ["Maintain Weight", "Lose Weight (fat loss)", "Gain Muscle (lean mass)"])
    activity_label = st.selectbox("Activity Level:", list(activity_factors.keys()), index=2)
    activity_factor = activity_factors[activity_label]

    target_date = st.date_input("Target date to achieve goal (optional):", value=date.today())

    if st.button("Calculate Personal Plan", key="personal_calc"):
        st.markdown("---")
        st.subheader("🧾 Personal Summary")
        st.write(f"Age: **{age}** — Gender: **{gender}** — Weight: **{weight:.1f} kg** — Height: **{height:.1f} cm**")
        st.write(f"Activity: **{activity_label}** — Goal: **{goal}**")

        bmr = calc_bmr(gender, weight, height, age)
        maintenance = bmr * activity_factor

        if goal == "Lose Weight (fat loss)":
            target_cals = maintenance - 500
        elif goal == "Gain Muscle (lean mass)":
            target_cals = maintenance + 300
        else:
            target_cals = maintenance

        # Protein targets by goal
        if goal == "Gain Muscle (lean mass)":
            protein_target = weight * 1.8
        elif goal == "Lose Weight (fat loss)":
            protein_target = weight * 1.5
        else:
            protein_target = weight * 1.2

        # Save session targets
        st.session_state["target_cals"] = target_cals
        st.session_state["target_protein"] = protein_target

        st.success(f"⚡ BMR: **{bmr:.0f} kcal/day** — Maintenance: **{maintenance:.0f} kcal/day**")
        st.success(f"🔥 Target Calories: **{target_cals:.0f} kcal/day** — 💪 Protein target: **{protein_target:.0f} g/day**")

        # Diet plan (rule-based sample)
        st.markdown("### 🍱 Sample Daily Diet Plan (example, adjustable)")
        def build_plan_for_goal(goal_choice):
            plan = {"Breakfast": [], "Lunch": [], "Snack": [], "Dinner": []}
            if goal_choice == "Gain Muscle (lean mass)":
                plan["Breakfast"] = [("oats", 70), ("milk", 200), ("banana", 120)]
                plan["Lunch"] = [("rice", 200), ("chicken", 180), ("spinach", 100)]
                plan["Snack"] = [("yogurt", 150), ("egg", 50)]
                plan["Dinner"] = [("beef", 180), ("potato", 150), ("broccoli", 100)]
            elif goal_choice == "Lose Weight (fat loss)":
                plan["Breakfast"] = [("oats", 40), ("milk", 150), ("apple", 120)]
                plan["Lunch"] = [("chicken", 150), ("spinach", 150), ("tomato", 100)]
                plan["Snack"] = [("yogurt", 120), ("banana", 80)]
                plan["Dinner"] = [("fish", 150), ("broccoli", 120), ("cucumber", 100)]
            else:
                plan["Breakfast"] = [("oats", 50), ("milk", 200), ("banana", 100)]
                plan["Lunch"] = [("rice", 180), ("chicken", 150), ("peas", 100)]
                plan["Snack"] = [("apple", 150), ("yogurt", 120)]
                plan["Dinner"] = [("fish", 150), ("potato", 150), ("spinach", 100)]
            return plan

        plan = build_plan_for_goal(goal)
        plan_totals = {"cal": 0.0, "pro": 0.0}
        for meal, items in plan.items():
            with st.expander(meal + " (click to expand)", expanded=(meal == "Breakfast")):
                meal_cal = 0.0
                meal_pro = 0.0
                for fk, g in items:
                    cal, pro = estimate_from_serving(fk, g)
                    meal_cal += cal
                    meal_pro += pro
                    st.write(f"- {fk.capitalize()} — {g} g → {cal:.0f} kcal, {pro:.1f} g protein")
                st.markdown(f"**Meal total:** {meal_cal:.0f} kcal — {meal_pro:.1f} g protein")
                plan_totals["cal"] += meal_cal
                plan_totals["pro"] += meal_pro

        st.markdown("---")
        st.subheader("Plan summary vs targets")
        st.write(f"Planned calories: **{plan_totals['cal']:.0f} kcal** — Target: **{target_cals:.0f} kcal**")
        st.write(f"Planned protein: **{plan_totals['pro']:.0f} g** — Target: **{protein_target:.0f} g**")
        if plan_totals["cal"] < target_cals:
            st.info(f"Planned meals are **{target_cals - plan_totals['cal']:.0f} kcal** below target — consider an extra snack or slightly larger portions.")
        elif plan_totals["cal"] > target_cals + 200:
            st.info(f"Planned meals are **{plan_totals['cal'] - target_cals:.0f} kcal** above target — consider slightly smaller portions or leaner choices.")
        else:
            st.success("Planned meals are close to your calorie target — good balance!")

        if plan_totals["pro"] < protein_target:
            st.info(f"Protein is **{protein_target - plan_totals['pro']:.0f} g** below target — add an egg, extra yogurt, or more chicken/fish.")
        else:
            st.success("Protein target is covered by the plan ✔️")

        # Workout suggestions
        st.markdown("### 🏋️ Workout Suggestions")
        if goal == "Lose Weight (fat loss)":
            st.write("- Cardio: 30–45 min moderate cardio most days (5×/week).")
            st.write("- Strength: 2–3 full-body sessions/week (20–30 min) to preserve muscle.")
            st.write("- Daily movement and sleep help manage appetite and energy.")
        elif goal == "Gain Muscle (lean mass)":
            st.write("- Strength: 45–60 min, 4 days/week (progressive overload).")
            st.write("- Cardio: light 10–20 min 2×/week to keep conditioning.")
            st.write("- Prioritize protein intake, gradual calorie surplus, and rest.")
        else:
            st.write("- 30 min moderate activity most days + 2 strength sessions/week for maintenance.")

        # Timeline (if using target_date)
        if target_date and target_date > date.today():
            days_left = (target_date - date.today()).days
            st.markdown("---")
            st.subheader("Timeline note")
            if goal == "Lose Weight (fat loss)":
                st.write(f"{days_left} days left. Safe loss: ~0.25–0.5 kg/week; be patient and consistent.")
            elif goal == "Gain Muscle (lean mass)":
                st.write(f"{days_left} days left. Muscle gains are slow — aim for ~0.25–0.5 kg/month of lean mass.")
            else:
                st.write(f"{days_left} days left — focus on consistency.")

        st.balloons()

# -------------------------------
# Tab 3: Health Advisor (Diabetes & Blood Pressure)
with tab_health:
    st.write("### Health Advisor — basic condition-aware diet & activity suggestions")
    st.markdown("Select any conditions you have. This section gives conservative, general recommendations to help manage common conditions. **Not medical advice.**")
    cond_cols = st.columns(3)
    with cond_cols[0]:
        has_diabetes = st.checkbox("Diabetes (type 1 / type 2)")
    with cond_cols[1]:
        has_high_bp = st.checkbox("High Blood Pressure (Hypertension)")
    with cond_cols[2]:
        has_low_bp = st.checkbox("Low Blood Pressure (Hypotension)")

    # Basic medical info to tailor suggestions (reuse personal inputs if already filled)
    st.write("Provide some basic details (these help tailor simple suggestions):")
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        dob_h = st.date_input("DOB (for age, optional):", value=date(2003, 1, 1),min_value=date(1900, 1, 1), max_value=date.today(), key="dob_health")
        age_h = calculate_age(dob_h)
        st.write(f"Age: {age_h}")
    with h_col2:
        bp_weight = st.number_input("Weight (kg) (optional):", min_value=30.0, max_value=300.0, value=70.0, key="weight_health")

    # If none selected, show info
    if not (has_diabetes or has_high_bp or has_low_bp):
        st.info("Select one or more conditions to receive condition-aware diet & activity tips.")
    else:
        st.markdown("---")
        # DIABETES ADVICE
        if has_diabetes:
            st.subheader("Diabetes — diet & activity suggestions")
            st.write("Goal: control blood glucose by managing carbs, prioritizing fiber, and regular activity.")
            st.markdown("**Diet tips (general):**")
            st.write("- Favor complex carbs (oats, legumes), vegetables, lean proteins, and healthy fats.")
            st.write("- Avoid sugary drinks, sweets, white bread, and highly processed foods.")
            st.write("- Prefer whole fruits over fruit juices. Monitor portion sizes of starchy foods (rice, potatoes).")
            st.write("- Spread carbohydrates across the day and include protein & fiber to slow glucose spikes.")
            st.markdown("**Sample daily choices:**")
            st.write("- Breakfast: oats + milk + berries or egg + veggies.")
            st.write("- Lunch: lentils/beans or chicken + lots of salad/vegetables + small portion of rice.")
            st.write("- Snack: apple + nuts or yogurt.")
            st.write("- Dinner: fish/tofu + veggies (smaller carb portion).")
            st.markdown("**Activity:**")
            st.write("- Aim for ~30 minutes moderate exercise (walking) most days; strength training 2×/week helps insulin sensitivity.")
            st.markdown("**Monitoring & Caution:**")
            st.write("- If on medication (insulin or others), follow medical advice and monitor blood glucose; adjust carbs with clinician guidance.")
            st.write("- This tool gives general tips — always consult your doctor for treatment.")

        # HIGH BLOOD PRESSURE ADVICE
        if has_high_bp:
            st.subheader("High Blood Pressure — diet & activity suggestions")
            st.write("Goal: lower blood pressure naturally via reduced salt, increased potassium, weight management, and cardio.")
            st.markdown("**Diet tips (general):**")
            st.write("- Reduce added salt and processed foods high in sodium.")
            st.write("- Eat potassium-rich foods (banana, spinach, potatoes in moderation), fresh fruits & vegetables, lean proteins.")
            st.write("- Favor low-fat dairy (milk, yogurt) and whole grains.")
            st.markdown("**Foods to avoid / limit:**")
            st.write("- Salty snacks, canned soups high in sodium, processed meats (sausages, bacon), excessive alcohol.")
            st.markdown("**Activity:**")
            st.write("- Regular aerobic activity (30 minutes most days) — brisk walking, cycling, or swimming helps reduce BP.")
            st.write("- Strength training 2×/week is fine; check with a clinician if you have severe hypertension.")
            st.markdown("**Monitoring & Caution:**")
            st.write("- If on BP medication, follow your clinician; sudden large changes in diet/exercise should be discussed with them.")

        # LOW BLOOD PRESSURE ADVICE
        if has_low_bp:
            st.subheader("Low Blood Pressure — diet & activity suggestions")
            st.write("Goal: maintain adequate blood pressure and avoid dizziness/fainting.")
            st.markdown("**Diet tips (general):**")
            st.write("- Stay well-hydrated, include small frequent meals, increase salt moderately if advised by clinician.")
            st.write("- Include balanced carbs and proteins; avoid sudden large meals that cause 'postprandial' drops.")
            st.markdown("**Activity:**")
            st.write("- Gentle aerobic activity (walking) is good; avoid sudden standing up from sitting quickly.")
            st.write("- Strength training is helpful; focus on good hydration and gradual progress.")
            st.markdown("**Monitoring & Caution:**")
            st.write("- If you feel faint/dizzy frequently, consult a clinician. Do not self-medicate.")

        st.markdown("---")
        st.subheader("Practical combined advice (if multiple conditions)")
        st.write("- Emphasize whole foods, lean proteins, vegetables, and controlled portions.")
        st.write("- Avoid sugary drinks & excessive salt; prioritize hydration and regular activity.")
        st.write("- Use the Personal Plan tab to get calorie & protein targets, then apply these condition-specific food choices.")
        st.success("These are general lifestyle recommendations. For tailored medical advice, tests, and prescriptions, consult a healthcare professional.")

# End of app
st.markdown("---")

