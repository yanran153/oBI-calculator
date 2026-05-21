import streamlit as st

# 页面设置
st.set_page_config(page_title="oBI Risk Calculator", page_icon="🔥")
st.title("Older adult Burn Index (oBI) Risk Calculator")
st.markdown("This tool is intended for clinical reference only and does not constitute medical advice.")

# 输入区域
st.header("Patient Information")
age = st.number_input("Age (years)", min_value=18, max_value=120, value=65, step=1)
second_degree = st.number_input("Second-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
third_degree = st.number_input("Third-degree burn area (% TBSA)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)

# 计算按钮
if st.button("Calculate Risk"):
    # 计算oBI
    oBI = 0.07 * second_degree + 0.10 * third_degree + delta_age(age)
    
    # 风险分层
    if oBI < 7.52:
        risk = "Low Risk"
        mortality = "~3.0%"
        color = "green"
    elif oBI < 10.16:
        risk = "Moderate Risk"
        mortality = "~31.2%"
        color = "orange"
    else:
        risk = "High Risk"
        mortality = "~88.9%"
        color = "red"
    
    # 显示结果
    st.header("Result")
    st.markdown(f"**oBI Score:** {oBI:.2f}")
    st.markdown(f"**Risk Level:** :{color}[{risk}]")
    st.markdown(f"**Estimated In-hospital Mortality:** {mortality}")
    st.markdown("---")
    st.caption("Note: This is a research tool for clinical reference. Individual patient assessment should consider all available clinical information.")

def delta_age(age):
    if age < 60:
        return 0
    elif age < 75:
        return 0.75
    elif age < 85:
        return 3.40
    else:
        return 4.10