import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم
# ---------------------------------------------------------
st.set_page_config(
    page_title="مشروع المهندس سجاد 2026 | المنظومة الهندسية",
    page_icon="📊",
    layout="wide"
)

st.title("📊 مشروع المهندس سجاد 2026 - المنظومة الهندسية المتكاملة")
st.markdown("---")

# ---------------------------------------------------------
# 2. إنشاء قاعدة البيانات التاريخية (المواد والأجور)
# ---------------------------------------------------------

# قائمة المواد الإنشائية الأساسية
materials_list = ["طابوق عادي", "سمنت مقاوم", "حديد شيش", "رمل أسود", "حصى مكسر", "بورك", "كاشي عادي", "مرمر", "سيراميك", "أسباغ مائية", "زجاج"]

# سجل أسعار المواد التاريخية (الأشهر من 1 إلى 9)
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

# سجل أجور الكوادر للأشهر (من 5 إلى 9) وحسب المحافظات
provinces = ["بغداد", "البصرة", "النجف الأشرف", "كربلاء المقدسة", "أربيل", "سليمانية", "دهوك", "بابل", "ذي قار", "ميسان", "المثنى", "الديوانية", "واسط", "ديالى", "صلاح الدين", "كركوك", "الانبار", "نينوى"]

wages_data = []
np.random.seed(42)
for month in range(5, 10):
    for prov in provinces:
        wages_data.append({
            "الشهر": month,
            "المحافظة": prov,
            "المهندسون": int(np.random.choice([50000, 55000, 60000, 65000, 70000, 75000])),
            "العمال الماهرون": int(np.random.choice([35000, 40000, 45000, 50000])),
            "العمال شبه الماهرين": int(np.random.choice([25000, 30000, 35000])),
            "العمال غير الماهرين": int(np.random.choice([15000, 20000, 25000]))
        })
df_wages_history = pd.DataFrame(wages_data)

# ---------------------------------------------------------
# 3. تبويبات النظام (طراز الشيتات)
# ---------------------------------------------------------
tab_sheet1, tab_sheet2, tab_sheet3, tab_sheet4 = st.tabs([
    "📋 شيت 1: سجل أسعار المواد التاريخية", 
    "👷 شيت 2: سجل أجور الكوادر والعمال", 
    "🔮 شيت 3: لوحة التنبؤ الذكية والتحليل البياني", 
    "📑 شيت 4: جدول الكميات والتكلفة الكلية الشاملة"
])

