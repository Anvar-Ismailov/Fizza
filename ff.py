import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAnimation
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler
)
import requests

TOKEN = "7179080851:AAGu_seX2xH6Q9WeY7tu6qT0i4BR6K1yje4" 



TERMS = {
    "инерция": "Инерция — дененің өз қозғалыс күйін сақтау қасиеті. Егер денеге сырттан күш әсер етпесе, дене өзінің бастапқы тыныштық күйін немесе түзу сызықты бірқалыпты қозғалысын сақтайды...",
    "жылдамдық": "Жылдамдық — қозғалыстағы дененің орын ауыстыруының уақытқа қатынасы. Бұл — векторлық шама...",
    "масса": "Масса — дененің инерциясының және гравитациялық өзара әрекеттестіктің өлшемі...",
    "күш": "Күш — денелердің қозғалысын немесе пішінін өзгертуге әсер ететін физикалық шама...",
    "үдеу": "Үдеу — дененің жылдамдығының уақыт бойынша өзгеру жылдамдығы...",
    "энергия": "Энергия — дененің жұмыс істеу қабілетін сипаттайтын скалярлық шама...",
    "кинетикалық энергия": "Кинетикалық энергия — қозғалыстағы дененің энергиясы. Ek = (mv²)/2...",
    "потенциалдық энергия": "Потенциалдық энергия — дененің орналасуына немесе серпімділік күйіне байланысты жинақталған энергия...",
    "импульс": "Импульс — дененің қозғалысын сипаттайтын векторлық шама. p = mv...",
    "қысым": "Қысым — бірлік ауданға түсірілген күш. P = F/S...",
    "тығыздық": "Тығыздық — заттың бірлік көлеміндегі массасы. Формула: ρ = m/V...",
    "жұмыс": "Жұмыс — күш әсерінен орын ауыстыру кезінде орындалатын физикалық шама...",
    "қуат": "Қуат — жұмыстың орындалу жылдамдығы. N = A/t...",
    "ом заңы": "Ом заңы — өткізгіштегі ток күші I өткізгіш ұштарындағы кернеуге U тура пропорционал, кедергіге R кері пропорционал: I = U/R...",
    "магнит өрісі": "Магнит өрісі — электр зарядтарының қозғалысы кезінде пайда болатын күш өрісі...",
    "электр өрісі": "Электр өрісі — электр зарядтарының айналасында пайда болатын күш өрісі...",
    "кернеу": "Кернеу — электр өрісіндегі екі нүктенің потенциалдар айырмасы...",
    "ток күші": "Ток күші — өткізгіштің көлденең қимасы арқылы өтетін электр зарядының уақытқа қатынасы...",
    "индукция": "Индукция — магнит өрісінің өзгерісі кезінде электр қозғаушы күштің пайда болуы...",
    "изотермиялық процесс": "Изотермиялық процесс — температура тұрақты сақталатын термодинамикалық процесс...",
    "изохорлық процесс": "Изохорлық процесс — көлем тұрақты, қысым мен температура өзгеретін процесс...",
    "изобаралық процесс": "Изобаралық процесс — қысым тұрақты, көлем мен температура өзгеретін процесс...",
    "радиоактивтілік": "Радиоактивтілік — тұрақсыз атом ядроларының өздігінен ыдырап, жаңа ядролар мен бөлшектер шығару қасиеті...",
    "атом": "Атом — химиялық элементтің ең кіші бөлшегі, ядро мен электрондардан тұрады...",
    "молекула": "Молекула — заттың қасиеттерін сақтайтын ең кіші бөлшек...",
    "электрон": "Электрон — теріс зарядталған элементар бөлшек, атом ядросын айнала қозғалады...",
    "фотон": "Фотон — жарықтың және электромагниттік толқынның элементар бөлшегі...",
    "толқын": "Толқын — кеңістікте тербеліс энергиясын тасымалдайтын процесс...",
    "интерференция": "Интерференция — екі немесе бірнеше толқын қабаттасқанда, күшейтілген және әлсіреген аймақтардың пайда болуы...",
    "дифракция": "Дифракция — толқынның кедергіні айналып өтуі немесе саңылаудан өткенде бағыттарының өзгеруі...",
    "поляризация": "Поляризация — жарықтың немесе басқа толқындардың белгілі бір бағытта тербелу қасиеті...",
    "энтропия": "Энтропия — жүйенің ретсіздік дәрежесін сипаттайтын шама...",
}

