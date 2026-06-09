# ============================================
# نظام الري الذكي - لوحة التحكم من البيانات الفعلية
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام الري الذكي", page_icon="🌾", layout="wide")

# عنوان رئيسي
st.title("🌾 نظام الري الذكي - لوحة التحكم المتقدمة")
st.markdown("---")

# ============================================
# 1. تحميل البيانات
# ============================================
uploaded_file = st.file_uploader("📂 حمّل ملف CSV بيانات المستشعرات", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    st.success(f"✅ تم تحميل {len(df)} قراءة من {df['timestamp'].min().date()} إلى {df['timestamp'].max().date()}")
    
    # ============================================
    # 2. اختيار اليوم والوقت
    # ============================================
    st.subheader("📅 اختر قراءة معينة لعرض التفاصيل")
    
    # قائمة بجميع التواريخ والمواعيد
    df['date_str'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    selected_timestamp = st.selectbox("اختر التوقيت", df['date_str'].tolist())
    
    # جلب بيانات الصف المختار
    current_data = df[df['date_str'] == selected_timestamp].iloc[0]
    
    # ============================================
    # 3. عرض القراءات الحالية
    # ============================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ درجة الحرارة", f"{current_data['temperature_C']} °C")
    with col2:
        st.metric("💧 الرطوبة الجوية", f"{current_data['humidity_%']} %")
    with col3:
        st.metric("🧂 الملوحة", f"{current_data['salinity_EC_dSm']} dS/m")
    with col4:
        st.metric("📋 حالة التربة", current_data['soil_condition'])
    
    # ============================================
    # 4. قرار النظام الفعلي
    # ============================================
    decision = current_data['system_decision']
    if decision == "SYSTEM OK":
        st.success(f"✅ قرار النظام: {decision}")
    elif decision == "IRRIGATE NOW":
        st.warning(f"💧 قرار النظام: {decision} - يلزم الري فورًا")
    else:
        st.error(f"🧬 قرار النظام: {decision} - PGPR + ري مطلوب")
    
    st.markdown("---")
    
    # ============================================
    # 5. الرسوم البيانية
    # ============================================
    st.subheader("📈 تطور القياسات خلال الأسبوع")
    
    # اختيار عرض آخر 50 قراءة أو كل البيانات
    days_to_show = st.slider("عدد الأيام الماضية للعرض", 1, 7, 3)
    cutoff_date = df['timestamp'].max() - pd.Timedelta(days=days_to_show)
    df_filtered = df[df['timestamp'] >= cutoff_date]
    
    # رسم بياني للملوحة
    fig1 = px.line(df_filtered, x='timestamp', y='salinity_EC_dSm', 
                   title='🧂 تطور الملوحة',
                   labels={'timestamp': 'التاريخ', 'salinity_EC_dSm': 'الملوحة (dS/m)'})
    fig1.add_hlines(y=8, line_dash="dash", line_color="red", annotation_text="حد الخطر (8 dS/m)")
    st.plotly_chart(fig1, use_container_width=True)
    
    # رسم بياني للرطوبة والحرارة معًا
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_filtered['timestamp'], y=df_filtered['humidity_%'], 
                              mode='lines+markers', name='الرطوبة %'))
    fig2.add_trace(go.Scatter(x=df_filtered['timestamp'], y=df_filtered['temperature_C'], 
                              mode='lines+markers', name='درجة الحرارة °C', yaxis="y2"))
    fig2.update_layout(
        title='🌡️ تطور الرطوبة ودرجة الحرارة',
        xaxis_title='التاريخ',
        yaxis_title='الرطوبة (%)',
        yaxis2=dict(title='درجة الحرارة (°C)', overlaying='y', side='right')
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # ============================================
    # 6. إحصائيات القرارات
    # ============================================
    st.subheader("📊 إحصائيات قرارات النظام")
    
    decision_stats = df['system_decision'].value_counts()
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("✅ SYSTEM OK", decision_stats.get("SYSTEM OK", 0))
    col_b.metric("💧 IRRIGATE NOW", decision_stats.get("IRRIGATE NOW", 0))
    col_c.metric("🧬 PGPR + IRR ON", decision_stats.get("PGPR + IRR ON", 0))
    
    # ============================================
    # 7. جدول جميع البيانات
    # ============================================
    with st.expander("📋 عرض جميع البيانات"):
        st.dataframe(df)
    
    # ============================================
    # 8. تحليل ذكي إضافي
    # ============================================
    st.subheader("🧠 تحليل ذكي - أنماط المشاكل")
    
    # متى زادت الملوحة عن 8؟
    high_salinity = df[df['salinity_EC_dSm'] > 8]
    if not high_salinity.empty:
        st.warning(f"⚠️ سجلت الملوحة أعلى من 8 dS/m في {len(high_salinity)} قراءة")
        st.dataframe(high_salinity[['timestamp', 'salinity_EC_dSm', 'soil_condition', 'system_decision']])
    
    # متى كانت الرطوبة أقل من 30%؟
    low_humidity = df[df['humidity_%'] < 30]
    if not low_humidity.empty:
        st.warning(f"💨 سجلت رطوبة أقل من 30% في {len(low_humidity)} قراءة")
        st.dataframe(low_humidity[['timestamp', 'humidity_%', 'temperature_C', 'system_decision']])
    
else:
    # إذا لم يرفع المستخدم ملف
    st.info("👈 يرجى رفع ملف CSV الذي يحتوي على بيانات المستشعرات")
    st.markdown("""
    **تنسيق الملف المطلوب:**
    - يجب أن يحتوي على الأعمدة التالية:
      - `timestamp` (تاريخ ووقت)
      - `humidity_%` (الرطوبة الجوية)
      - `salinity_EC_dSm` (الملوحة)
      - `temperature_C` (درجة الحرارة)
      - `soil_condition` (حالة التربة)
      - `system_decision` (قرار النظام)
    """)