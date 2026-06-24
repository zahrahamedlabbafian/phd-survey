import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

# ==========================================
# تنظیمات صفحه
# ==========================================
st.set_page_config(
    page_title="پرسشنامه دکتری گراف و ترکیبیات",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# عنوان و توضیحات
# ==========================================
st.title("📊 پرسشنامه دوره دکتری گراف و ترکیبیات")
st.markdown("""
**با سلام و عرض ادب**

پرسشنامه زیر به منظور بررسی و بازنگری دروس مقطع دکتری گراف و ترکیبیات تهیه شده است 
و پاسخگویان دانشجویان و دانش‌آموختگان این رشته می‌باشند. 
خواهشمند است سؤالات را با دقت پاسخ دهید تا بتواند در جهت دستیابی به بهترین برنامه، کارآمد باشد.

**آزمایشگاه نظریه گراف و کاربردهای آن، دانشگاه فردوسی مشهد**
""")
st.divider()

# ==========================================
# توابع کمکی برای ذخیره و بارگذاری داده
# ==========================================

def save_response(data):
    """
    ذخیره پاسخ در فایل CSV با مدیریت کامل خطاها
    
    Args:
        data (dict): دیکشنری شامل پاسخ‌های کاربر
    
    Returns:
        bool: True اگر ذخیره موفق بود، False اگر خطا رخ داد
    """
    file_path = "data/responses.csv"
    
    # 1. ایجاد پوشه data اگر وجود ندارد
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        st.error(f"❌ خطا در ایجاد پوشه data: {e}")
        return False
    
    # 2. بارگذاری داده‌های موجود
    df = pd.DataFrame()  # دیتافریم خالی پیش‌فرض
    
    if os.path.exists(file_path):
        try:
            # بررسی خالی بودن فایل
            if os.path.getsize(file_path) > 0:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                # فایل خالی است
                st.warning("⚠️ فایل CSV خالی بود، یک فایل جدید ساخته می‌شود.")
        except pd.errors.EmptyDataError:
            st.warning("⚠️ فایل CSV خالی یا خراب است، بازسازی می‌شود.")
        except Exception as e:
            st.error(f"❌ خطا در خواندن فایل: {e}")
            # پشتیبان‌گیری از فایل خراب
            if os.path.exists(file_path):
                backup_path = f"data/responses_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                try:
                    os.rename(file_path, backup_path)
                    st.info(f"📁 از فایل قبلی پشتیبان گرفته شد: {backup_path}")
                except:
                    pass
            df = pd.DataFrame()
    
    # 3. ایجاد دیتافریم جدید برای پاسخ
    try:
        new_df = pd.DataFrame([data])
    except Exception as e:
        st.error(f"❌ خطا در ایجاد داده جدید: {e}")
        return False
    
    # 4. ترکیب با داده‌های قبلی
    try:
        if df.empty:
            df = new_df
        else:
            # اطمینان از هم‌شکل بودن ستون‌ها
            for col in new_df.columns:
                if col not in df.columns:
                    df[col] = None  # اضافه کردن ستون جدید با مقدار خالی
            df = pd.concat([df, new_df], ignore_index=True)
    except Exception as e:
        st.error(f"❌ خطا در ترکیب داده‌ها: {e}")
        return False
    
    # 5. ذخیره در فایل
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        st.error(f"❌ خطا در ذخیره فایل: {e}")
        return False


def load_responses():
    """
    بارگذاری پاسخ‌های قبلی با مدیریت خطا
    
    Returns:
        pd.DataFrame: دیتافریم شامل پاسخ‌ها
    """
    file_path = "data/responses.csv"
    
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        if os.path.getsize(file_path) == 0:
            return pd.DataFrame()
        return pd.read_csv(file_path, encoding='utf-8-sig')
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ خطا در بارگذاری فایل: {e}")
        return pd.DataFrame()

# ==========================================
# فرم اصلی
# ==========================================

with st.form("survey_form"):
    st.header("بخش اول: اطلاعات دموگرافیک")
    
    col1, col2 = st.columns(2)
    with col1:
        fullname = st.text_input(
            "نام و نام خانوادگی *", 
            placeholder="مثال: علی محمدی"
        )
        email = st.text_input(
            "ایمیل", 
            placeholder="example@email.com"
        )
    
    with col2:
        status = st.selectbox(
            "وضعیت تحصیلی *",
            options=["انتخاب کنید...", "دانشجوی دکتری", "دانش‌آموخته دکتری", "پسادکتری", "هیئت علمی"]
        )
        university = st.text_input(
            "دانشگاه/مرکز علمی", 
            placeholder="مثال: دانشگاه فردوسی مشهد"
        )
    
    st.header("بخش دوم: ارزیابی دروس تخصصی")
    st.caption("لطفاً میزان اهمیت هر یک از دروس زیر را در دوره دکتری مشخص کنید.")
    
    # لیست دروس (قابل ویرایش)
    courses = [
        "نظریه گراف پیشرفته",
        "ترکیبیات پیشرفته",
        "الگوریتم‌های گراف",
        "کاربردهای گراف در شبکه",
        "رنگ‌آمیزی گراف",
        "گراف‌های تصادفی",
        "بهینه‌سازی ترکیبیاتی",
        "نظریه رمز و گراف"
    ]
    
    # ماتریس مقیاس لیکرت برای دروس
    course_ratings = {}
    for course in courses:
        course_ratings[course] = st.select_slider(
            f"اهمیت درس **{course}**",
            options=["خیلی کم", "کم", "متوسط", "زیاد", "خیلی زیاد"],
            value="متوسط",
            key=f"course_{course}"
        )
    
    st.header("بخش سوم: مهارت‌ها و توانمندی‌ها")
    st.caption("میزان تسلط خود را در موارد زیر ارزیابی کنید.")
    
    skills = [
        "تسلط بر مبانی نظریه گراف",
        "توانایی اثبات قضایا",
        "برنامه‌نویسی الگوریتم‌های گراف",
        "کار با نرم‌افزارهای تخصصی (مثل SageMath, NetworkX)",
        "مطالعه مقالات تخصصی به زبان انگلیسی",
        "نگارش مقالات علمی"
    ]
    
    # ماتریس مقیاس لیکرت برای مهارت‌ها
    skill_ratings = {}
    for skill in skills:
        skill_ratings[skill] = st.select_slider(
            f"**{skill}**",
            options=["ضعیف", "متوسط", "خوب", "عالی"],
            value="متوسط",
            key=f"skill_{skill}"
        )
    
    st.header("بخش چهارم: پیشنهادات و نظرات تکمیلی")
    
    suggestions = st.text_area(
        "پیشنهادات شما برای بهبود برنامه درسی دوره دکتری گراف و ترکیبیات",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=150
    )
    
    research_interests = st.text_area(
        "حوزه‌های پژوهشی مورد علاقه شما",
        placeholder="مثال: نظریه گراف طیفی، گراف‌های کیلی، کاربردهای ترکیبیات...",
        height=100
    )
    
    st.divider()
    st.caption("⚠️ فیلدهای دارای * الزامی هستند.")
    
    # دکمه ثبت
    submitted = st.form_submit_button("✅ ثبت پاسخ‌ها", use_container_width=True)
    
    if submitted:
        # اعتبارسنجی
        errors = []
        if not fullname:
            errors.append("نام و نام خانوادگی")
        if status == "انتخاب کنید...":
            errors.append("وضعیت تحصیلی")
        
        if errors:
            st.error(f"⚠️ لطفاً فیلدهای زیر را تکمیل کنید: {', '.join(errors)}")
        else:
            # ساخت دیکشنری پاسخ
            response_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fullname": fullname,
                "email": email,
                "status": status,
                "university": university,
                "suggestions": suggestions,
                "research_interests": research_interests,
            }
            
            # اضافه کردن پاسخ‌های دروس
            for course, rating in course_ratings.items():
                response_data[f"course_{course}"] = rating
            
            # اضافه کردن پاسخ‌های مهارت‌ها
            for skill, rating in skill_ratings.items():
                response_data[f"skill_{skill}"] = rating
            
            # ذخیره (با بررسی نتیجه)
            success = save_response(response_data)
            
            if success:
                st.success("✅ پاسخ‌های شما با موفقیت ثبت شد. سپاسگزاریم!")
                st.balloons()
                
                # پاک کردن فرم با استفاده از session state
                st.session_state.form_submitted = True
            else:
                st.error("❌ متأسفانه خطایی در ثبت پاسخ رخ داد. لطفاً دوباره تلاش کنید.")

