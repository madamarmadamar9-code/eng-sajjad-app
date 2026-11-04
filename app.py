import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(page_title="الحاسبة الهندسية الشاملة - م. سجاد علي", layout="wide")

# CSS لدعم اللغة العربية وتنسيق الواجهة
st.markdown("""
    <style>
        body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
        .stButton>button { width: 100%; background-color: #2E86C1; color: white; border-radius: 8px; }
        .stButton>button:hover { background-color: #1B4F72; }
        .total-box { background-color: #D4EFDF; padding: 20px; border-radius: 10px; border: 2px solid #27AE60; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ الحاسبة الهندسية الشاملة (الكميات، التكاليف، والتنبؤ)")
st.markdown("إعداد وإشراف: المهندس سجاد علي")

# ==========================================
# 2. قاعدة بيانات الأسعار (مستوحاة من النشرة العراقية)
# ==========================================
# يمكنك لاحقاً تبديل هذا بـ pd.read_excel('prices.xlsx')
PRICES_DB = {
    "خرسانة جاهزة (متر مكعب)": 110000,
    "حديد تسليح (طن)": 980000,
    "طابوق (ألف طابوقة)": 180000,
    "رمل (متر مكعب)": 150000, # سعر اللوري تقريباً
    "حصى (متر مكعب)": 170000,
    "سمنت (طن)": 110000,
    "كاشي أو سيراميك (متر مربع)": 12000,
    "لبخ - مواد وعمل (متر مربع)": 8000,
    "صبغ - مواد وعمل (متر مربع)": 6000,
    "تأسيسات كهربائية (نقطة)": 15000
}

# ==========================================
# 3. نظام التخزين (Session State) لجدول الكميات
# ==========================================
if 'project_items' not in st.session_state:
    st.session_state.project_items = []

def add_to_project(item_name, quantity, unit, unit_price):
    total = quantity * unit_price
    st.session_state.project_items.append({
        "الفقرة": item_name,
        "الكمية": round(quantity, 2),
        "الوحدة": unit,
        "سعر الوحدة (دينار)": unit_price,
        "الكلفة الإجمالية (دينار)": total
    })
    st.success(f"✅ تمت إضافة {item_name} بنجاح إلى جدول الكميات!")

# ==========================================
# 4. تقسيم الواجهة إلى أقسام (Tabs)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📐 حساب الكميات (إضافة للمشروع)", 
    "📊 جدول الكميات والكلفة الكلية", 
    "📈 التنبؤ بأسعار المواد (AI)", 
    "👷‍♂️ طاقم العمالة"
])

# ---------------------------------------------------------
# القسم الأول: حساب الكميات الذكي بناءً على الأبعاد
# ---------------------------------------------------------
with tab1:
    st.header("حساب الكميات الهندسية")
    category = st.selectbox("اختر نوع العمل:", 
                            ["الأعمال الخرسانية (أساسات، أعمدة، سقوف)", 
                             "أعمال حديد التسليح", 
                             "أعمال الإنهاءات (لبخ، صبغ، سيراميك/كاشي)"])
    
    st.markdown("---")
    
    # 1. الخرسانة
    if category == "الأعمال الخرسانية (أساسات، أعمدة، سقوف)":
        st.subheader("حساب حجم الخرسانة")
        col1, col2, col3 = st.columns(3)
        length = col1.number_input("الطول الكلي (متر)", min_value=0.0, value=10.0)
        width = col2.number_input("العرض الكلي (متر)", min_value=0.0, value=10.0)
        thickness = col3.number_input("السُمك أو الارتفاع (متر)", min_value=0.0, value=0.2) # 20 سم للأساس مثلاً
        
        volume = length * width * thickness
        st.info(f"حجم الخرسانة المطلوب = {volume:.2f} متر مكعب")
        
        if st.button("إضافة الخرسانة للمشروع"):
            add_to_project("خرسانة جاهزة", volume, "متر مكعب", PRICES_DB["خرسانة جاهزة (متر مكعب)"])

    # 2. الحديد
    elif category == "أعمال حديد التسليح":
        st.subheader("حساب كمية الحديد")
        vol_concrete = st.number_input("أدخل حجم الخرسانة (متر مكعب):", min_value=0.0, value=20.0)steel_ratio = st.slider("نسبة التسليح (كغم/متر مكعب) حسب المخطط:", 80, 200, 100)
        steel_type = st.selectbox("نوع القطر المستخدم أغلب شيء:", ["أبو 12 ملم", "أبو 16 ملم (شائع للأساسات)", "أبو 20 ملم"])
        
        total_steel_kg = vol_concrete * steel_ratio
        total_steel_ton = total_steel_kg / 1000
        
        st.info(f"الكمية المطلوبة = {total_steel_ton:.2f} طن (من حديد {steel_type})")
        
        if st.button("إضافة الحديد للمشروع"):
            add_to_project(f"حديد تسليح ({steel_type})", total_steel_ton, "طن", PRICES_DB["حديد تسليح (طن)"])

    # 3. الإنهاءات
    elif category == "أعمال الإنهاءات (لبخ، صبغ، سيراميك/كاشي)":
        st.subheader("حساب مساحات الإنهاءات")
        finishing_type = st.selectbox("اختر الفقرة:", ["لبخ", "صبغ", "كاشي أو سيراميك"])
        
        col1, col2 = st.columns(2)
        l = col1.number_input("الطول الإجمالي للجدران/الأرضية (متر)", min_value=0.0, value=12.0)
        h = col2.number_input("الارتفاع أو العرض (متر)", min_value=0.0, value=3.0)
        
        area = l * h
        st.info(f"المساحة السطحية المطلوبة = {area:.2f} متر مربع")
        
        if st.button(f"إضافة {finishing_type} للمشروع"):
            item_key = f"{finishing_type} - مواد وعمل (متر مربع)" if finishing_type in ["لبخ", "صبغ"] else "كاشي أو سيراميك (متر مربع)"
            add_to_project(finishing_type, area, "متر مربع", PRICES_DB[item_key])

# ---------------------------------------------------------
# القسم الثاني: جدول الكميات (BoQ) والكلفة الكلية
# ---------------------------------------------------------
with tab2:
    st.header("جدول الكميات المُسعّر (BoQ)")
    
    if len(st.session_state.project_items) > 0:
        df_project = pd.DataFrame(st.session_state.project_items)
        
        # تنسيق الأرقام بوجود فوارز
        st.dataframe(df_project.style.format({"سعر الوحدة (دينار)": "{:,.0f}", "الكلفة الإجمالية (دينار)": "{:,.0f}"}), use_container_width=True)
        
        total_materials_cost = df_project["الكلفة الإجمالية (دينار)"].sum()
        
        st.markdown(f"""
        <div class="total-box">
            <h3>إجمالي كلفة المواد المُضافة للمشروع</h3>
            <h1>{total_materials_cost:,.0f} دينار عراقي</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ مسح كل البيانات والبدء من جديد"):
            st.session_state.project_items = []
            st.rerun()
    else:
        st.warning("جدول الكميات فارغ. اذهب إلى قسم (حساب الكميات) لإضافة المواد للمشروع.")

# ---------------------------------------------------------
# القسم الثالث: التنبؤ الذكي بالأسعار (AI Forecasting)
# ---------------------------------------------------------
with tab3:
    st.header("📈 تحليل اتجاهات السوق والتنبؤ بأسعار النشرة العراقية")
    st.write("يقوم البرنامج بتحليل أسعار الأشهر التسعة الأولى باستخدام الانحدار الخطي (Linear Regression) للتنبؤ بالربع الأخير من السنة.")
    
    material_to_predict = st.selectbox("اختر المادة لتحليل أسعارها:", ["حديد تسليح (طن)", "سمنت (طن)", "طابوق (ألف طابوقة)"])
    
    # بيانات افتراضية للأشهر 1 إلى 9 (يمكنك تعديلها بناءً على النشرة الحقيقية)
    months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    if material_to_predict == "حديد تسليح (طن)":
        historical_prices = np.array([950000, 955000, 960000, 975000, 970000, 985000, 990000, 1000000, 980000])
    elif material_to_predict == "سمنت (طن)":
        historical_prices = np.array([105000, 106000, 106000, 107000, 108000, 109000, 110000, 110000, 111000])
    else:
        historical_prices = np.array([170000, 172000, 175000, 175000, 178000, 180000, 182000, 180000, 185000])
    
    # خوارزمية التنبؤ (Linear Regression)
    z = np.polyfit(months, historical_prices, 1) # حساب الميل والتقاطع
    p = np.poly1d(z)
    
    future_months = np.array([10, 11, 12])future_prices = p(future_months)
    
    # دمج البيانات للرسم
    all_months = np.concatenate((months, future_months))
    all_prices = np.concatenate((historical_prices, future_prices))
    status = ['فعلي (النشرة)']*9 + ['تنبؤ ذكي (AI)']*3
    
    df_pred = pd.DataFrame({"الشهر": all_months, "السعر (دينار)": all_prices, "الحالة": status})
    
    # رسم المخطط البياني
    fig = px.line(df_pred, x="الشهر", y="السعر (دينار)", color="الحالة", markers=True,
                  title=f"منحنى الأسعار والتنبؤ لمادة: {material_to_predict}",
                  color_discrete_map={"فعلي (النشرة)": "blue", "تنبؤ ذكي (AI)": "red"})
    
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("تنبؤ شهر 10", f"{future_prices[0]:,.0f} د.ع")
    col2.metric("تنبؤ شهر 11", f"{future_prices[1]:,.0f} د.ع")
    col3.metric("تنبؤ شهر 12", f"{future_prices[2]:,.0f} د.ع")

# ---------------------------------------------------------
# القسم الرابع: طاقم العمالة
# ---------------------------------------------------------
with tab4:
    st.header("تحديد كلفة طاقم العمالة")
    days = st.number_input("عدد أيام العمل المقدرة للمشروع:", min_value=1, value=30)
    
    col1, col2 = st.columns(2)
    engineers = col1.number_input("عدد المهندسين (80,000 د.ع/يوم)", value=1)
    skilled_labor = col2.number_input("عدد العمال المهرة - خلفة (50,000 د.ع/يوم)", value=2)
    unskilled_labor = col1.number_input("عدد العمال غير المهرة (25,000 د.ع/يوم)", value=4)
    guards = col2.number_input("عدد الحراس (15,000 د.ع/يوم)", value=1)
    
    daily_cost = (engineers * 80000) + (skilled_labor * 50000) + (unskilled_labor * 25000) + (guards * 15000)
    total_labor_cost = daily_cost * days
    
    st.info(f"إجمالي كلفة العمالة لمدة {days} يوم = {total_labor_cost:,.0f} دينار عراقي")

# ==========================================
# الخلاصة الكلية بأسفل التطبيق
# ==========================================
st.markdown("---")
st.header("💰 الخلاصة والتكلفة الاستثمارية الكلية للمشروع")

try:
    total_materials = df_project["الكلفة الإجمالية (دينار)"].sum() if len(st.session_state.project_items) > 0 else 0
except:
    total_materials = 0
    
try:
    total_labor = total_labor_cost
except:
    total_labor = 0

grand_total = total_materials + total_labor

col1, col2, col3 = st.columns(3)
col1.metric("تكلفة الكادر والعمالة", f"{total_labor:,.0f} د.ع")
col2.metric("تكلفة المواد والتجهيزات", f"{total_materials:,.0f} د.ع")
col3.metric("🔥 الكلفة الإجمالية للمشروع", f"{grand_total:,.0f} د.ع")
