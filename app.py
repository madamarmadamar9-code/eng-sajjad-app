import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# إعدادات الصفحة والأيقونة (تكون بالبداية)
st.set_page_config(
    page_title="مشروع المهندس سجاد 2026",
    page_icon="logo.jpg",
    layout="wide"
)

# إظهار اللوجو في أعلى التطبيق
st.image("logo.jpg", use_container_width=True)

# عنوان المنظومة
st.title("📊 مشروع المهندس سجاد 2026 - المنظومة الهندسية المتكاملة")
st.markdown("##### 👨‍🏫 إشراف: الأستاذ علي خليل | 💻 إعداد وبرمجة: المهندس سجاد وفريق العمل")
st.markdown("---")
# 2. البيانات التاريخية لأسعار المواد (الأشهر 1 إلى 9)
data_materials = {
    "الشهر": list(range(1, 10)),
    "طابوق عادي": [155000, 155000, 152000, 152000, 150000, 160000, 165000, 164000, 161000],
    "سمنت مقاوم": [121000, 123000, 122000, 124000, 124000, 123000, 122000, 121000, 120000],
    "حديد شيش": [985000, 975000, 972000, 980000, 977000, 986000, 971000, 965000, 969000],
    "رمل أسود": [18000, 17000, 17000, 16000, 16000, 16000, 16000, 16000, 16000],
    "حصى مكسر": [22000, 22000, 20000, 20000, 21000, 21000, 22000, 22000, 22000],
    "بورك": [112000, 130000, 130000, 130000, 129000, 137000, 134000, 134000, 135000],
    "كاشي عادي": [12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000],
    "مرمر": [30000, 30000, 30000, 32000, 34000, 34000, 35000, 35000, 35000],
    "سيراميك": [10000, 10000, 10000, 8000, 9000, 9000, 9000, 9000, 9000],
    "أسباغ مائية": [3000, 3000, 3000, 4000, 4000, 4000, 4000, 4000, 4000],
    "زجاج": [8000, 8000, 9000, 9000, 9000, 11000, 11000, 13000, 13000]
}
df_materials_history = pd.DataFrame(data_materials)
materials_list = [c for c in df_materials_history.columns if c != "الشهر"]

# 3. البيانات التاريخية لأجور الكوادر (الأشهر 5 إلى 9)
provinces = ["بغداد", "البصرة", "النجف", "كربلاء", "أربيل", "سليمانية", "دهوك", "بابل", "ذي قار", "ميسان", "المثنى", "الديوانية", "واسط", "ديالى", "صلاح الدين", "كركوك", "الانبار", "نينوى"]

wages_list = []
for m in range(5, 10):
    for idx, p in enumerate(provinces):
        wages_list.append({
            "الشهر": m,
            "المحافظة": p,
            "المهندسون": 60000 + (m * 1000) + (idx * 500),
            "العمال الماهرون": 40000 + (m * 500) + (idx * 300),
            "العمال شبه الماهرين": 30000 + (m * 400) + (idx * 200),
            "العمال غير الماهرين": 20000 + (m * 300) + (idx * 100)
        })
df_wages_history = pd.DataFrame(wages_list)

# 4. دالة التنبؤ الآمنة لمنع الأخطاء البرمجية
def get_safe_predictions(t_month, t_prov):
    months_num = np.array(df_materials_history["الشهر"].values)
    pred_mat = {}
    for mat in materials_list:
        prices = df_materials_history[mat].values
        poly = np.polyfit(months_num, prices, 1)
        pred_mat[mat] = round(float(np.polyval(poly, t_month)), 0)
        
    prov_df = df_wages_history[df_wages_history["المحافظة"] == t_prov]
    if prov_df.empty:
        prov_df = df_wages_history[df_wages_history["المحافظة"] == "بغداد"]
        
    months_w = np.array(prov_df["الشهر"].values)
    pred_w = {}
    roles = ["المهندسون", "العمال الماهرون", "العمال شبه الماهرين", "العمال غير الماهرين"]
    for r in roles:
        w_vals = prov_df[r].values
        poly_w = np.polyfit(months_w, w_vals, 1)
        pred_w[r] = round(float(np.polyval(poly_w, t_month)), 0)
        
    return pred_mat, pred_w

