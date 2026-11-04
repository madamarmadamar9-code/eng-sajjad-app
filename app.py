import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. إعدادات الصفحة الشاملة
st.set_page_config(page_title="المنظومة الهندسية الشاملة - م. سجاد", layout="wide")

st.title("🏗️ المنظومة الهندسية الشاملة لحساب الكميات والتسعير والتنبؤ بالأسعار")
st.subheader("إعداد وإشراف: المهندس سجاد علي")
st.markdown("---")

# إنشاء التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs([
    "📐 1. حساب الكميات والأبعاد الهندسية", 
    "📋 2. جدول الكميات المجمع (BoQ) والتكلفة الكلية", 
    "📈 3. نشرة الأسعار العراقية (12 شهر) والتنبؤ الآلي"
])

# ---------------------------------------------------------
# التبويب الأول: حساب الكميات والأبعاد
# ---------------------------------------------------------
with tab1:
    st.header("أولاً: إدخال الأبعاد الهندسية وحساب الكميات التفصيلية")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.subheader("⛏️ 1. الحفر والأساسات")
        excav_len = st.number_input("طول موقع الحفر (متر)", min_value=1.0, value=15.0)
        excav_wid = st.number_input("عرض موقع الحفر (متر)", min_value=1.0, value=10.0)
        excav_dep = st.number_input("عمق الحفر (متر)", min_value=0.2, value=1.5)
        
        raft_thick = st.number_input("سمك خرسانة الأساس / الرافت (متر)", min_value=0.1, value=0.6)
        
    with col_b:
        st.subheader("🏛️ 2. الأعمدة والجسور والسقوف والستاير")
        cols_count = st.number_input("عدد الأعمدة (الدينك)", min_value=1, value=16)
        col_w = st.number_input("عرض العمود (متر)", value=0.3)
        col_l = st.number_input("طول العمود (متر)", value=0.4)
        col_h = st.number_input("ارتفاع العمود (متر)", value=3.2)
        
        roof_thick = st.number_input("سمك خرسانة السقف (متر)", min_value=0.1, value=0.2)
        parapet_height = st.number_input("ارتفاع الستارة السطحية (متر)", min_value=0.5, value=1.2)
        
    with col_c:
        st.subheader("🎨 3. البناء والإنهاءات والكهرباء")
        wall_height = st.number_input("ارتفاع الجدران صافي (متر)", min_value=1.0, value=3.2)
        tile_size = st.selectbox("قياس الكاشي/السيراميك", ["60x60 سم", "50x50 سم", "40x40 سم"])
        elec_points = st.number_input("عدد النقاط الكهربائية التقديري", min_value=5, value=45)
        sanitary_points = st.number_input("عدد التأسيسات الصحية", min_value=1, value=8)

    # *** الحسابات الهندسية الرياضية المباشرة ***
    # كميات الحفر والخرسانات
    excav_vol = excav_len * excav_wid * excav_dep # حجم الحفر م3
    raft_vol = excav_len * excav_wid * raft_thick # خرسانة الأساس م3
    cols_vol = cols_count * (col_w * col_l * col_h) # خرسانة الدينك م3
    roof_vol = excav_len * excav_wid * roof_thick # خرسانة السقف م3
    parapet_len = 2 * (excav_len + excav_wid)
    parapet_vol = parapet_len * 0.25 * parapet_height # خرسانة أو بناء الستارة م3
    
    total_concrete_vol = raft_vol + cols_vol + roof_vol + parapet_vol

    # حديد التسليح بالأقطار
    steel_12mm = total_concrete_vol * 35 / 1000.0  # طن (للأسقف والرباطات)
    steel_16mm = total_concrete_vol * 55 / 1000.0  # طن (للأعمدة والجسور)
    steel_25mm = total_concrete_vol * 30 / 1000.0  # طن (للأساسات)
    total_steel_tons = steel_12mm + steel_16mm + steel_25mm

    # الطابوق والإنهاءات
    wall_area = (2 * (excav_len + excav_wid)) * wall_height
    total_bricks = (wall_area * 450) + (parapet_len * parapet_height * 450) # عدد الطابوق الشامل
    
    plaster_area = wall_area * 2  # لبخ داخلي وخارجي
    paint_area = plaster_area      # صبغ للجدران
    floor_area = excav_len * excav_wid # مساحة الكاشي م2
    
    # حساب عدد الكاشي
    tile_area_m2 = 0.36 if tile_size == "60x60 سم" else (0.25 if tile_size == "50x50 سم" else 0.16)
    total_tiles_count = int(floor_area / tile_area_m2)

    st.markdown("---")
    st.success("✅ **تم حساب جميع الكميات الإنشائية والإنهاءات بنجاح!**")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("حجم الحفر الكلي", f"{excav_vol:.1f} م³")
    m2.metric("حجم الخرسانة الإجمالي", f"{total_concrete_vol:.1f} م³")
    m3.metric("حديد التسليح الإجمالي", f"{total_steel_tons:.2f} طن")
    m4.metric("عدد الكاشي المطلوب", f"{total_tiles_count:,} قطعة")