FORMULAS = {
    "жылдамдық": "v = s/t",
    "кинетикалық энергия": "Ek = (mv²)/2",
    "потенциалдық энергия": "Ep = mgh немесе Ep = (k*x²)/2",
    "қысым": "P = F/S, сұйықтықта: P = ρgh",
    "тығыздық": "ρ = m/V",
    "импульс": "p = mv",
    "жұмыс": "A = F·s·cos(α), электр жұмысы: A = UIt",
    "қуат": "N = A/t, N = UI",
    "ом заңы": "I = U/R",
    "ток күші": "I = q/t",
    "кернеу": "U = A/q",
    "идеал газ теңдеуі": "pV = nRT",
    "бойль-мариотт заңы": "pV = const",
    "гей-люссак заңы": "V/T = const",
    "шарль заңы": "p/T = const",
    "жиілік": "ν = 1/T",
    "толқын ұзындығы": "λ = v/ν",
    "фотон энергиясы": "E = hν",
    "радиоактивті ыдырау": "N = N₀·e^(−λt)",
    "салыстырмалылық": "E = mc²",
}

THEORIES = {
    "ньютон заңдары": "Ньютонның үш заңы — механиканың негізі...",
    "энергия сақталу заңы": "Тұйық жүйеде энергия жойылмайды және жоқтан пайда болмайды...",
    "архимед заңы": "Сұйыққа немесе газға батырылған денеге ығыстырылған сұйықтың салмағына тең көтеруші күш әсер етеді...",
    "ом заңы": "Электр тізбегіндегі ток күші кернеуге тура, кедергіге кері пропорционал: I = U/R...",
    "термодинамиканың бірінші заңы": "Жүйеге берілген жылу оның ішкі энергиясын өзгертуге және жұмыс істеуге жұмсалады...",
    "толқындық теория": "Жарық толқын ретінде таралады. Интерференция, дифракция, поляризация — толқындық қасиеттердің дәлелі...",
    "электромагниттік индукция": "Магнит ағыны өзгергенде тұйық тізбекте электр қозғаушы күш пайда болады (Фарадей заңы)...",
    "салыстырмалылық теориясы": "Эйнштейннің салыстырмалылық теориясы — кеңістік, уақыт және масса-энергияның өзара байланысын сипаттайды...",
}

EXPERIMENTS = {
    "Архимед тәжірибесі": "Архимед тәжірибесі — сұйыққа толық батырылған денеге әсер ететін көтеруші күшті көрсету...",
    "Галилей шары тәжірибесі": "Галилей шары тәжірибесі — вакуумда әртүрлі массалы денелердің бірдей үдеумен құлауын көрсету...",
    "Фарадей индукция тәжірибесі": "Фарадей тәжірибесі — магнит өрісі өзгергенде тұйық тізбекте электр тогының пайда болуын дәлелдейді...",
    "Джоуль жылу тәжірибесі": "Джоуль тәжірибесі — механикалық энергияның жылу энергиясына айналуын көрсетеді...",
    "Юнг тәжірибесі": "Юнг тәжірибесі — жарық интерференциясын көрсетуге арналған...",
    "Эрстед тәжірибесі": "Эрстед тәжірибесі — электр тогының магнит өрісін тудыратынын көрсетеді...",
    "Ньютон маятнигі": "Ньютон маятнигі — импульс пен энергия сақталу заңдарын көрсету...",
}