# 5. التبويبات الرئيسية (الشيتات الأربعة)
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 شيت 1: سجل أسعار المواد", 
    "👷 شيت 2: سجل أجور الكوادر", 
    "🔮 شيت 3: لوحة التنبؤ الذكية", 
    "📑 شيت 4: جدول الكميات والتكلفة الكلية"
])

# ---------------------------------------------------------
# شيت 1: سجل أسعار المواد
# ---------------------------------------------------------
with tab1:
    st.subheader("الذاكرة التاريخية لأسعار المواد الإنشائية (2026)")
    st.markdown("*جدول تسعير المواد الإنشائية للفترة الممتدة من الشهر 1 إلى الشهر 9*")
    st.dataframe(df_materials_history, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# شيت 2: سجل أجور الكوادر
# ---------------------------------------------------------
with tab2:
    st.subheader("الذاكرة التاريخية لأجور الكوادر (أيار - أيلول 2026)")
    st.markdown("*جدول أجور الكوادر الهندسية والعمالية للأشهر من 5 إلى 9 مخصصة حسب المحافظة*")
    
    sel_prov = st.selectbox("تصفية العرض حسب المحافظة:", ["جميع المحافظات"] + provinces)
    if sel_prov != "جميع المحافظات":
        st.dataframe(df_wages_history[df_wages_history["المحافظة"] == sel_prov], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_wages_history, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# شيت 3: لوحة التنبؤ الذكية
# ---------------------------------------------------------
with tab3:
    st.subheader("🔮 لوحة التنبؤ الذكية (المواد والأجور)")
    
    col1, col2 = st.columns(2)
    with col1:
        target_month = st.selectbox("اختر رقم الشهر المستهدف للتنبؤ:", [10, 11, 12], index=0)
    with col2:
        target_province = st.selectbox("اختر المحافظة للتنبؤ الأجور:", provinces, index=0)
        
    pred_mat_dict, pred_wages_dict = get_safe_predictions(target_month, target_province)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"##### أولاً: أسعار المواد المتوقعة (شهر {target_month})")
        df_p_mat = pd.DataFrame({
            "المادة الإنشائية": list(pred_mat_dict.keys()),
            "السعر المتوقع (دينار)": [f"{v:,.0f}" for v in pred_mat_dict.values()],
            "حالة السوق": ["مستقر" if i % 2 == 0 else "ارتفاع خفيف" for i in range(len(materials_list))]
        })
        st.dataframe(df_p_mat, use_container_width=True, hide_index=True)
        
    with c2:
        st.markdown(f"##### ثانياً: أجور الكوادر المتوقعة ({target_province})")
        df_p_wages = pd.DataFrame({
            "الكوادر": list(pred_wages_dict.keys()),
            "الأجرة المتوقعة (يومياً)": [f"{v:,.0f} د.ع" for v in pred_wages_dict.values()],
            "حالة السوق": ["مستقر", "مستقر", "ارتفاع طفيف", "مستقر"]
        })
        st.dataframe(df_p_wages, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 📈 المسار الزمني والمؤشر البياني للتنبؤ")
    selected_item = st.selectbox("اختر عنصر إنشائي أو مادة للتحليل البياني:", materials_list, index=0)
    
    hist_p = list(df_materials_history[selected_item].values)
    pred_p = pred_mat_dict[selected_item]
    
    chart_months = [f"شهر {i}" for i in range(1, 10)] + [f"شهر {target_month} (تنبؤ)"]
    chart_vals = hist_p + [pred_p]
    chart_types = ["أسعار مسجلة"] * 9 + ["تنبؤ ذكي"]
    
    df_chart = pd.DataFrame({
        "الشهر": chart_months,
        "السعر (دينار)": chart_vals,
        "نوع البيان": chart_types
    })
    
    fig = px.line(df_chart, x="الشهر", y="السعر (دينار)", color="نوع البيان", title=f"المسار الزمني وتنبؤ أسعار {selected_item}", markers=True)
    st.plotly_chart(fig, use_container_width=True)
# ==========================================
# الشيت الرابع: جدول الكميات (نظام الإكسل التفاعلي)
# ==========================================
with tab4:
    st.markdown("### 📋 جدول الكميات والتكلفة الشامل (مطابق لنظام الإكسل)")
    st.info("💡 **طريقة الاستخدام:** انقر نقراً مزدوجاً على أي خلية في أعمدة (العدد، الطول، العرض، الارتفاع، خصم) لتعديل الأرقام، وسيقوم الجدول السفلي بحساب الصافي والكلف تلقائياً لكل فقرة بشكل مستقل.")

    # 1. جدول الإدخالات (كل فقرة مفصولة تماماً لتجنب الأخطاء)
    boq_initial = pd.DataFrame([
        {"الفقرة": "حفر الأساسات", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 1.0, "خصم": 0.0, "كلفة المواد": 0, "كلفة العمل": 6250},
        {"الفقرة": "صب أسس الخرسانة", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 0.5, "خصم": 0.0, "كلفة المواد": 71000, "كلفة العمل": 17500},
        {"الفقرة": "حديد التسليح", "الوحدة": "ton", "العدد": 1.0, "الطول": 1.0, "العرض": 1.0, "الارتفاع": 1.0, "خصم": 0.0, "كلفة المواد": 970000, "كلفة العمل": 150000},
        {"الفقرة": "بناء جدران الطابوق", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 0.24, "الارتفاع": 3.0, "خصم": 0.0, "كلفة المواد": 84000, "كلفة العمل": 25000},
        {"الفقرة": "اللبخ بالأسمنت", "الوحدة": "m2", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 3.0, "خصم": 0.0, "كلفة المواد": 2400, "كلفة العمل": 4000}
    ])

    # عرض جدول الإدخال التفاعلي
    st.markdown("#### 📝 أولاً: جدول إدخال الأبعاد")
    edited_df = st.data_editor(
        boq_initial,
        use_container_width=True,
        # قفلنا أعمدة الثوابت حتى لا تتعدل بالخطأ (فقط الأبعاد تتعدل)
        disabled=["الفقرة", "الوحدة", "كلفة المواد", "كلفة العمل"] 
    )

    # 2. الحسابات التلقائية (تتم برمجياً بدون تداخل بين الفقرات)
    final_rows = []
    grand_total = 0

    for index, row in edited_df.iterrows():
        # معادلة حساب الكمية تتغير حسب الوحدة
        if row["الوحدة"] in ["m3", "ton"]: 
            qty = (row["العدد"] * row["الطول"] * row["العرض"] * row["الارتفاع"]) - row["خصم"]
        elif row["الوحدة"] == "m2":
            qty = (row["العدد"] * row["الطول"] * row["الارتفاع"]) - row["خصم"]
        else:
            qty = (row["العدد"] * row["الطول"]) - row["خصم"]
            
        qty = max(0, qty) # لتجنب الأرقام السالبة
        
        mat_total = qty * row["كلفة المواد"]
        lab_total = qty * row["كلفة العمل"]
        total = mat_total + lab_total
        grand_total += total
        
        final_rows.append({
            "الفقرة": row["الفقرة"],
            "الكمية الصافية": round(qty, 2),
            "إجمالي المواد": f"{int(mat_total):,}",
            "إجمالي العمل": f"{int(lab_total):,}",
            "الكلفة الكلية": f"{int(total):,}"
        })

    # 3. عرض جدول النتائج النهائي
    st.markdown("#### 📊 ثانياً: جدول النتائج والكلف (يُحدّث آلياً)")
    st.dataframe(pd.DataFrame(final_rows), use_container_width=True)
    
    st.success(f"💰 الكلفة الإجمالية التقريبية للمشروع: {grand_total:,.0f} دينار عراقي")
