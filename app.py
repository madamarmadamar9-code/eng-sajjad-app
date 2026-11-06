import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(
    page_title="مشروع المهندس سجاد 2026 - المنظومة المتكاملة",
    page_icon="logo.jpg",
    layout="wide"
)

# 2. إظهار اللوجو والعنوان
st.image("logo.jpg", use_container_width=True)
st.title("📊 مشروع المهندس سجاد 2026 - المنظومة الهندسية المتكاملة")
st.markdown("##### 👨‍🏫 إشراف: الأستاذ علي خليل | 💻 إعداد وبرمجة: المهندس سجاد وفريق العمل")
st.markdown("---")

# 3. إنشاء الشيتات الأربعة
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 البيانات التاريخية لأسعار المواد",
    "👷 البيانات التاريخية لأجور العمال",
    "📊 التحليلات والرسوم البيانية",
    "📋 الشيت الرابع: جدول الكميات والتكلفة الشامل"
])

# ==========================================
# 🟢 الشيت الأول: البيانات التاريخية لأسعار المواد
# ==========================================
with tab1:
    st.header("📈 البيانات التاريخية لأسعار المواد (الأشهر 1 إلى 9)")
    data_materials = {
        "الشهر": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "طابوق عادي": [155000, 155000, 152000, 152000, 150000, 160000, 165000, 164000, 161000],
        "سمنت مقاوم": [121000, 123000, 122000, 124000, 124000, 123000, 122000, 121000, 120000],
        "حديد شيش": [985000, 975000, 972000, 980000, 977000, 986000, 971000, 965000, 969000],
        "رمل أسود": [18000, 17000, 17000, 16000, 16000, 16000, 16000, 16000, 16000],
        "حصى مكسر": [22000, 22000, 20000, 20000, 21000, 21000, 22000, 22000, 22000],
        "بورك": [112000, 130000, 130000, 130000, 129000, 137000, 134000, 134000, 135000],
        "كاشي عادي": [12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000],
        "مرمر": [30000, 30000, 30000, 32000, 34000, 34000, 35000, 35000, 35000],
        "سيراميك": [10000, 10000, 10000, 8000, 9000, 9000, 9000, 9000, 9000],
        "أصباغ مائية": [3000, 3000, 3000, 4000, 4000, 4000, 4000, 4000, 4000],
        "تأسيسات كهربائية (نقطة)": [15000, 15000, 15000, 15000, 16000, 16000, 16000, 16000, 16000],
        "أنابيب مياه ومجاري (م.ط)": [10000, 10000, 11000, 11000, 11500, 12000, 12000, 12000, 12000]
    }
    df_materials_history = pd.DataFrame(data_materials)
    st.dataframe(df_materials_history, use_container_width=True)

# ==========================================
# 🟢 الشيت الثاني: البيانات التاريخية لأجور العمال
# ==========================================
with tab2:
    st.header("👷 البيانات التاريخية لأجور الكوادر والعمال (الأشهر 1 إلى 9)")
    data_labor = {
        "الشهر": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "العمال غير الماهرين": [25000, 25000, 25000, 25000, 26000, 26000, 27000, 27000, 27000],
        "العمال شبه الماهرين": [35000, 35000, 35000, 36000, 36000, 37000, 37000, 38000, 38000],
        "العمال الماهرون": [50000, 50000, 52000, 52000, 55000, 55000, 55000, 58000, 60000],
        "فني كهرباء (كهربائي)": [45000, 45000, 45000, 48000, 48000, 50000, 50000, 52000, 55000],
        "فني سباكة ومياه (سباك)": [45000, 45000, 45000, 48000, 48000, 50000, 50000, 52000, 55000],
        "المهندسون": [100000, 100000, 100000, 105000, 105000, 110000, 110000, 115000, 120000]
    }
    df_labor_history = pd.DataFrame(data_labor)
    st.dataframe(df_labor_history, use_container_width=True)

# ==========================================
# 🟢 الشيت الثالث: التحليلات والرسوم البيانية
# ==========================================
with tab3:
    st.header("📊 التحليلات البيانية ورسوم أسعار المواد")
    selected_mat = st.selectbox("اختر المادة لتتبع مسار سعرها:", list(df_materials_history.columns[1:]))
    fig_mat = px.line(df_materials_history, x="الشهر", y=selected_mat, title=f"تغير سعر {selected_mat} عبر الأشهر", markers=True)
    st.plotly_chart(fig_mat, use_container_width=True)

