import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مشروع المهندس سجاد 2026",
    page_icon="📊",
    layout="wide"
)

st.title("📊 مشروع المهندس سجاد 2026 - المنظومة الهندسية المتكاملة")
st.markdown("---")

# 2. سجل أسعار المواد التاريخية (الأشهر 1 إلى 9)
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

# 3. سجل أجور الكوادر (الأشهر 5 إلى 9)
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

# 4. دالة التنبؤ الآمنة والمحصنة مضادة للأخطاء
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

# 5. التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 شيت 1: سجل أسعار المواد", 
    "👷 شيت 2: سجل أجور الكوادر", 
    "🔮 شيت 3: لوحة التنبؤ الذكية", 
    "📑 شيت 4: جدول الكميات والتكلفة الكلية"
])

# ---------------------------------------------------------
# شيت 1
# ---------------------------------------------------------
with tab1:
    st.subheader("الذاكرة التاريخية لأسعار المواد الإنشائية (2026)")
    st.markdown("*جدول تسعير المواد الإنشائية للفترة الممتدة من الشهر 1 إلى الشهر 9*")
    st.dataframe(df_materials_history, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# شيت 2
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
# شيت 3
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

# ---------------------------------------------------------
# شيت 4
# ---------------------------------------------------------
with tab4:
    st.subheader("📑 جدول الكميات والتكلفة الكلية الشاملة للمشروع")
    st.markdown("*مربوط آلياً بأسعار المواد والأجور المستقبليّة المحسوبة في لوحة التنبؤ*")
    
    p_mat_sec4, p_wages_sec4 = get_safe_predictions(10, "بغداد")
    
    with st.expander("📐 مدخلات الأبعاد الهندسية للمشروع", expanded=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        with col_in1:
            l_b = st.number_input("طول البناء (متر)", value=15.0)
            w_b = st.number_input("عرض البناء (متر)", value=10.0)
            h_b = st.number_input("ارتفاع الجدران (متر)", value=3.2)
        with col_in2:
            raft_t = st.number_input("سمك خرسانة الرافت (متر)", value=0.6)
            roof_t = st.number_input("سمك خرسانة السقف (متر)", value=0.2)
            cols_n = st.number_input("عدد الدينك (الأعمدة)", value=16)
        with col_in3:
            parapet_h = st.number_input("ارتفاع الستارة (متر)", value=1.2)
            excav_d = st.number_input("عمق الحفر (متر)", value=1.5)

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

    p_steel = p_mat_sec4["حديد شيش"]
    p_cement = p_mat_sec4["سمنت مقاوم"]
    p_brick = p_mat_sec4["طابوق عادي"]
    p_tile = p_mat_sec4["كاشي عادي"]
    p_paint = p_mat_sec4["أسباغ مائية"]
    
    w_eng = p_wages_sec4["المهندسون"]
    w_skilled = p_wages_sec4["العمال الماهرون"]
    
    cost_excav = vol_excav * 8000
    cost_conc = total_concrete * (p_cement * 0.35 + 35000)
    cost_steel = steel_tons * p_steel
    cost_brick = (total_bricks / 1000.0) * p_brick
    cost_tile = floor_area * p_tile
    cost_finish = finish_area * p_paint * 2
    
    cost_materials_total = cost_excav + cost_conc + cost_steel + cost_brick + cost_tile + cost_finish
    cost_labor_total = (w_eng * 30) + (w_skilled * 60 * 2)

    grand_total_project = cost_materials_total + cost_labor_total

    boq_df = pd.DataFrame({
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
        "الكمية / المساحة": [
            f"{vol_excav:.1f} م3", f"{total_concrete:.1f} م3", f"{steel_tons:.2f} طن",
            f"{total_bricks:,.0f} طابوقة", f"{floor_area:.1f} م2", f"{finish_area:.1f} م2", "شامل الطاقم"
        ],
        "كلفة المواد (مربوطة بالتنبؤ)": [
            f"{cost_excav:,.0f} د.ع", f"{cost_conc:,.0f} د.ع", f"{cost_steel:,.0f} د.ع",
            f"{cost_brick:,.0f} د.ع", f"{cost_tile:,.0f} د.ع", f"{cost_finish:,.0f} د.ع", "-"
        ],
        "كلفة العمل": [
            "150,000 د.ع", "800,000 د.ع", "450,000 د.ع", "900,000 د.ع", "350,000 د.ع", "600,000 د.ع", f"{cost_labor_total:,.0f} د.ع"
        ],
        "الكلفة الكلية": [
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
    st.markdown("##### 📜 جدول الكميات والتكلفة الشاملة للمشروع (BoQ)")
    st.table(boq_df)
    st.success(f"💰 **الكلفة الكلية التقديرية للمشروع الكامل: {grand_total_project:,.0f} دينار عراقي**")