HELP = {
    "Bot пайдалану нұсқаулығы": "FIzBot-ты пайдалану үшін төменгі мәзірдегі бөлімдерді таңдаңыз...",
    "Формула іздеу көмегі": "Қажетті формуланы іздеу үшін формула атауын немесе физикалық құбылысты жазыңыз...",
    "Категориялар бойынша іздеу": "Ботта барлық мәліметтер 6 негізгі категорияға бөлінген...",
    "Сұрақ қою үлгілері": "Мысал сұрақтар:\n- Архимед заңы қалай дәлелденеді?\n- Жылдамдық пен үдеу айырмашылығы неде? ...",
}

CATEGORIES = {
    "Терминдер": "Физиканың негізгі ұғымдары мен сөздіктері...",
    "Формулалар": "Физикадағы негізгі формулалар мен олардың түсіндірмесі...",
    "Теориялар": "Физикадағы басты теориялар, заңдар, олардың ашылу тарихы...",
    "Тәжрибелер": "Тарихи және классикалық ғылыми тәжірибелер...",
    "Көмек": "Ботпен жұмыс істеу, формула немесе теория іздеу, категориялар бойынша сұраныс жасау...",
}

VIDEOS = {
    "Кинетикалық энергия": "https://youtu.be/58426pBfNow?si=3xa70q_nss-twhG0",
    "Инерция және Ньютон заңдары": "https://youtu.be/MFb8F_DbGNk?si=2cXP7Dz3627eKe3T",
    "Архимед заңы": "https://youtu.be/E56HmuL2TX0?si=ipPQXUHWtcq28lgX",
    "Энергия сақталу заңы": "https://youtu.be/I1ytuqPDjMM?si=tRnQqB8P0luaBRu8",
    "Толқындар және интерференция": "https://youtu.be/9L4NOXQpk34?si=TE5_iZ3fYtFiXPuT",
    "Электр тогы және Ом заңы": "https://youtu.be/C8r5UxMWZFs?si=FBPgca4m-53eeis3",
    "Қысым және гидростатика": "https://youtu.be/OuSjiNDT-94?si=NNW2OnrXVNa-ai3-",
    "Салыстырмалылық теориясы": "https://youtu.be/njw91NOOqY8?si=83Nt-sBb9M4qR26k",
    "Фотон, жарық және толқындық қасиеттері": "https://youtu.be/BwjNRBfNfts?si=dqd089eudwcaW1l1",
    "Фарадей индукция тәжірибесі": "https://youtu.be/DSEI3N-GMHw?si=xrIjNl48cU0gyhT8",
    "Жылдамдық пен үдеу": "https://youtu.be/recc-PvfPsY?si=2ucZbjVMWU43L6d4",
    "Молекулалық-кинетикалық теория": "https://youtu.be/WsiLxwMsX1c?si=9JeZIyC6l82Qq90G"
}

QUIZZES = [
    {
        "question": "Ньютонның бірінші заңы қалай аталады?",
        "options": ["Инерция заңы", "Әрекет және қарсы әрекет заңы", "Динамика заңы"],
        "answer": 0
    },
    {
        "question": "Энергия сақталу заңы қалай тұжырымдалады?",
        "options": [
            "Энергия жойылады",
            "Энергия сақталады және тек түрленеді",
            "Энергия массамен тең"
        ],
        "answer": 1
    },
    {
        "question": "Ньютонның бірінші заңы қалай аталады?",
        "options": ["Инерция заңы", "Әрекет және қарсы әрекет заңы", "Динамика заңы"],
        "answer": 0
    },
    {
        "question": "Ньютонның екінші заңы нені сипаттайды?",
        "options": ["Дене тыныштықта болады", "Күш пен үдеу арасындағы байланысты", "Әрекетке қарсы әрекет"],
        "answer": 1
    },
    {
        "question": "Ньютонның үшінші заңының мәні неде?",
        "options": ["Үдеу күшке тура пропорционал", "Дене өзінің күйін сақтайды", "Әрекетке тең және қарама-қарсы әрекет болады"],
        "answer": 2
    },
    {
        "question": "Инерция дегеніміз не?",
        "options": ["Дененің массасы", "Дененің қозғалысқа қарсыласуы", "Қысым"],
        "answer": 1
    },
    {
        "question": "Күштің өлшем бірлігі қандай?",
        "options": ["Джоуль", "Ньютон", "Ватт"],
        "answer": 1
    },
    {
        "question": "Денеге әрекет ететін күштер теңгерілген болса, дене не істейді?",
        "options": ["Қозғалысын өзгертеді", "Үдей қозғалады", "Жылдамдығын өзгертпей қозғалады немесе тыныштықта болады"],
        "answer": 2
    },
    {
        "question": "Масса нені сипаттайды?",
        "options": ["Дененің көлемін", "Дененің салмағын", "Инерция шамасын"],
        "answer": 2
    },
    {
        "question": "Гравитациялық күш неге тәуелді?",
        "options": ["Денелердің массасына және арақашықтығына", "Тек жылдамдыққа", "Температураға"],
        "answer": 0
    },
    {
        "question": "Үдеу мен масса арасындағы байланыс қандай?",
        "options": ["Тікелей пропорционал", "Кері пропорционал", "Байланыс жоқ"],
        "answer": 1
    },
    {
        "question": "1 Ньютон күш неге тең?",
        "options": ["1 кг/м²", "1 кг·м/с²", "1 м/с²"],
        "answer": 1
    }
]

