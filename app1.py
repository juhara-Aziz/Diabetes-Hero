import streamlit as st
import json
import os
from questions import LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5
import random
from gtts import gTTS

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# إنشاء الملفات إذا لم تكن موجودة
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# دوال مساعدة
def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# إعداد الصفحة
st.set_page_config(
    page_title="بطل السكري",
    page_icon="🦸🦸‍♀️",
    layout="wide"
)
st.markdown("""
<style>

/* الخلفية */

.stApp{
    background: linear-gradient(
        135deg,
        #E3F2FD 0%,
        #BBDEFB 25%,
        #C8E6C9 50%,
        #FFF9C4 75%,
        #FFE0B2 100%
    );

    background-attachment: fixed;
}

/* البانر */

.main-banner{
    background:linear-gradient(
    90deg,
    #4FC3F7,
    #81C784
    );

    padding:35px;
    border-radius:30px;
    margin-bottom:30px;
    text-align:center;
}

/* عنوان البانر */

.main-banner h1{
    font-size:56px;
    color:#0D47A1;
    font-weight:bold;
}

/* نص البانر */

.main-banner p{
    font-size:24px;
    color:#1565C0;
    font-weight:bold;
}

/* العناوين */

h1,h2,h3{
    color:#0D47A1 !important;
    text-align:center;
}

/* النصوص */

p,label,span{
    color:#333333;
}

/* السايد بار */

section[data-testid="stSidebar"]{
    background:#DFF3FF;
}

/* الأزرار */

.stButton > button{
    width:100%;
    height:50px;
    border-radius:15px;
    background:#4CAF50;
    color:white;
    border:none;
    font-size:18px;
    font-weight:bold;
}

/* خانات الإدخال */

.stTextInput input{
    background:white !important;
    color:black !important;
    border:2px solid #4FC3F7 !important;
    border-radius:15px !important;
}

.stNumberInput input{
    background:white !important;
    color:black !important;
    border:2px solid #4FC3F7 !important;
    border-radius:15px !important;
}

.stSelectbox div[data-baseweb="select"]{
    background:white !important;
    color:black !important;
    border-radius:15px !important;
}

/* البطاقات */

.card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-banner">
<h1>🦸‍♂️⭐ بطل السكري ⭐🦸‍♀️</h1>
<p>كل خطوة صغيرة تقربك من أن تصبح بطلاً حقيقياً 🌈</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style='text-align:center;font-size:45px;margin-bottom:20px'>
🩸 💉 🍎 🧃 🏃 ⭐
</div>
""", unsafe_allow_html=True)



# الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# قبل تسجيل الدخول
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "القائمة",
        ["الرئيسية", "تسجيل مستخدم", "تسجيل دخول"]
    )

    if menu == "الرئيسية":
        st.header("مرحباً بك في بطل السكري")
        st.write("""
        تطبيق تعليمي للأطفال المصابين بالسكري.

        ✅ تعلم بطريقة ممتعة
        ✅ مستويات تعليمية
        ✅ شارات وإنجازات
        ✅ متابعة التقدم
        """)

    elif menu == "تسجيل مستخدم":

        st.header("إنشاء حساب جديد")

        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        child_name = st.text_input("اسم الطفل")
        age = st.number_input("العمر", 1, 18)

        role = st.selectbox(
            "نوع الحساب",
            ["طفل", "ولي أمر"]
        )

        linked_child = ""

        if role == "ولي أمر":
            linked_child = st.text_input(
                "اسم مستخدم الطفل"
            )

        if st.button("إنشاء الحساب"):

            users = load_users()

            exists = any(
                u["username"] == username
                for u in users
            )

            if exists:
                st.error("اسم المستخدم مستخدم مسبقاً")

            else:

                users.append({
                    "username": username,
                    "password": password,
                    "child_name": child_name,
                    "age": age,
                    "role": role,
                    "linked_child": linked_child
                })

                save_users(users)

                st.success("تم إنشاء الحساب بنجاح")
                                

    elif menu == "تسجيل دخول":


    

        st.header("تسجيل الدخول")

        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")

        if st.button("دخول"):

            users = load_users()

            user = None

            for u in users:
                if (
                    u["username"] == username
                    and u["password"] == password
                ):
                    user = u
                    break

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("بيانات الدخول غير صحيحة")

# دالة عرض أي مستوى
def show_level(level_name, questions, user):

    child_name = user["child_name"]

    st.header(f"📚 {level_name}")

    st.info(
        f"🦸‍♂️ هيا يا {child_name}! أكمل التحدي لتصبح بطل السكري الحقيقي ⭐"
    )

    answers = []

    for i, q in enumerate(questions):

        question_text = q["question"]

        if level_name == "المستوى الخامس":
            question_text = question_text.replace(
                "البطل",
                 child_name
            )

        audio_file = f"audio_{level_name}_{i}.mp3"

        audio_text = f"{question_text}. "
        for option in q["options"]:
            audio_text += option + ". "
        tts = gTTS(
            text=audio_text,
            lang="ar"
            )

        tts.save(audio_file)

        col1, col2 = st.columns([8, 1])

        with col1:

            answer = st.radio(
                question_text,
                q["options"],
                index=None,
                key=f"{level_name}_{i}"
            )

        with col2:
            if st.button(
                "🔊",
                key=f"audio_{level_name}_{i}"
            ):

                with open(audio_file, "rb") as audio:
                    st.audio(audio.read())

        answers.append(answer)
    if st.button(f"إنهاء {level_name}"):
        correct = 0
        for ans, q in zip(answers, questions):
            if ans == q["answer"]:
                correct += 1
            score = int((correct / len(questions)) * 100)

        # حفظ التقدم
            progress = load_progress()

            if user["username"] not in progress:
                 progress[user["username"]] = {}

            progress[user["username"]][level_name] = score
            save_progress(progress)
            st.success(
            f"🎉 أحسنت يا {child_name}! درجتك {score}%"
            )

        
            if score >= 80:
                badge = ""
                if level_name == "المستوى الأول":
                    badge = "🏅 بطل العادات الصحية"

                elif level_name == "المستوى الثاني":
                    badge = "🏅 بطل الكربوهيدرات الذكي"

                elif level_name == "المستوى الثالث":
                    badge = "🏅 بطل القرار الصحيح"

                elif level_name == "المستوى الرابع":
                    badge = "🏅 بطل الممارسات الصحية"

                elif level_name == "المستوى الخامس":
                    badge = "👑 بطل السكري"

                st.balloons()
                st.success(
                    f"🎉 مبروك يا {child_name}! حصلت على الشارة:\n\n{badge}"
                )
                st.success(f"🏆 رائع يا {child_name}! تم فتح المستوى التالي."
                )
            else:
                st.warning(
                "💪 حاول مرة أخرى للحصول على 80٪ أو أكثر."
            )