# ==========================================
# 🟢 الشيت الرابع: حساب الكميات والتكاليف (الشيت الرابع النهائي)
# ==========================================
with tab4:
    st.header("📋 الشيت الرابع: جدول الكميات والتكلفة الشامل (مطابق للشيت 4)")
    st.info("💡 يمكنك تعديل أبعاد وخصومات كل فقرة بشكل مستقل تماماً عبر القوائم التشاركية الأدناه:")

    items_fourth = [
        {"name": "حفر الأساسات", "unit": "m3", "l": 48.0, "w": 0.6, "h": 1.0, "disc": 0.0, "mat_rate": 0, "labor_rate": 6250, "cadre": "العمال غير الماهرين"},
        {"name": "صب أسس الخرسانة", "unit": "m3", "l": 48.0, "w": 0.6, "h": 0.4, "disc": 0.0, "mat_rate": 71000, "labor_rate": 17500, "cadre": "العمال شبه الماهرين"},
        {"name": "بناء جدران الطابوق", "unit": "m3", "l": 48.0, "w": 0.24, "h": 3.0, "disc": 4.0, "mat_rate": 84000, "labor_rate": 25000, "cadre": "العمال الماهرون"},
        {"name": "اللبخ بالأسمنت", "unit": "m2", "l": 48.0, "w": 1.0, "h": 3.0, "disc": 6.25, "mat_rate": 2400, "labor_rate": 4000, "cadre": "العمال الماهرون"},
        {"name": "البياض بالبورك", "unit": "m2", "l": 48.0, "w": 1.0, "h": 3.0, "disc": 6.25, "mat_rate": 1600, "labor_rate": 3500, "cadre": "العمال الماهرون"},
        {"name": "تطبيق الأرضيات", "unit": "m2", "l": 48.0, "w": 1.0, "h": 1.0, "disc": 0.0, "mat_rate": 10500, "labor_rate": 4250, "cadre": "العمال الماهرون"},
        {"name": "تطبيق سيراميك الجدران", "unit": "m2", "l": 20.0, "w": 1.0, "h": 3.0, "disc": 1.5, "mat_rate": 11000, "labor_rate": 4500, "cadre": "العمال الماهرون"},
        {"name": "أصباغ مائية للجدران", "unit": "m2", "l": 48.0, "w": 1.0, "h": 3.0, "disc": 6.25, "mat_rate": 2000, "labor_rate": 2500, "cadre": "العمال الماهرون"},
        {"name": "التأسيسات الكهربائية والأسلاك", "unit": "نقطة", "l": 40.0, "w": 1.0, "h": 1.0, "disc": 0.0, "mat_rate": 16000, "labor_rate": 10000, "cadre": "فني كهرباء (كهربائي)"},
        {"name": "تأسيسات المياه والمجاري (البواري)", "unit": "م.طول", "l": 30.0, "w": 1.0, "h": 1.0, "disc": 0.0, "mat_rate": 12000, "labor_rate": 8000, "cadre": "فني سباكة ومياه (سباك)"}
    ]

    calculated_rows = []
    grand_total_num = 0.0

    for item in items_fourth:
        with st.expander(f"📌 مدخلات فقرة: {item['name']}", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                l_val = st.number_input(f"الطول / العدد - {item['name']}", value=float(item['l']), step=0.5, key=f"f4_l_{item['name']}")
            
            with c2:
                if item["unit"] == "m3":
                    w_val = st.number_input(f"العرض (م) - {item['name']}", value=float(item['w']), step=0.05, key=f"f4_w_{item['name']}")
                else:
                    w_val = 1.0
                    st.text_input(f"العرض - {item['name']}", value="سطحي (غير مطلوب)", disabled=True, key=f"f4_dis_w_{item['name']}")
                    
            with c3:
                if item["unit"] in ["m3", "m2"]:
                    h_val = st.number_input(f"السمك / الارتفاع (م) - {item['name']}", value=float(item['h']), step=0.1, key=f"f4_h_{item['name']}")
                else:
                    h_val = 1.0
                    st.text_input(f"الارتفاع - {item['name']}", value="غير مطلوب", disabled=True, key=f"f4_dis_h_{item['name']}")
                
            with c4:
                disc_val = st.number_input(f"الخصم (الفتحات) - {item['name']}", value=float(item['disc']), step=0.25, key=f"f4_disc_{item['name']}")

        # حساب الكميات الصافية
        if item["unit"] == "m3":
            gross_qty = l_val * w_val * h_val
        elif item["unit"] == "m2":
            gross_qty = l_val * h_val
        else:
            gross_qty = l_val
            
        net_qty = max(0.0, gross_qty - disc_val)
        
        mat_cost = net_qty * item["mat_rate"]
        labor_cost = net_qty * item["labor_rate"]
        total_cost = mat_cost + labor_cost
        
        grand_total_num += total_cost
        
        calculated_rows.append({
            "تفاصيل الفقرة الهندسية": item["name"],
            "الوحدة": item["unit"],
            "الطول / العدد": round(l_val, 2),
            "السمك / الارتفاع": round(h_val, 2) if item["unit"] in ["m3", "m2"] else "-",
            "الخصم": round(disc_val, 2),
            "الكمية الصافية": round(net_qty, 2),
            "كلفة المواد (مستقبلاً)": f"{int(mat_cost):,}",
            "الكادر المطلوب": item["cadre"],
            "كلفة العمل (مستقر)": f"{int(labor_cost):,}",
            "الكلفة الكلية المتوقعة (دينار)": f"{int(total_cost):,}"
        })

    df_s4 = pd.DataFrame(calculated_rows)

    st.markdown("---")
    st.subheader("📋 شيت جدول الكميات والتكاليف الإجمالية")
    
    st.dataframe(df_s4, use_container_width=True)

    st.markdown(
        f"""
        <div style="background-color: #1b5e20; padding: 16px; border-radius: 6px; text-align: center; color: white; font-size: 22px; font-weight: bold; font-family: sans-serif; margin-top: 15px;">
            الكلفة الإجمالية التقديرية (دينار عراقي) : {grand_total_num:,.0f}
        </div>
        """,
        unsafe_html=True
    )
