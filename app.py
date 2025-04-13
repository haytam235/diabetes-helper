import streamlit as st
import pandas as pd
from datetime import datetime

# تعريب النصوص
def translate_text(language):
    if language == "العربية":
        return {
            "title": "تطبيق سجل السكري",
            "description": "مرحبًا! يساعدك هذا التطبيق على تسجيل بيانات السكري اليومية.",
            "date": "التاريخ",
            "blood_sugar": "مستوى السكر في الدم (مجم/ديسيلتر)",
            "insulin_dose": "جرعة الإنسولين (وحدات)",
            "notes": "ملاحظات",
            "save": "حفظ البيانات",
            "view": "عرض السجلات",
            "error": "يرجى ملء جميع الحقول!"
        }
    else:  # English
        return {
            "title": "Diabetes Diary App",
            "description": "Welcome! This app helps you log your daily diabetes data.",
            "date": "Date",
            "blood_sugar": "Blood Sugar Level (mg/dL)",
            "insulin_dose": "Insulin Dose (units)",
            "notes": "Notes",
            "save": "Save Data",
            "view": "View Records",
            "error": "Please fill all the fields!"
        }

# اختر اللغة
language = st.selectbox("Select Language / اختر اللغة", ["English", "العربية"])

# الترجمة بناءً على اللغة المختارة
texts = translate_text(language)

# عنوان التطبيق
st.title(texts["title"])
st.write(texts["description"])

# الحقول التي يجب ملؤها
date = st.date_input(texts["date"])
blood_sugar = st.number_input(texts["blood_sugar"], min_value=0, max_value=500)
insulin_dose = st.number_input(texts["insulin_dose"], min_value=0, max_value=100)
notes = st.text_area(texts["notes"])

# تحميل بيانات سابقة من الملف
file_path = 'diabetes_data.csv'

try:
    # حاول قراءة البيانات السابقة
    df = pd.read_csv(file_path)
except FileNotFoundError:
    # إذا لم يكن الملف موجودًا، قم بإنشاء DataFrame فارغ
    df = pd.DataFrame(columns=["date", "blood_sugar", "insulin_dose", "notes"])

# زر حفظ البيانات
if st.button(texts["save"]):
    # التحقق من أن جميع الحقول مكتملة
    if date and blood_sugar and insulin_dose and notes:
        # إضافة المدخلات الجديدة إلى DataFrame
        new_entry = pd.DataFrame([[date, blood_sugar, insulin_dose, notes]],
                                 columns=["date", "blood_sugar", "insulin_dose", "notes"])
        df = pd.concat([df, new_entry], ignore_index=True)
        
        # حفظ البيانات في الملف
        df.to_csv(file_path, index=False)
        
        # إعادة تعيين المدخلات بعد الحفظ
        date = None
        blood_sugar = 0
        insulin_dose = 0
        notes = ""
        
        st.success(f"{texts['save']} {texts['view']}!")
    else:
        # إذا كانت الحقول غير مكتملة
        st.error(texts["error"])

# زر لعرض السجلات السابقة
if st.button(texts["view"]):
    if not df.empty:
        st.write("### سجل البيانات السابق:")
        st.write(df)
    else:
        st.write("لا توجد بيانات بعد.")