# بعد تسجيل الدخول
# بعد تسجيل الدخول
if st.session_state.logged_in:

    user = st.session_state.user
    role = user.get("role", "طفل")

    # ==================
    # لوحة ولي الأمر
    # ==================
    if role == "ولي أمر":

        st.header("👩 لوحة ولي الأمر")

        progress = load_progress()

        child_username = user.get(
            "linked_child",
            ""
        )

        user_progress = progress.get(
            child_username,
            {}
        )

        st.write(
            f"👦 اسم الطفل: {child_username}"
        )

        if user_progress:

            for level, score in user_progress.items():

                st.write(f"{level}: {score}%")
                st.progress(score / 100)

            avg = int(
                sum(user_progress.values())
                / len(user_progress)
            )

            st.metric(
                "التقدم العام",
                f"{avg}%"
            )

        else:
            st.info("لا توجد نتائج بعد")

        st.subheader("💡 نصيحة اليوم")

        tips = [
            "الالتزام بقياس السكر بانتظام يساعد على التحكم الأفضل بالسكري 🌟",
            "شرب الماء بانتظام عادة صحية مهمة لطفلك 💧",
            "النشاط البدني اليومي يساعد في الحفاظ على مستوى السكر ⚽",
            "احرص على توفير وجبات خفيفة صحية مثل الفواكه 🍎",
            "تعليم الطفل التعرف على أعراض انخفاض السكر مهم جداً 🚨",
             "الدعم النفسي والتشجيع يساعد الطفل على التعايش بثقة ❤️"
        ]
        st.info(random.choice(tips))

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # ==================
    # واجهة الطفل
    # ==================
    else:

        st.sidebar.success(
            f"مرحباً {user['child_name']} 🦸"
        )

        progress = load_progress()

        user_progress = progress.get(
            user["username"],
            {}
        )

        options = [
            "لوحة الطفل",
            "المستوى الأول"
        ]

        if user_progress.get("المستوى الأول", 0) >= 80:
            options.append("المستوى الثاني")

        if user_progress.get("المستوى الثاني", 0) >= 80:
            options.append("المستوى الثالث")

        if user_progress.get("المستوى الثالث", 0) >= 80:
            options.append("المستوى الرابع")

        if user_progress.get("المستوى الرابع", 0) >= 80:
            options.append("المستوى الخامس")

        options.append("تسجيل خروج")

        page = st.sidebar.selectbox(
            "اختر",
            options
        )

        if page == "لوحة الطفل":


            st.header("🏆 لوحة الطفل")

            score1 = user_progress.get("المستوى الأول", 0)
            score2 = user_progress.get("المستوى الثاني", 0)
            score3 = user_progress.get("المستوى الثالث", 0)
            score4 = user_progress.get("المستوى الرابع", 0)
            score5 = user_progress.get("المستوى الخامس", 0)

            total = int(
                (score1 + score2 + score3 + score4 + score5) / 5
            )

            st.metric(
                "التقدم العام",
                f"{total}%"
            )

            st.progress(total / 100)

            st.subheader("🏅 الشارات التي حصلت عليها")

            if score1 >= 80:
                st.success("🏅 بطل العادات الصحية")

            if score2 >= 80:
                st.success("🏅 بطل الكربوهيدرات الذكي")

            if score3 >= 80:
                st.success("🏅 بطل القرار الصحيح")

            if score4 >= 80:
                st.success("🏅 بطل الممارسات الصحية")

            if score5 >= 80:
                st.success("🏆 بطل السكري")

            if (
                score1 < 80 and
                score2 < 80 and
                score3 < 80 and
                score4 < 80 and
                score5 < 80
            ):

                st.info("لم تحصل على أي شارة بعد، أكمل المستويات أولاً ⭐")

        elif page == "المستوى الأول":

            show_level("المستوى الأول", LEVEL_1, user)

        elif page == "المستوى الثاني":
            show_level("المستوى الثاني", LEVEL_2, user)

        elif page == "المستوى الثالث":
            show_level("المستوى الثالث", LEVEL_3, user)

        elif page == "المستوى الرابع":
            show_level("المستوى الرابع", LEVEL_4, user)

        elif page == "المستوى الخامس":
            show_level("المستوى الخامس", LEVEL_5, user)

        elif page == "تسجيل خروج":

            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
