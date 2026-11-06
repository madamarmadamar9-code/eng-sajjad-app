import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="مشروع المهندس سجاد 2026", page_icon="logo.jpg", layout="wide")

# إبقاء اللوكو بحجم كبير وواضح
st.image("logo.jpg", width=400)

st.title("📊 مشروع المهندس سجاد 2026 - المنظومة الهندسية المتكاملة")
st.markdown("##### 👨‍🏫 إشراف: الأستاذ علي خليل | 💻 إعداد وبرمجة: المهندس سجاد وفريق العمل")
st.markdown("---")

# ==========================================
# تحميل البيانات
# ==========================================
@st.cache_data
def load_base_data():
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
    df_mat = pd.DataFrame(data_materials)
    mat_list = [c for c in df_mat.columns if c != "الشهر"]

    provs = ["بغداد", "البصرة", "النجف", "كربلاء", "أربيل", "سليمانية", "دهوك", "بابل", "ذي قار", "ميسان", "المثنى", "الديوانية", "واسط", "ديالى", "صلاح الدين", "كركوك", "الانبار", "نينوى"]
    w_list = []
    for m in range(1, 10):
        for idx, p in enumerate(provs):
            w_list.append({
                "الشهر": m,
                "المحافظة": p,
                "المهندسون": 60000 + (m * 1000) + (idx * 500),
                "العمال الماهرون": 40000 + (m * 500) + (idx * 300),
                "العمال شبه الماهرين": 30000 + (m * 400) + (idx * 200),
                "العمال غير الماهرين": 20000 + (m * 300) + (idx * 100)
            })
    df_w = pd.DataFrame(w_list)
    return df_mat, df_w, mat_list, provs

df_materials_history, df_wages_history, materials_list, provinces = load_base_data()

@st.cache_data 
def get_safe_predictions(t_month, t_prov):
    months_num = np.array(df_materials_history["الشهر"].values)
    pred_mat = {}
    for mat in materials_list:
        prices = df_materials_history[mat].values
        poly = np.polyfit(months_num, prices, 1)
        pred_mat[mat] = max(0, round(float(np.polyval(poly, t_month)), 0))
        
    prov_df = df_wages_history[df_wages_history["المحافظة"] == t_prov]
    if prov_df.empty: prov_df = df_wages_history[df_wages_history["المحافظة"] == "بغداد"]
        
    months_w = np.array(prov_df["الشهر"].values)
    pred_w = {}
    roles = ["المهندسون", "العمال الماهرون", "العمال شبه الماهرين", "العمال غير الماهرين"]
    for r in roles:
        w_vals = prov_df[r].values
        poly_w = np.polyfit(months_w, w_vals, 1)
        pred_w[r] = max(0, round(float(np.polyval(poly_w, t_month)), 0))
        
    return pred_mat, pred_w

# ==========================================
# واجهة التبويبات
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 شيت 1: سجل أسعار المواد", 
    "👷 شيت 2: سجل أجور الكوادر", 
    "🔮 شيت 3: لوحة التنبؤ والرسوم", 
    "📑 شيت 4: جدول الكميات الشامل"
])