# ---------------------------------------------------------
# التبويب الثاني: BoQ والتكلفة الكلية
# ---------------------------------------------------------
with tab2:
    st.header("ثانياً: جدول الكميات المجمع (BoQ) وحساب الكلفة الكلية")
    
    # إدخال أسعار المواد المباشرة أو الاعتماد على الشهر
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("💵 أسعار الفقرات (يمكن تعديلها يدوياً)")
        p_excav = st.number_input("سعر حفر المتر المكعب (دينار)", value=8000)
        p_conc = st.number_input("سعر المتر المكعب للخرسانة الجاهزة (دينار)", value=110000)
        p_steel = st.number_input("معدل سعر طن حديد التسليح (دينار)", value=980000)
        p_brick = st.number_input("سعر ألف طابوقة (دينار)", value=180000)
        p_tile = st.number_input("سعر المتر المربع للكاشي (دينار)", value=14000)
        p_plaster = st.number_input("سعر م2 اللبخ والصبغ (دينار)", value=9000)
        p_elec = st.number_input("كلفة النقطة الكهربائية (دينار)", value=15000)
        p_sanitary = st.number_input("كلفة نقطة التأسيس الصحي (دينار)", value=35000)

    with col_p2:
        st.subheader("👷 طاقم العمالة والتشغيل")
        labor_option = st.radio("طريقة حساب أجور العمالة", ["نسبة مئوية من كلفة المواد", "حساب حسب أيام طاقم العمل"])
        if labor_option == "نسبة مئوية من كلفة المواد":
            labor_pct = st.number_input("نسبة أجور العمل والآليات (%)", min_value=5.0, value=22.0)
            custom_labor = None
        else:
            days = st.number_input("عدد أيام تنفيذ المشروع المتوقعة", value=60)
            daily_cost = st.number_input("كلفة طاقم العمالة اليومية (دينار)", value=180000)
            custom_labor = days * daily_cost

    # حساب التكاليف لكل فقرة
    cost_excav = excav_vol * p_excav
    cost_conc = total_concrete_vol * p_conc
    cost_steel = total_steel_tons * p_steel
    cost_brick = (total_bricks / 1000.0) * p_brick
    cost_tile = floor_area * p_tile
    cost_plaster = plaster_area * p_plaster
    cost_elec = elec_points * p_elec
    cost_sanitary = sanitary_points * p_sanitary

    total_mat_cost = cost_excav + cost_conc + cost_steel + cost_brick + cost_tile + cost_plaster + cost_elec + cost_sanitary
    
    if custom_labor is not None:
        labor_cost = custom_labor
    else:
        labor_cost = total_mat_cost * (labor_pct / 100.0)

    grand_total_cost = total_mat_cost + labor_cost

    # بناء جدول الكميات BoQ المتكامل
    boq_data = {
        "ت": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "فقرة العمل": [
            "أعمال الحفر والتأسيس",
            "الخرسانة المسلحة (أساس + أعمدة + سقف + ستارة)",
            f"حديد التسليح (12mm: {steel_12mm:.1f}t | 16mm: {steel_16mm:.1f}t | 25mm: {steel_25mm:.1f}t)",
            "البناء بالطابوق المحلي للجدران والستارة",
            f"تغليف الأرضيات بالكاشي ({tile_size})",
            "أعمال اللبخ والصبغ الداخلي والخارجي",
            "التأسيسات الكهربائية",
            "التأسيسات الصحية والسباكة",
            "أجور طاقم العمالة والتشغيل والآليات"
        ],
        "الكمية": [
            f"{excav_vol:.1f} م³",
            f"{total_concrete_vol:.1f} م³",
            f"{total_steel_tons:.2f} طن",
            f"{total_bricks:,.0f} طابوقة",
            f"{floor_area:.1f} م² ({total_tiles_count:,} قطعة)",
            f"{plaster_area:.1f} م²",
            f"{elec_points} نقطة",
            f"{sanitary_points} نقطة",
            "شامل التنفيذ"
        ],
        "السعر المفرد (دينار)": [f"{p_excav:,}", f"{p_conc:,}", f"{p_steel:,}", f"{p_brick:,}", f"{p_tile:,}", f"{p_plaster:,}", f"{p_elec:,}", f"{p_sanitary:,}", "-"],
        "الكلفة الإجمالية (دينار)": [
            f"{cost_excav:,.0f}", f"{cost_conc:,.0f}", f"{cost_steel:,.0f}", 
            f"{cost_brick:,.0f}", f"{cost_tile:,.0f}", f"{cost_plaster:,.0f}", 
            f"{cost_elec:,.0f}", f"{cost_sanitary:,.0f}", f"{labor_cost:,.0f}"
        ]
    }

    st.markdown("### 📜 جدول الكميات الشامل والنهائي للمشروع (BoQ)")
    st.table(pd.DataFrame(boq_data))
    
    st.markdown("---")
    st.metric("🏆 الكلفة الإجمالية التقديرية الكاملة للمشروع", f"{grand_total_cost:,.0f} دينار عراقي")