# ==========================================
# نمایش نتایج (دسترسی مدیر)
# ==========================================

st.divider()
st.subheader("📊 مشاهده نتایج (دسترسی مدیر)")

# احراز هویت ساده
password = st.text_input("رمز عبور برای مشاهده نتایج:", type="password")

if password == "admin123":  # این رمز را تغییر دهید
    st.success("✅ دسترسی تایید شد!")
    
    # بارگذاری داده‌ها
    df = load_responses()
    
    if not df.empty:
        # آمار کلی
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("تعداد کل پاسخ‌ها", len(df))
        with col2:
            if 'status' in df.columns:
                students = len(df[df['status'] == 'دانشجوی دکتری'])
                st.metric("تعداد دانشجویان", students)
            else:
                st.metric("تعداد دانشجویان", 0)
        with col3:
            if 'status' in df.columns:
                graduates = len(df[df['status'] == 'دانش‌آموخته دکتری'])
                st.metric("تعداد دانش‌آموختگان", graduates)
            else:
                st.metric("تعداد دانش‌آموختگان", 0)
        
        # نمایش جدول
        st.subheader("📋 لیست کامل پاسخ‌ها")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # دکمه دانلود
        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥 دانلود همه پاسخ‌ها (CSV)",
            data=csv,
            file_name=f"پاسخ‌های_نظرسنجی_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # نمودارهای تحلیلی
        if 'status' in df.columns:
            st.subheader("📊 تحلیل سریع")
            
            # نمودار توزیع وضعیت تحصیلی
            status_counts = df['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="توزیع وضعیت تحصیلی پاسخ‌دهندگان",
                hole=0.3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        # نمایش چند نمونه از نظرات (در صورت وجود)
        if 'suggestions' in df.columns:
            with st.expander("💬 مشاهده نظرات و پیشنهادات"):
                for i, (idx, row) in enumerate(df.iterrows()):
                    if row['suggestions'] and len(str(row['suggestions']).strip()) > 0:
                        st.write(f"**{i+1}.** {row['fullname']}: {row['suggestions']}")
        
    else:
        st.info("📭 هنوز هیچ پاسخی ثبت نشده است.")
else:
    if password:
        st.error("❌ رمز عبور اشتباه است!")
    else:
        st.info("🔑 برای مشاهده نتایج، رمز عبور را وارد کنید.")

# ==========================================
# پاورقی
# ==========================================
st.divider()
st.caption("📌 این پرسشنامه توسط آزمایشگاه نظریه گراف و کاربردهای آن، دانشگاه فردوسی مشهد تهیه شده است.")