RESOURCES = {
    "Кітаптар": [
        "1. Р. Фейнман. Фейнман лекциялары по физике.",
        "2. Д. Халидей, Р. Резник, К. Уокер. Физика.",
        "3. Л.Д. Ландау, Е.М. Лифшиц. Теоретическая физика."
    ],
    "Сайты": [
        "https://www.khanacademy.org/science/physics",
        "https://phys.org/",
        "https://www.fizmat.kz/"
    ],
    "Онлайн-курстар": [
        "Coursera: https://www.coursera.org/courses?query=physics",
        "edX: https://www.edx.org/learn/physics",
        "Stepik: https://stepik.org/catalog/search?query=физика"
    ]
}


USER_DATA = {}

FEEDBACK, = range(1)


# --- КЛАВИАТУРЫ ---

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Терминдер", callback_data='terms')],
        [InlineKeyboardButton("🔬 Теориялар", callback_data='theories')],
        [InlineKeyboardButton("📐 Формулалар", callback_data='formulas')],
        [InlineKeyboardButton("🧪 Тәжрибелер", callback_data='experiments')],
        [InlineKeyboardButton("🎬 Бейнелер", callback_data='videos')],
        [InlineKeyboardButton("📝 Квиз/Тест", callback_data='quiz')],
        [InlineKeyboardButton("📚 Ресурстар", callback_data='resources')],
        [InlineKeyboardButton("🌐 Wikipedia/Wolfram", callback_data='external')],
        [InlineKeyboardButton("✉️ Обратная связь", callback_data='feedback')],
        [InlineKeyboardButton("👤 Кабинет/Прогресс", callback_data='profile')],
        [InlineKeyboardButton("🗂 Категориялар", callback_data='categories')],
        [InlineKeyboardButton("🆘 Көмек", callback_data='help')],
        [InlineKeyboardButton("❓ Сұрақ қою", callback_data='ask')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Артқа", callback_data='back')]])


# --- ОБРАБОТЧИКИ ---

async def show_main_menu(update, context):
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "Сәлем! Мен FIzBot — физика бойынша көмекшіңізмін. Төменнен бөлімді таңдаңыз:",
            reply_markup=main_keyboard()
        )
    else:
        await update.message.reply_text(
            "Сәлем! Мен FIzBot — физика бойынша көмекшіңізмін. Төменнен бөлімді таңдаңыз:",
            reply_markup=main_keyboard()
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)