# ---------------------------------------------------------
# التبويب الثالث: نشرة الأسعار والتنبؤ
# ---------------------------------------------------------
with tab3:
    st.header("ثالثاً: نشرة الأسعار العراقية (12 شهراً) والتنبؤ الذكي للربع الأخير")
    
    selected_mat = st.selectbox("اختر المادة للتحليل والتنبؤ", ["حديد التسليح (طن)", "الخرسانة الجاهزة (م3)", "الطابوق (ألف)"])
    
    # أشهر السنة الـ 12
    all_months = ["شهر 1", "شهر 2", "شهر 3", "شهر 4", "شهر 5", "شهر 6", "شهر 7", "شهر 8", "شهر 9", "شهر 10 (تنبؤ)", "شهر 11 (تنبؤ)", "شهر 12 (تنبؤ)"]
    
    # بيانات النشرة لـ 9 أشهر فعلية
    months_num = np.arange(1, 10)
    if selected_mat == "حديد التسليح (طن)":
        actual_prices = [910000, 920000, 915000, 930000, 945000, 950000, 960000, 970000, p_steel]
    elif selected_mat == "الخرسانة الجاهزة (م3)":
        actual_prices = [102000, 104000, 105000, 105000, 108000, 108000, 110000, 110000, p_conc]
    else:
        actual_prices = [160000, 162000, 165000, 168000, 170000, 172000, 175000, 178000, p_brick]

    # خوارزمية التنبؤ للأشهر 10 و 11 و 12
    poly = np.polyfit(months_num, actual_prices, 1)
    future_months_num = np.array([10, 11, 12])
    pred_prices = np.polyval(poly, future_months_num)

    full_prices = list(actual_prices) + list(pred_prices)
    types = ["أسعار مسجلة بالشرة"] * 9 + ["تنبؤ ذكي (مستقبلي)"] * 3

    df_price_chart = pd.DataFrame({
        "الشهر": all_months,
        "السعر (دينار)": full_prices,
        "نوع السعر": types
    })

    # رسم المخطط التفاعلي
    fig = px.line(
        df_price_chart, x="الشهر", y="السعر (دينار)", color="نوع السعر",
        title=f"📈 المسار السعري ونسبة التنبؤ لمادة {selected_mat} على مدار 12 شهراً",
        markers=True, line_shape="spline"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🗓️ جدول نشرة الأسعار المعتمدة (12 شهر)")
    st.dataframe(df_price_chart.T)
