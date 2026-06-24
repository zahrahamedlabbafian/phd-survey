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
    st.header("بخش اول: اطلاعات فردی")
    
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
        work = st.selectbox( 
            "وضعیت شغلی",
            options=["انتخاب کنید...", "شاغل", "بدون شغل"]
        )
        address = st.text_input(
            "محل کار:",
            placeholder="مثال: دانشگاه فردوسی مشهد"
        )   

    with col2:
        gender = st.selectbox(
            "جنسیت",
            options=["انتخاب کنید...", "مرد", "زن"]
        )
        status = st.selectbox(
            "وضعیت تحصیلی *",
            options=["انتخاب کنید...", "دانشجوی دکتری", "دانش‌آموخته دکتری"]
        )
        university = st.text_input(
            "دانشگاه/مرکز علمی",
            placeholder="مثال: دانشگاه فردوسی مشهد"
        )
    
    # ========== انگیزه ==========
    st.subheader("انگیزه شما از انتخاب حوزه «نظریه گراف» در مقطع تحصیلات تکمیلی")
    st.caption("می‌توانید بیش از یک گزینه انتخاب کنید")

    motivation_options = [
        "علاقه شخصی به ریاضیات و نظریه گراف",
        "اهمیت علمی و کاربردی نظریه گراف در سایر علوم",
        "توصیه اساتید، پژوهشگران یا افراد دیگر",
        "بازار کار خوب",
        "شهرت و اعتبار حرفه‌ای",
        "جذابیت مسائل و ساختارهای ریاضی در گراف‌ها",
        "سهولت قبولی در این رشته",
        "ارتقای شغل فعلی"
    ]

    motivations = st.multiselect(
        "گزینه‌های مورد نظر را انتخاب کنید:",
        options=motivation_options,
        placeholder="یک یا چند گزینه را انتخاب کنید..."
    )
    
    # ========== مهارت‌ها ==========
    st.header("بخش دوم: ارزیابی مهارت‌های آموخته شده در دانشگاه")
    st.caption("تا چه حد مهارت‌های زیر را در دانشگاه فرا می‌گیرید؟ (از 1 تا 5 نمره دهید)")

    skills = [
        "توانایی کارگروهی",
        "مهارت‌های تخصصی شامل برنامه‌نویسی و کار با نرم‌افزار",
        "استفاده از مسائل گراف در مسائل روزمره",
        "قدرت تجزیه و تحلیل"
    ]

    skill_scores = {}
    for skill in skills:
        skill_scores[skill] = st.select_slider(
            f"**{skill}**",
            options=[1, 2, 3, 4, 5],
            value=3,
            key=f"skill_score_{skill}"
        )
    
    # ========== ارزیابی دروس (ماتریس) ==========
    st.header("بخش سوم: ارزیابی تأثیر دروس گذرانده شده")
    st.caption("لطفاً تأثیر هر یک از دروس را در موارد خواسته شده با عددی بین 1 تا 5 امتیاز دهید.")

    # لیست دروس (ردیف‌ها)
    courses = [
        "مباحثی در نظریه گراف",
        "نظریه جبری گراف",
        "نظریه طیفی گراف",
        "ترکیبیات پیشرفته",
        "بهینه‌سازی ترکیباتی",
        "الگوریتم‌های گرافی",
        "گراف‌های تصادفی",
        "نظریه رمزنگاری",
        "طرح‌های بلوکی",
        "ماترویدها",
        "تاپولوژی ترکیباتی",
        "نظریه کدگذاری",
        "پایگاه داده‌های گرافی",
        "یادگیری ماشین گرافی",
        "رنگ‌آمیزی گراف پیشرفته"
    ]

    # لیست ستون‌ها (معیارهای ارزیابی)
    criteria = [
        "تناسب درس با اهداف رشته",
        "تناسب سرفصل‌ها با درس",
        "تناسب شیوه تدریس با سرفصل‌ها",
        "توانمندی استاد در ارائه درس",
        "بروز بودن محتوا و جدید بودن درس",
        "مناسب بودن تعداد واحدهای آموزشی درس",
        "مناسب بودن حجم مطالب درس",
        "میزان علاقه‌مندی به درس",
        "ضرورت حل تمرین یا آزمایشگاه برای این درس",
        "نقش درس در افزایش توانمندی علمی شما"
    ]

    # ایجاد دیتافریم با مقادیر پیش‌فرض (همه ۳)
    data = {}
    data["درس"] = courses
    for criterion in criteria:
        data[criterion] = [3] * len(courses)

    df_courses = pd.DataFrame(data)

    # نمایش جدول قابل ویرایش
    edited_df = st.data_editor(
        df_courses,
        use_container_width=True,
        hide_index=True,
        column_config={
            "درس": st.column_config.TextColumn("دروس", disabled=True, width="medium"),
            **{
                criterion: st.column_config.NumberColumn(
                    criterion,
                    min_value=1,
                    max_value=5,
                    step=1,
                    width="small"
                )
                for criterion in criteria
            }
        },
        num_rows="fixed"
    )

    # ========== سوالات باز ==========
    st.header("بخش چهارم: سوالات باز")
    
    suggestion_1 = st.text_area(
        "به نظر شما کدام دروس باید در برنامه دکتری گراف به صورت اجباری ارائه شوند؟",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=100
    )
    
    suggestion_2 = st.text_area(
        "اگر پیشنهادی برای تغییر منابع، سرفصل‌ها و پیش‌نیازی-هم‌نیازی دارید (به دلایلی همچون عدم تناسب سرفصل‌ها، قدیمی بودن منبع در صورت موجود بودن منبع جدیدتر و برتر و...) ذکر نمایید. (با ذکر نام کتاب)",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=100
    )
    
    suggestion_3 = st.text_area(
        "لطفاً پیشنهادات خود را برای ارائه‌ی دوره‌ها، کارگاه‌ها، سمینارها و همایش‌ها جهت تقویت دانش و مهارت‌های تخصصی در حوزه‌های مرتبط با نظریه گراف و ریاضیات گسسته بیان نمایید:",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=100
    )
    
    suggestion_4 = st.text_area(
        "به نظر شما یک دانش‌آموخته در حوزه‌های مرتبط با نظریه گراف در مقطع دکتری باید دارای چه دانش‌ها و مهارت‌های علمی، پژوهشی و تحلیلی باشد؟",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=100
    )

    suggestion_5 = st.text_area(
        "اگر در سوال قبل، دانش و مهارت‌های یاد شده با دروسی که در این مقطع ارائه می‌شود قابل دستیابی نیست، لطفا پیشنهاد خود را برای دروس یا مهارت‌های لازم، ارائه دهید.",
        placeholder="لطفاً نظرات و پیشنهادات خود را در اینجا بنویسید...",
        height=100
    )

    st.divider()
    st.caption("🙏 با تشکر فراوان از زمان و توجه شما")
    
    # ========== دکمه ثبت ==========
    submitted = st.form_submit_button("✅ ثبت پاسخ‌ها", use_container_width=True)
    
    if submitted:
        # ========== اعتبارسنجی ==========
        errors = []
        if not fullname:
            errors.append("نام و نام خانوادگی")
        if status == "انتخاب کنید...":
            errors.append("وضعیت تحصیلی")
        
        if errors:
            st.error(f"⚠️ لطفاً فیلدهای زیر را تکمیل کنید: {', '.join(errors)}")
        else:
            # ========== ساخت دیکشنری پاسخ ==========
            response_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fullname": fullname,
                "email": email,
                "gender": gender if gender != "انتخاب کنید..." else "",
                "work": work if work != "انتخاب کنید..." else "",
                "address": address,
                "status": status,
                "university": university,
                "motivations": ", ".join(motivations) if motivations else "",
            }
            
            # اضافه کردن نمرات مهارت‌ها
            for skill, score in skill_scores.items():
                response_data[f"skill_{skill}"] = score
            
            # اضافه کردن امتیازات دروس (ماتریس)
            for idx, row in edited_df.iterrows():
                course_name = row["درس"]
                for criterion in criteria:
                    key = f"course_{course_name}_{criterion}"
                    response_data[key] = row[criterion]
            
            # اضافه کردن سوالات باز
            response_data["suggestion_1"] = suggestion_1
            response_data["suggestion_2"] = suggestion_2
            response_data["suggestion_3"] = suggestion_3
            response_data["suggestion_4"] = suggestion_4
            response_data["suggestion_5"] = suggestion_5
            
            # ========== ذخیره ==========
            success = save_response(response_data)
            
            if success:
                st.success("✅ پاسخ‌های شما با موفقیت ثبت شد. سپاسگزاریم!")
                st.balloons()
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
        
        # نمایش نظرات (در صورت وجود)
        suggestion_cols = [col for col in df.columns if col.startswith('suggestion_')]
        if suggestion_cols:
            with st.expander("💬 مشاهده نظرات و پیشنهادات"):
                for idx, row in df.iterrows():
                    st.write(f"**{idx+1}. {row['fullname']}**")
                    for col in suggestion_cols:
                        if row[col] and len(str(row[col]).strip()) > 0:
                            st.write(f"- {col.replace('suggestion_', 'سوال ')}: {row[col]}")
                    st.divider()
        
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