# Квиз
async def quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    index = USER_DATA.get(user_id, {}).get("quiz_index", 0)
    if index >= len(QUIZZES):
        await update.callback_query.edit_message_text(
            "Квиз аяқталды! Дұрыс жауаптар саны: {}\n\n".format(
                USER_DATA[user_id].get("quiz_score", 0)
            ),
            reply_markup=back_keyboard()
        )
        return
    q = QUIZZES[index]
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f'quiz_answer_{i}')] for i, opt in enumerate(q["options"])
    ]
    await update.callback_query.edit_message_text(
        q["question"],
        reply_markup=InlineKeyboardMarkup(keyboard + [[InlineKeyboardButton("🔙 Артқа", callback_data='back')]])
    )

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    index = USER_DATA.get(user_id, {}).get("quiz_index", 0)
    answer = int(query.data.split("_")[-1])
    correct = QUIZZES[index]["answer"]
    score = USER_DATA.get(user_id, {}).get("quiz_score", 0)
    if answer == correct:
        result = "✅ Дұрыс!"
        score += 1
    else:
        result = "❌ Қате! Дұрыс жауап: {}".format(QUIZZES[index]["options"][correct])
    USER_DATA.setdefault(user_id, {})["quiz_score"] = score
    USER_DATA[user_id]["quiz_index"] = index + 1
    await query.edit_message_text(result, reply_markup=back_keyboard())
    await quiz_handler(update, context)

# Ресурсы
async def resources_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "<b>Пайдалы ресурстар:</b>\n\n"
    for section, lst in RESOURCES.items():
        text += f"<b>{section}:</b>\n"
        text += "\n".join(lst) + "\n\n"
    await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=back_keyboard())


# Профиль/прогресс
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    quiz_score = USER_DATA.get(user_id, {}).get("quiz_score", 0)
    quiz_index = USER_DATA.get(user_id, {}).get("quiz_index", 0)
    history = USER_DATA.get(user_id, {}).get("history", [])
    bookmarks = USER_DATA.get(user_id, {}).get("bookmarks", [])
    text = (
        f"👤 <b>Сіздің кабинетіңіз:</b>\n"
        f"📝 Квиз нәтижесі: {quiz_score} дұрыс жауап (барлығы {len(QUIZZES)} сұрақ)\n"
        f"⭐️ Сақталған сұраныстар: {len(bookmarks)}\n"
        f"📜 Сұраныстар тарихы (соңғы 5):\n" +
        ("\n".join(history[-5:]) if history else "Жоқ")
    )
    await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=back_keyboard())

# Обратная связь
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "✉️ Өз ұсынысыңызды, сұрағыңызды немесе шағымыңызды жазыңыз. Сообщение будет передано разработчику.",
        reply_markup=back_keyboard()
    )
    return FEEDBACK

async def feedback_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logging.info(f"Feedback from {user.username} ({user.id}): {update.message.text}")
    await update.message.reply_text("✅ Спасибо! Ваше сообщение отправлено разработчику.", reply_markup=back_keyboard())
    return ConversationHandler.END

# Wikipedia
async def external_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "🌐 Поиск по Wikipedia. Введите ваш физический вопрос или термин:"
        "\n\nПример: масса электрона, закон Архимеда, энергия фотона и т.п.",
        reply_markup=back_keyboard()
    )
    context.user_data["external"] = True


async def visual_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    name = query.data.replace("visual_", "")
    await query.answer()

# Кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'terms':
        text = "Терминдер тізімі:\n" + "\n".join([f"- {t}" for t in TERMS])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'theories':
        text = "Теориялар тізімі:\n" + "\n".join([f"- {t}" for t in THEORIES])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'formulas':
        text = "Формулалар тізімі:\n" + "\n".join([f"- {t}" for t in FORMULAS])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'experiments':
        text = "Тәжрибелер тізімі:\n" + "\n".join([f"- {t}" for t in EXPERIMENTS])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'videos':
        text = "🎬 Физика бейнелері мен анимациялар:\n\n"
        for name, url in VIDEOS.items():
            text += f"▪️ <a href=\"{url}\">{name}</a>\n"
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=back_keyboard(), disable_web_page_preview=False)
    elif query.data == 'help':
        text = "Көмек бөлімдері:\n" + "\n".join([f"- {t}" for t in HELP])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'categories':
        text = "Категориялар тізімі:\n" + "\n".join([f"- {t}" for t in CATEGORIES])
        await query.edit_message_text(text, reply_markup=back_keyboard())
    elif query.data == 'ask':
        await query.edit_message_text("Сұрағыңызды жазыңыз. Мысалы: инерция деген не?", reply_markup=back_keyboard())
    elif query.data == 'back':
        await show_main_menu(update, context)
    elif query.data == 'quiz':
        user_id = update.effective_user.id
        USER_DATA[user_id] = {"quiz_index": 0, "quiz_score": 0}
        await quiz_handler(update, context)
    elif query.data.startswith('quiz_answer_'):
        await handle_quiz_answer(update, context)
    elif query.data == 'resources':
        await resources_handler(update, context)
    elif query.data == 'profile':
        await profile_handler(update, context)
    elif query.data == 'feedback':
        return await feedback_start(update, context)
    elif query.data == 'external':
        await external_handler(update, context)
    elif query.data.startswith('visual_'):
        await visual_show(update, context)

# Сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    user_id = update.effective_user.id

    # Wikipedia API
    if context.user_data.get("external"):
        context.user_data["external"] = False
        url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{text.replace(' ', '_')}"
        r = requests.get(url)
        if r.ok and 'extract' in r.json():
            summary = r.json()['extract']
            reply = f"🌐 <b>Wikipedia:</b>\n{summary}"
        else:
            reply = "Извините, по вашему запросу Wikipedia не дала результата. Попробуйте другой термин."
        await update.message.reply_text(reply, parse_mode="HTML", reply_markup=back_keyboard())
        return

    reply = None
    if text in TERMS:
        reply = f"📚 <b>{text.title()}</b>:\n{TERMS[text]}"
    elif text in THEORIES:
        reply = f"🔬 <b>{text.title()}</b>:\n{THEORIES[text]}"
    elif text in FORMULAS:
        reply = f"📐 <b>{text.title()}</b>:\n{FORMULAS[text]}"
    elif text in EXPERIMENTS:
        reply = f"🧪 <b>{text.title()}</b>:\n{EXPERIMENTS[text]}"
    elif text in VIDEOS:
        reply = f"🎬 <b>{text.title()}</b>:\n<a href=\"{VIDEOS[text]}\">{VIDEOS[text]}</a>"
    elif text in HELP:
        reply = f"🆘 <b>{text.title()}</b>:\n{HELP[text]}"
    elif text in CATEGORIES:
        reply = f"🗂 <b>{text.title()}</b>:\n{CATEGORIES[text]}"
    else:
        found = False
        for dct, emoji in [
            (TERMS, "📚"), (THEORIES, "🔬"), (FORMULAS, "📐"),
            (EXPERIMENTS, "🧪"), (VIDEOS, "🎬"), (HELP, "🆘"), (CATEGORIES, "🗂")
        ]:
            for key in dct:
                if text in key or key in text:
                    if dct is VIDEOS:
                        reply = f"{emoji} <b>{key.title()}</b>:\n<a href=\"{dct[key]}\">{dct[key]}</a>"
                    else:
                        reply = f"{emoji} <b>{key.title()}</b>:\n{dct[key]}"
                    found = True
                    break
            if found:
                break
        if not reply:
            reply = "Кешіріңіз, бұл сұраныс бойынша ақпарат табылмады. Басқа сұрақ қойып көріңіз немесе мәзірді қолданыңыз."

    # Сохраняем историю пользователя
    USER_DATA.setdefault(user_id, {}).setdefault("history", []).append(text)
    if len(USER_DATA[user_id]["history"]) > 20:
        USER_DATA[user_id]["history"] = USER_DATA[user_id]["history"][-20:]

    await update.message.reply_text(reply, parse_mode="HTML", reply_markup=back_keyboard(), disable_web_page_preview=False)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    feedback_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(feedback_start, pattern='^feedback$')],
        states={
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_receive)]
        },
        fallbacks=[CallbackQueryHandler(show_main_menu, pattern='^back$')]
    )
    app.add_handler(feedback_conv)
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот іске қосылды!")
    app.run_polling()

if __name__ == "__main__":
    main()