# ---------------------------------------------------------
# الشيت الأول: سجل أسعار المواد
# ---------------------------------------------------------
with tab_sheet1:
    st.subheader("الذاكرة التاريخية لأسعار المواد الإنشائية (2026)")
    st.markdown("*جدول تسعير المواد الإنشائية للفترة الممتدة من الشهر 1 إلى الشهر 9*")
    st.dataframe(df_materials_history, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# الشيت الثاني: سجل أجور الكوادر
# ---------------------------------------------------------
with tab_sheet2:
    st.subheader("الذاكرة التاريخية لأجور الكوادر (أيول - أيلول 2026)")
    st.markdown("*جدول اليوميات والكوادر الهندسية والفنية والعمالة للأشهر من 5 إلى 9 مخصصة حسب المحافظة*")
    
    selected_prov_filter = st.selectbox("تصفية حسب المحافظة:", ["الكل"] + provinces)
    if selected_prov_filter != "الكل":
        filtered_wages = df_wages_history[df_wages_history["المحافظة"] == selected_prov_filter]
    else:
        filtered_wages = df_wages_history
        
    st.dataframe(filtered_wages, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# الشيت الثالث: لوحة التنبؤ الذكية
# ---------------------------------------------------------
with tab_sheet3:
    st.subheader("🔮 لوحة التنبؤ الذكية (المواد والأجور)")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        target_month = st.selectbox("اختر رقم الشهر المستهدف بالتنبؤ:", [10, 11, 12], index=0)
    with col_sel2:
        target_province = st.selectbox("اختر المحافظة لتقدير الأجور:", provinces, index=0)
        
    st.markdown("---")
    
    col_t1, col_t2 = st.columns(2)
    
    # تنبؤ أسعار المواد
    pred_materials_dict = {}
    months_num = np.arange(1, 10)
    for mat in materials_list:
        prices = df_materials_history[mat].values
        poly = np.polyfit(months_num, prices, 1)
        pred_val = np.polyval(poly, target_month)
        pred_materials_dict[mat] = round(float(pred_val), 0)
        
    with col_t1:
        st.markdown("##### أولاً: التنبؤ بأسعار المواد الإنشائية")
        df_pred_mat = pd.DataFrame({
            "المادة الإنشائية": list(pred_materials_dict.keys()),
            f"السعر المتوقع (شهر {target_month})": [f"{v:,.0f} د.ع" for v in pred_materials_dict.values()],
            "حالة السوق المتوقعة": ["استقرار نسبياً" if i % 2 == 0 else "ارتفاع خفيف" for i in range(len(materials_list))]
        })
        st.dataframe(df_pred_mat, use_container_width=True, hide_index=True)
        
    # تنبؤ أجور الكوادر
    with col_t2:
        st.markdown(f"##### ثانياً: أجور الكوادر المتوقعة ({target_province})")
        prov_wages = df_wages_history[df_wages_history["المحافظة"] == target_province]
        months_wages = prov_wages["الشهر"].values
        
        pred_wages_dict = {}
        roles = ["المهندسون", "العمال الماهرين", "العمال شبه الماهرين", "العمال غير الماهرين"]
        for role in roles:
            w_vals = prov_wages[role].values
            poly_w = np.polyfit(months_wages, w_vals, 1)
            pred_w = np.polyval(poly_w, target_month)
            pred_wages_dict[role] = round(float(pred_w), 0)
            
        df_pred_wages = pd.DataFrame({
            "الكوادر": list(pred_wages_dict.keys()),
            f"الأجرة المتوقعة (شهر {target_month})": [f"{v:,.0f} د.ع" for v in pred_wages_dict.values()],
            "حالة السوق": ["مستقر", "مستقر", "ارتفاع طفيف", "مستقر"]
        })
        st.dataframe(df_pred_wages, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 📈 المسار الزمني والمؤشر البياني للتنبؤ")
    selected_chart_mat = st.selectbox("اختر عنصر إنشائي أو مادة لرسم التحليل الزمني:", materials_list, index=0)
    
    history_p = list(df_materials_history[selected_chart_mat].values)
    pred_p = pred_materials_dict[selected_chart_mat]
    
    chart_months = [f"شهر {i}" for i in range(1, 10)] + [f"شهر {target_month} (تنبؤ)"]
    chart_values = history_p + [pred_p]
    chart_types = ["أسعار مسجلة"] * 9 + ["تنبؤ ذكي"]
    
    df_chart = pd.DataFrame({
        "الشهر": chart_months,
        "السعر (دينار)": chart_values,
        "النوع": chart_types
    })
    
    fig = px.line(df_chart, x="الشهر", y="السعر (دينار)", color="النوع", title=f"المسار الزمني وتنبؤ أسعار {selected_chart_mat}", markers=True, line_shape="spline")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# الشيت الرابع: جدول الكميات والتكلفة الشاملة للمشروع
# ---------------------------------------------------------
with tab_sheet4:
    st.subheader("📑 جدول الكميات والكلفة الشامل (مربوط آلياً بالأسعار والأجور المستقبليّة)")
    
    with st.expander("📐 مدخلات الأبعاد الهندسية للمشروع", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            l_b = st.number_input("طول البناء (متر)", value=15.0)
            w_b = st.number_input("عرض البناء (متر)", value=10.0)
            h_b = st.number_input("ارتفاع السقف (متر)", value=3.2)
        with c2:
            raft_t = st.number_input("سمك خرسانة الرافت (متر)", value=0.6)
            roof_t = st.number_input("سمك الخرسانة المسلحة للسقف (متر)", value=0.2)
            cols_n = st.number_input("عدد الدينك (الأعمدة)", value=16)
        with c3:
            parapet_h = st.number_input("ارتفاع الستارة (متر)", value=1.2)
            excav_d = st.number_input("عمق الحفر (متر)", value=1.5)

    # الحسابات الرياضية المباشرة
    vol_excav = l_b * w_b * excav_d
    vol_raft = l_b * w_b * raft_t
    vol_cols = cols_n * (0.3 * 0.4 * h_b)
    vol_roof = l_b * w_b * roof_t
    vol_parapet = (2 * (l_b + w_b)) * 0.25 * parapet_h
    total_concrete = vol_raft + vol_cols + vol_roof + vol_parapet
    
    steel_tons = (total_concrete * 120) / 1000.0
    wall_area = (2 * (l_b + w_b)) * h_b
    total_bricks = (wall_area * 450) + ((2 * (l_b + w_b)) * parapet_h * 450)
    finish_area = wall_area * 2
    floor_area = l_b * w_b

    # ربط الكلف بالأسعار والأجور المتوقعة للشهر والمحافظة المحضرة في شيت 3
    p_steel = pred_materials_dict["حديد شيش"]
    p_cement = pred_materials_dict["سمنت مقاوم"]
    p_brick = pred_materials_dict["طابوق عادي"]
    p_tile = pred_materials_dict["كاشي عادي"]
    p_paint = pred_materials_dict["أسباغ مائية"]
    
    w_eng = pred_wages_dict["المهندسون"]
    w_skilled = pred_wages_dict["العمال الماهرين"]
    
    cost_excav = vol_excav * 8000
    cost_conc = total_concrete * (p_cement * 0.35 + 30000)
    cost_steel = steel_tons * p_steel
    cost_brick = (total_bricks / 1000.0) * p_brick
    cost_tile = floor_area * p_tile
    cost_finish = finish_area * p_paint * 2
    
    cost_materials_total = cost_excav + cost_conc + cost_steel + cost_brick + cost_tile + cost_finish
    cost_labor_total = (w_eng * 30) + (w_skilled * 60 * 3) # تقدير العمل لمرحلة المشروع

    grand_total_project = cost_materials_total + cost_labor_total

    boq_master = pd.DataFrame({
        "ت": [1, 2, 3, 4, 5, 6, 7],
        "مرحلة العمل": [
            "حفر الأساسات والتأسيس",
            "صب الخرسانة المسلحة (أساس + أعمدة + سقف)",
            f"حديد التسليح الإجمالي ({steel_tons:.2f} طن)",
            "البناء بالطابوق للجدران والستارة",
            "تغليف الأرضيات بالكاشي",
            "اللبخ والصبغ والإنهاءات",
            "أجور الكوادر الهندسية والعمالة"
        ],
        "العدد / الكمية / الطول": [
            f"{vol_excav:.1f} م3", f"{total_concrete:.1f} م3", f"{steel_tons:.2f} طن",
            f"{total_bricks:,.0f} طابوقة", f"{floor_area:.1f} م2", f"{finish_area:.1f} م2", "شامل الطاقم"
        ],
        "كلفة المواد (مربوط آلياً)": [
            f"{cost_excav:,.0f} د.ع", f"{cost_conc:,.0f} د.ع", f"{cost_steel:,.0f} د.ع",
            f"{cost_brick:,.0f} د.ع", f"{cost_tile:,.0f} د.ع", f"{cost_finish:,.0f} د.ع", "-"
        ],
        "كلفة العمل (مستقلة)": [
            "150,000 د.ع", "800,000 د.ع", "450,000 د.ع", "900,000 د.ع", "350,000 د.ع", "600,000 د.ع", f"{cost_labor_total:,.0f} د.ع"
        ],
        "الكلفة الكلية المتوقعة": [
            f"{cost_excav + 150000:,.0f} د.ع",
            f"{cost_conc + 800000:,.0f} د.ع",
            f"{cost_steel + 450000:,.0f} د.ع",
            f"{cost_brick + 900000:,.0f} د.ع",
            f"{cost_tile + 350000:,.0f} د.ع",
            f"{cost_finish + 600000:,.0f} د.ع",
            f"{cost_labor_total:,.0f} د.ع"
        ]
    })

    st.markdown("---")
    st.markdown("##### 🏆 جدول الكميات والتكلفة الكلية الشاملة للمشروع")
    st.table(boq_master)
    
    st.success(f"💰 **الكلفة الإجمالية التقديرية للمشروع الكامل (مربوطة بالتنبؤ المستقبلي): {grand_total_project:,.0f} دينار عراقي**")
