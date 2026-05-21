import streamlit as st
import math

# ---------------------- 1. Define All the Function Used for Risk Calculation ----------------------
def delta_age(age):
    """Age Stratification Term"""
    if age < 60:
        return 0
    elif age < 75:
        return 0.75
    elif age < 85:
        return 3.40
    else:
        return 4.10

def calculate_mortality_prob(oBI):
    intercept = -8.84   
    oBI = 0.07 * second_degree + 0.10 * third_degree + delta_age(age)
    logit = intercept + oBI
    prob = 1 / (1 + math.exp(-logit))
    return prob

# ---------------------- 2. Streamlit Page Setting ----------------------
st.set_page_config(page_title="oBI Risk Calculator", page_icon="🔥")
st.title("Older adult Burn Index (oBI) Risk Calculator")
st.markdown("This tool is intended for clinical reference only and does not constitute medical advice.")

# ---------------------- 3. Input ----------------------
st.header("Patient Information")
age = st.number_input("Age (years)", min_value=18, max_value=120, value=65, step=1)
second_degree = st.number_input("Second-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
third_degree = st.number_input("Third-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)


# ---------------------- 4. Calculation And Output ----------------------
if st.button("Calculate Risk"):
    # Calculating oBI
    oBI = 0.07 * second_degree + 0.10 * third_degree + delta_age(age)
    
    # Calculating the Risk of Mortality
    mortality_prob = calculate_mortality_prob(oBI)
    
    # Risk Stratification
    if oBI < 7.52:
        risk_level = "Low Risk"
        color_hex =  "#FDF5F7"
        position_text = "Current patient: Low Risk zone (0 – 7.52)"
    elif oBI < 10.16:
        risk_level = "Moderate Risk"
        color_hex = "#E8A0AD"
        position_text = "Current patient: Moderate Risk zone (7.52 – 10.16)"
    else:
        risk_level = "High Risk"
        color_hex = "#91072F"
        position_text = "Current patient: High Risk zone (≥ 10.16)"
   
    # Result Output
    st.header("📊 Calculation Results")
    st.metric(label="oBI Score", value=f"{oBI:.2f}")
    st.metric(label="Estimated In-hospital Mortality", value=f"{mortality_prob:.1%}")

    # Risk Stratification
    st.markdown(
        f'<h3>Risk Level: <span style="color:{color}; font-weight:bold;">{risk_level}</span></h3>',
        unsafe_allow_html=True
    )

    # Risk Interval
    st.markdown("---")
    st.subheader("📏 oBI Risk Interval")
    st.markdown(f"""
    <div style="font-size:18px; font-weight:bold; margin-bottom:10px;">
        0 &nbsp;&nbsp; – &nbsp;&nbsp; 7.52 &nbsp;&nbsp; – &nbsp;&nbsp; 10.16 &nbsp;&nbsp; – &nbsp;&nbsp; ∞
    </div>
    <div style="font-size:16px; color:#555; margin-bottom:10px;">
        Low &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Moderate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; High
    </div>
    <div style="font-size:17px; font-weight:bold; color:{color};">
        {position_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Note: This is a research tool for clinical reference. Individual patient assessment should consider all available clinical information.")