with tab1:
    st.subheader("الذاكرة التاريخية لأسعار المواد الإنشائية (2026)")
    st.dataframe(df_materials_history, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("الذاكرة التاريخية لأجور الكوادر (2026)")
    sel_prov = st.selectbox("تصفية العرض حسب المحافظة:", ["جميع المحافظات"] + provinces)
    if sel_prov != "جميع المحافظات":
        st.dataframe(df_wages_history[df_wages_history["المحافظة"] == sel_prov], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_wages_history, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🔮 لوحة التنبؤ الذكية والتحليل البياني")
    col1, col2 = st.columns(2)
    with col1:
        target_month = st.selectbox("اختر رقم الشهر المستهدف للتنبؤ:", [10, 11, 12], index=0)
    with col2:
        target_province = st.selectbox("اختر المحافظة للتنبؤ:", provinces, index=0)
        
    pred_mat_dict, pred_wages_dict = get_safe_predictions(target_month, target_province)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"##### أسعار المواد المتوقعة (شهر {target_month})")
        df_p_mat = pd.DataFrame({"المادة الإنشائية": list(pred_mat_dict.keys()), "السعر المتوقع": [f"{v:,.0f}" for v in pred_mat_dict.values()]})
        st.dataframe(df_p_mat, use_container_width=True, hide_index=True)
    with c2:
        st.markdown(f"##### أجور الكوادر المتوقعة ({target_province})")
        df_p_wages = pd.DataFrame({"الكوادر": list(pred_wages_dict.keys()), "الأجرة المتوقعة": [f"{v:,.0f}" for v in pred_wages_dict.values()]})
        st.dataframe(df_p_wages, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 📈 المسار البياني للأسعار")
    chart_item = st.selectbox("اختر المادة لرسم مسارها الزمني:", materials_list, index=0)
    hist_prices = list(df_materials_history[chart_item].values)
    pred_price = pred_mat_dict[chart_item]
    x_months = [f"شهر {i}" for i in range(1, 10)] + [f"شهر {target_month}"]
    y_prices = hist_prices + [pred_price]
    df_chart = pd.DataFrame({"الشهر": x_months, "السعر (دينار)": y_prices})
    fig = px.line(df_chart, x="الشهر", y="السعر (دينار)", title=f"المسار الزمني لأسعار: {chart_item}", markers=True)
    fig.update_traces(line_color='#176B87', marker=dict(size=8, color='#053B50'))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# الشيت الرابع: جدول الكميات (النسخة الفائقة السرعة)
# ==========================================
with tab4:
    st.markdown("### 📋 جدول الكميات والتكلفة الشامل لجميع مراحل العمل")

    c_m, c_p = st.columns(2)
    with c_m:
        selected_month_b = st.selectbox("اختر شهر التسعير المرجعي (1-12):", list(range(1, 13)), index=0, key="boq_month") 
    with c_p:
        selected_prov_b = st.selectbox("اختر المحافظة لتسعير العمل:", provinces, index=0, key="boq_prov")

    # جدول الإدخال فقط (بدون أسعار، علمود يكون سريع جداً وميعلق)
    boq_inputs_only = pd.DataFrame([
        {"الفقرة": "حفر الأسس الترابية", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 1.0, "خصم": 0.0},
        {"الفقرة": "صب أسس خرسانة", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 0.5, "خصم": 0.0},
        {"الفقرة": "بناء جدران طابوق", "الوحدة": "m3", "العدد": 1.0, "الطول": 10.0, "العرض": 0.24, "الارتفاع": 3.0, "خصم": 0.0},
        {"الفقرة": "سقف خرسانة مسلحة", "الوحدة": "m3", "العدد": 1.0, "الطول": 5.0, "العرض": 4.0, "الارتفاع": 0.2, "خصم": 0.0},
        {"الفقرة": "تطبيق أرضيات كاشي", "الوحدة": "m2", "العدد": 1.0, "الطول": 5.0, "العرض": 4.0, "الارتفاع": 0.0, "خصم": 0.0},
        {"الفقرة": "تطبيق أرضيات مرمر", "الوحدة": "m2", "العدد": 1.0, "الطول": 4.0, "العرض": 4.0, "الارتفاع": 0.0, "خصم": 0.0},
        {"الفقرة": "تطبيق سيراميك جدران", "الوحدة": "m2", "العدد": 1.0, "الطول": 4.0, "العرض": 1.0, "الارتفاع": 2.0, "خصم": 0.0},
        {"الفقرة": "بياض جص/بورك داخلي", "الوحدة": "m2", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 3.0, "خصم": 0.0},
        {"الفقرة": "لبخ بالأسمنت خارجي", "الوحدة": "m2", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 3.0, "خصم": 0.0},
        {"الفقرة": "أصباغ مائية جدران", "الوحدة": "m2", "العدد": 1.0, "الطول": 10.0, "العرض": 1.0, "الارتفاع": 3.0, "خصم": 0.0},
        {"الفقرة": "تركيب زجاج", "الوحدة": "m2", "العدد": 1.0, "الطول": 2.0, "العرض": 2.0, "الارتفاع": 0.0, "خصم": 0.0}
    ])

    st.markdown("#### 📝 أولاً: أدخل الأبعاد والكميات هنا (اكتب براحتك بدون أي تعليق)")
    with st.form("boq_form"):
        # مفتاح ثابت يمنع المتصفح من إعادة تحميل الجدول كل ثانية
        user_edited_df = st.data_editor(boq_inputs_only, use_container_width=True, disabled=["الفقرة", "الوحدة"], key="static_editor")
        submit_calc = st.form_submit_button("إحسب الكلفة النهائية 🧮", use_container_width=True)

    # الحساب يتم فقط عند الضغط على الزر، مما يلغي التعليق تماماً
    if submit_calc:
        if selected_month_b <= 9:
            mat_row = df_materials_history[df_materials_history["الشهر"] == selected_month_b].iloc[0]
            wage_row = df_wages_history[(df_wages_history["الشهر"] == selected_month_b) & (df_wages_history["المحافظة"] == selected_prov_b)].iloc[0]
            c_cement, c_gravel, c_sand, c_steel, c_brick = mat_row["سمنت مقاوم"], mat_row["حصى مكسر"], mat_row["رمل أسود"], mat_row["حديد شيش"], mat_row["طابوق عادي"]
            c_borak, c_kashi, c_marmar, c_ceramic = mat_row["بورك"], mat_row["كاشي عادي"], mat_row["مرمر"], mat_row["سيراميك"]
            c_paint, c_glass = mat_row["أسباغ مائية"], mat_row["زجاج"]
            w_skilled, w_unskilled, w_eng = wage_row["العمال الماهرون"], wage_row["العمال غير الماهرين"], wage_row["المهندسون"]
        else:
            pm_dict, pw_dict = get_safe_predictions(selected_month_b, selected_prov_b)
            c_cement, c_gravel, c_sand, c_steel, c_brick = pm_dict["سمنت مقاوم"], pm_dict["حصى مكسر"], pm_dict["رمل أسود"], pm_dict["حديد شيش"], pm_dict["طابوق عادي"]
            c_borak, c_kashi, c_marmar, c_ceramic = pm_dict["بورك"], pm_dict["كاشي عادي"], pm_dict["مرمر"], pm_dict["سيراميك"]
            c_paint, c_glass = pm_dict["أسباغ مائية"], pm_dict["زجاج"]
            w_skilled, w_unskilled, w_eng = pw_dict["العمال الماهرون"], pw_dict["العمال غير الماهرين"], pw_dict["المهندسون"]

        costs_map = {
            "حفر الأسس الترابية": {"mat": 0, "lab": w_unskilled / 3.5},
            "صب أسس خرسانة": {"mat": (c_cement * 0.35) + (c_gravel * 0.8) + (c_sand * 0.4), "lab": w_skilled / 2.5},
            "بناء جدران طابوق": {"mat": (c_brick * 0.4) + (c_cement * 0.08) + (c_sand * 0.2), "lab": w_skilled / 1.7},
            "سقف خرسانة مسلحة": {"mat": ((c_cement * 0.35) + (c_gravel * 0.8) + (c_sand * 0.4)) + (c_steel * 0.1), "lab": (w_skilled + w_eng * 0.2) / 2.0},
            "تطبيق أرضيات كاشي": {"mat": c_kashi + (c_cement * 0.01) + (c_sand * 0.02), "lab": w_skilled / 15},
            "تطبيق أرضيات مرمر": {"mat": c_marmar + (c_cement * 0.015) + (c_sand * 0.03), "lab": w_skilled / 8},
            "تطبيق سيراميك جدران": {"mat": c_ceramic + (c_cement * 0.01), "lab": w_skilled / 12},
            "بياض جص/بورك داخلي": {"mat": c_borak * 0.02, "lab": w_skilled / 20},
            "لبخ بالأسمنت خارجي": {"mat": (c_cement * 0.015) + (c_sand * 0.03), "lab": w_skilled / 10},
            "أصباغ مائية جدران": {"mat": c_paint * 0.2, "lab": w_skilled / 25},
            "تركيب زجاج": {"mat": c_glass, "lab": w_skilled / 20}
        }

        final_rows = []
        grand_total = 0

        for index, row in user_edited_df.iterrows():
            if row["الوحدة"] in ["m3", "ton"]: 
                qty = (row["العدد"] * row["الطول"] * row["العرض"] * row["الارتفاع"]) - row["خصم"]
            elif row["الوحدة"] == "m2":
                val1 = row["الطول"] if row["الطول"] > 0 else 1
                val2 = row["العرض"] if row["العرض"] > 0 else 1
                val3 = row["الارتفاع"] if row["الارتفاع"] > 0 else 1
                qty = (row["العدد"] * val1 * (val3 if row["الارتفاع"] > 0 else val2)) - row["خصم"]
            else:
                qty = (row["العدد"] * row["الطول"]) - row["خصم"]
                
            qty = max(0, qty)
            mat_cost_unit = costs_map[row["الفقرة"]]["mat"]
            lab_cost_unit = costs_map[row["الفقرة"]]["lab"]
            
            mat_total = qty * mat_cost_unit
            lab_total = qty * lab_cost_unit
            total = mat_total + lab_total
            grand_total += total
            
            final_rows.append({
                "الفقرة": row["الفقرة"],
                "الكمية الصافية": round(qty, 2),
                "كلفة المواد للوحدة": f"{int(mat_cost_unit):,}",
                "كلفة العمل للوحدة": f"{int(lab_cost_unit):,}",
                "إجمالي كلفة المواد": f"{int(mat_total):,}",
                "إجمالي كلفة العمل": f"{int(lab_total):,}",
                "الكلفة الكلية": f"{int(total):,}"
            })

        st.markdown("#### 📊 ثانياً: جدول النتائج والكلف النهائية")
        st.dataframe(pd.DataFrame(final_rows), use_container_width=True)
        st.success(f"💰 الكلفة الإجمالية للمشروع لشهر ({selected_month_b}) في ({selected_prov_b}): {grand_total:,.0f} دينار عراقي")
