import streamlit as st
import math

# -------------------------- Helper functions --------------------------
def delta_age(age):
    """Age-related risk adjustment factor based on published oBI formula."""
    if age < 60:
        return 0
    elif age < 75:
        return 0.75
    elif age < 85:
        return 3.40
    else:
        return 4.10

def calculate_otbsa(age, total_tbsa):
    """Calculate age-weighted TBSA (oTBSA) based on age-specific weight."""
    if age < 60:
        weight = 1.00
    elif age < 75:      # 60-74 years
        weight = 1.12
    elif age < 85:      # 75-84 years
        weight = 1.80
    else:               # ≥85 years
        weight = 2.00
    return total_tbsa * weight

# -------------------------- Page config --------------------------
st.set_page_config(page_title="oBI Risk and oTBSA Calculator", page_icon="🔥")
st.title("Older Adult Targeted Dual-tool Risk Assessment Strategy Calculator")
st.markdown("This tool is intended for clinical reference only and does not constitute medical advice.")

# -------------------------- Input section --------------------------
st.header("Patient Information")
age = st.number_input("Age (years)", min_value=18, max_value=120, value=65, step=1)
second_degree = st.number_input("Second-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
third_degree = st.number_input("Third-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)

# Total TBSA (original info box)
total_tbsa = second_degree + third_degree
st.info(f"📐 **Total burn area (second + third degree): {total_tbsa:.1f}% TBSA**")

# oTBSA (apricot custom box)
otbsa = calculate_otbsa(age, total_tbsa)
st.markdown(
    f"""
    <div style="background-color: #F8D4A0; padding: 12px 16px; border-radius: 6px; margin-bottom: 10px; width: 100%;">
        <div style="font-size: 16px; font-weight: bold; color: #C86920;">
            🔥 oTBSA (age‑weighted): {otbsa:.1f}%
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------- Calculation and results --------------------------
if st.button("Calculate Risk"):
    if total_tbsa > 100:
        st.error("❌ Error: Total burn area cannot exceed 100% TBSA. Please adjust inputs.")
        st.stop()
    else:
        oBI = 0.07 * second_degree + 0.10 * third_degree + delta_age(age)

        if oBI < 7.52:
            risk_level = "Low Risk"
            color = "#F28B9F"
            mortality_prob = 0.030
            position_text = "Current patient: Low Risk zone (0 – 7.52)"
        elif oBI < 10.16:
            risk_level = "Moderate Risk"
            color = "#E85970"
            mortality_prob = 0.312
            position_text = "Current patient: Moderate Risk zone (7.52 – 10.16)"
        else:
            risk_level = "High Risk"
            color = "#91072F"
            mortality_prob = 0.889
            position_text = "Current patient: High Risk zone (≥ 10.16)"

        st.header("📊 Calculation Results")
        st.metric(label="oBI Score", value=f"{oBI:.2f}")
        st.metric(label="Estimated In-hospital Mortality", value=f"{mortality_prob:.1%}")

        st.markdown(
            f'<h3>Risk Level: <span style="color:{color}; font-weight:bold;">{risk_level}</span></h3>',
            unsafe_allow_html=True
        )

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
