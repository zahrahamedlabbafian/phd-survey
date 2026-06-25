import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

# لیست معیارهای ارزیابی دروس
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
    "نقش درس در افزایش توانمندی علمی",
    "نقش درس در افزایش توانمندی شغلی"
]
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
        "مباحثی ویژه در نظریه گراف",
        "نظریه جبری گراف",
        "نظریه طیفی گراف",
        "ترکیبیات پیشرفته",
        "بهینه‌سازی ترکیبیاتی",
        "الگوریتم‌های گرافی",
        "آنالیز ترکیبیاتی پیشرفته",
        "ترکیبیات شمارشی",
        "روش‌های توپولوژيکی در گراف",
        "عملیات گراف",
        "فاصله در گراف",
        "گراف کاوی",
        "مباحثی در نظریه احتمالی گروه‌ها",
        "یادگیری ماشین روی گراف",
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
# نمایش نتایج (دسترسی مدیر) - نسخه کامل با تمام تحلیل‌ها
# ==========================================

st.divider()
st.subheader("📊 مشاهده نتایج (دسترسی مدیر)")

# احراز هویت ساده
password = st.text_input("رمز عبور برای مشاهده نتایج:", type="password")

if password == "admin123":
    st.success("✅ دسترسی تایید شد!")
    
    # بارگذاری داده‌ها
    df = load_responses()
    
    if not df.empty:
        # ============================================================
        # 1. مشخصات فردی پاسخ‌دهندگان
        # ============================================================
        st.header("👤 مشخصات فردی پاسخ‌دهندگان")
        st.caption("با توجه به کم بودن تعداد نظرات ثبت شده، در تمامی نمودارها از فراوانی بجای درصد فراوانی استفاده گردید.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # جنسیت
            st.subheader("جنسیت")
            if 'gender' in df.columns:
                gender_counts = df['gender'].value_counts()
                if not gender_counts.empty:
                    fig_gender = px.bar(
                        x=gender_counts.index,
                        y=gender_counts.values,
                        title="توزیع جنسیت پاسخ‌دهندگان",
                        text=gender_counts.values,
                        color=gender_counts.index,
                        labels={'x': 'جنسیت', 'y': 'تعداد'}
                    )
                    fig_gender.update_traces(textposition='outside')
                    st.plotly_chart(fig_gender, use_container_width=True)
                    
                    # نمایش جدول
                    gender_df = pd.DataFrame({
                        'جنسیت': gender_counts.index,
                        'فراوانی': gender_counts.values,
                        'درصد': (gender_counts.values / len(df) * 100).round(1)
                    })
                    st.dataframe(gender_df, use_container_width=True, hide_index=True)
        
        with col2:
            # سال ورود (اگر موجود باشد)
            st.subheader("سال ورود")
            if 'entry_year' in df.columns:
                year_counts = df['entry_year'].value_counts().sort_index()
                if not year_counts.empty:
                    fig_year = px.bar(
                        x=year_counts.index,
                        y=year_counts.values,
                        title="توزیع سال ورود پاسخ‌دهندگان",
                        text=year_counts.values,
                        color=year_counts.index,
                        labels={'x': 'سال ورود', 'y': 'تعداد'}
                    )
                    fig_year.update_traces(textposition='outside')
                    st.plotly_chart(fig_year, use_container_width=True)
        
        with col3:
            # وضعیت شغلی
            st.subheader("وضعیت شغلی")
            if 'work' in df.columns:
                work_counts = df['work'].value_counts()
                if not work_counts.empty:
                    fig_work = px.bar(
                        x=work_counts.index,
                        y=work_counts.values,
                        title="توزیع وضعیت شغلی",
                        text=work_counts.values,
                        color=work_counts.index,
                        labels={'x': 'وضعیت شغلی', 'y': 'تعداد'}
                    )
                    fig_work.update_traces(textposition='outside')
                    st.plotly_chart(fig_work, use_container_width=True)
        
        st.divider()
        
        # ============================================================
        # 2. انگیزه انتخاب رشته
        # ============================================================
        st.header("🎯 انگیزه انتخاب رشته")
        
        if 'motivations' in df.columns:
            # استخراج و شمارش انگیزه‌ها
            all_motivations = []
            for item in df['motivations'].dropna():
                if item:
                    all_motivations.extend([m.strip() for m in item.split(',')])
            
            if all_motivations:
                from collections import Counter
                mot_counts = Counter(all_motivations)
                mot_df = pd.DataFrame({
                    'انگیزه': list(mot_counts.keys()),
                    'فراوانی': list(mot_counts.values())
                }).sort_values('فراوانی', ascending=False)
                
                # محاسبه درصد
                total = mot_df['فراوانی'].sum()
                mot_df['درصد'] = (mot_df['فراوانی'] / total * 100).round(1)
                
                # نمودار
                fig_mot = px.bar(
                    mot_df,
                    x='انگیزه',
                    y='فراوانی',
                    title="انگیزه از انتخاب رشته نظریه گراف",
                    text='فراوانی',
                    color='انگیزه',
                    labels={'انگیزه': 'انگیزه', 'فراوانی': 'تعداد انتخاب‌ها'}
                )
                fig_mot.update_traces(textposition='outside')
                fig_mot.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_mot, use_container_width=True)
                
                # نمایش جدول
                st.dataframe(mot_df, use_container_width=True, hide_index=True)
                
                # نمایش پرتکرارترین
                top_mot = mot_df.iloc[0]
                st.info(f"📌 **پرتکرارترین انگیزه:** {top_mot['انگیزه']} با {top_mot['فراوانی']} نظر (معادل {top_mot['درصد']}% از کل نظرات)")
        
        st.divider()
        
        # ============================================================
        # 3. بررسی مهارت‌های فراگرفته شده
        # ============================================================
        st.header("💪 بررسی مهارت‌های فراگرفته شده در دانشگاه")
        
        # پیدا کردن ستون‌های مهارت‌ها
        skill_cols = [col for col in df.columns if col.startswith('skill_')]
        if skill_cols:
            # جدول درصد فراوانی
            st.subheader("توزیع درصد فراوانی گزینه‌های انتخاب شده به تفکیک مهارت")
            
            skill_labels = {
                'توانایی کارگروهی': 'توانایی کارگروهی',
                'مهارت‌های تخصصی شامل برنامه‌نویسی و کار با نرم‌افزار': 'مهارت‌های تخصصی',
                'استفاده از مسائل گراف در مسائل روزمره': 'کاربرد مسائل گراف',
                'قدرت تجزیه و تحلیل': 'قدرت تجزیه و تحلیل'
            }
            
            # ایجاد جدول فراوانی
            freq_data = {}
            for col in skill_cols:
                skill_name = col.replace('skill_', '')
                if skill_name in df.columns:
                    freq = df[skill_name].value_counts().sort_index()
                    freq_data[skill_labels.get(skill_name, skill_name)] = freq
            
            if freq_data:
                freq_df = pd.DataFrame(freq_data).fillna(0)
                # تبدیل به درصد
                freq_df_pct = freq_df.div(freq_df.sum()) * 100
                
                st.dataframe(freq_df_pct.round(2), use_container_width=True)
                
                # نمودار میانگین مهارت‌ها
                st.subheader("میانگین امتیاز مهارت‌ها (از ۱ تا ۵)")
                skill_means = {}
                for col in skill_cols:
                    skill_name = col.replace('skill_', '')
                    if skill_name in df.columns:
                        skill_means[skill_labels.get(skill_name, skill_name)] = df[skill_name].mean()
                
                if skill_means:
                    skill_mean_df = pd.DataFrame({
                        'مهارت': list(skill_means.keys()),
                        'میانگین': list(skill_means.values())
                    }).sort_values('میانگین', ascending=False)
                    
                    fig_skills = px.bar(
                        skill_mean_df,
                        x='مهارت',
                        y='میانگین',
                        title="میانگین امتیاز مهارت‌های فراگرفته شده",
                        text='میانگین',
                        color='مهارت',
                        range_y=[1, 5],
                        labels={'مهارت': 'مهارت', 'میانگین': 'میانگین امتیاز'}
                    )
                    fig_skills.update_traces(textposition='outside')
                    fig_skills.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_skills, use_container_width=True)
        
        st.divider()
        
        # ============================================================
        # 4. دیدگاه پاسخ‌دهندگان درباره دروس (ماتریس کامل)
        # ============================================================
        st.header("📚 دیدگاه پاسخ‌دهندگان درباره دروس")
        st.caption("امتیازدهی به معیارهای مختلف برای هر درس (از ۱ تا ۵)")
        
        # پیدا کردن ستون‌های دروس
        course_cols = [col for col in df.columns if col.startswith('course_')]
        if course_cols:
            # استخراج نام دروس و معیارها
            courses_list = []
            criteria_list = []
            
            for col in course_cols:
                if '_' in col:
                    parts = col.split('_', 1)
                    if len(parts) == 2:
                        course_name = parts[1]
                        # پیدا کردن معیار
                        for criterion in criteria:
                            if criterion in parts[0]:
                                courses_list.append(course_name)
                                criteria_list.append(criterion)
                                break
            
            # ایجاد دیتافریم برای ماتریس
            if courses_list and criteria_list:
                # محاسبه میانگین برای هر درس و هر معیار
                matrix_data = {}
                for course in set(courses_list):
                    matrix_data[course] = {}
                    for criterion in set(criteria_list):
                        col_name = f"course_{criterion}_{course}"
                        if col_name in df.columns:
                            matrix_data[course][criterion] = df[col_name].mean()
                        else:
                            matrix_data[course][criterion] = None
                
                if matrix_data:
                    matrix_df = pd.DataFrame(matrix_data).T
                    
                    # نمایش ماتریس گرمایی (Heatmap)
                    st.subheader("🔥 ماتریس گرمای امتیازات دروس بر اساس معیارها")
                    fig_heatmap = px.imshow(
                        matrix_df,
                        title="میانگین امتیازات هر درس بر اساس معیارها",
                        labels=dict(x="معیارها", y="دروس", color="میانگین امتیاز"),
                        color_continuous_scale="Viridis",
                        aspect="auto",
                        text_auto=True
                    )
                    fig_heatmap.update_layout(height=600)
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # نمایش جدول کامل
                    with st.expander("📋 مشاهده جدول کامل امتیازات دروس"):
                        st.dataframe(matrix_df.round(2), use_container_width=True)
        
        st.divider()
        
        # ============================================================
        # 5. جمع‌بندی و میانگین معیارها
        # ============================================================
        st.header("📊 جمع‌بندی میانگین معیارها")
        
        if course_cols:
            # محاسبه میانگین هر معیار برای همه دروس
            criterion_means = {}
            for criterion in criteria:
                cols = [col for col in course_cols if criterion in col]
                if cols:
                    all_values = []
                    for col in cols:
                        if col in df.columns:
                            all_values.extend(df[col].dropna().tolist())
                    if all_values:
                        criterion_means[criterion] = sum(all_values) / len(all_values)
            
            if criterion_means:
                criteria_df = pd.DataFrame({
                    'معیار': list(criterion_means.keys()),
                    'میانگین': list(criterion_means.values())
                }).sort_values('میانگین', ascending=False)
                
                # نمودار میله‌ای
                fig_criteria = px.bar(
                    criteria_df,
                    x='معیار',
                    y='میانگین',
                    title="میانگین امتیاز معیارهای ارزیابی دروس",
                    text='میانگین',
                    color='معیار',
                    range_y=[1, 5],
                    labels={'معیار': 'معیارها', 'میانگین': 'میانگین امتیاز'}
                )
                fig_criteria.update_traces(textposition='outside')
                fig_criteria.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_criteria, use_container_width=True)
                
                # نمایش جدول
                st.dataframe(criteria_df.round(3), use_container_width=True, hide_index=True)
        
        st.divider()
        
        # ============================================================
        # 6. سوالات باز
        # ============================================================
        st.header("💬 نظرات و پیشنهادات")
        
        suggestion_cols = [col for col in df.columns if col.startswith('suggestion_')]
        if suggestion_cols:
            # تعداد کل نظرات
            total_suggestions = 0
            for col in suggestion_cols:
                count = df[col].dropna().apply(lambda x: len(str(x).strip()) > 0).sum()
                total_suggestions += count
            
            st.metric("تعداد کل نظرات ثبت شده", total_suggestions)
            
            # نمایش نظرات در تب‌ها
            tab_names = [
                "دروس اجباری",
                "تغییر منابع",
                "دوره‌ها و کارگاه‌ها",
                "مهارت‌های دانش‌آموخته",
                "پیشنهادات تکمیلی"
            ]
            
            tabs = st.tabs(tab_names)
            
            for i, col in enumerate(suggestion_cols):
                with tabs[i] if i < len(tabs) else tabs[-1]:
                    suggestions_list = df[col].dropna().tolist()
                    suggestions_list = [s for s in suggestions_list if str(s).strip()]
                    
                    if suggestions_list:
                        # نمایش آمار
                        st.caption(f"تعداد نظرات: {len(suggestions_list)}")
                        
                        for j, text in enumerate(suggestions_list):
                            st.write(f"**{j+1}.** {text}")
                    else:
                        st.info("هیچ نظری در این بخش ثبت نشده است.")
        
        st.divider()
        
        # ============================================================
        # 7. جدول کامل پاسخ‌ها
        # ============================================================
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
        
    else:
        st.info("📭 هنوز هیچ پاسخی ثبت نشده است.")
else:
    if password:
        st.error("❌ رمز عبور اشتباه است!")
    else:
        st.info("🔑 برای مشاهده نتایج، رمز عبور را وارد کنید.")
