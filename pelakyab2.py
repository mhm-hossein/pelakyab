from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, InlineQueryHandler
import re

# دیکشنری شامل کد شهرها
city_codes = {
    "15": "تبریز 🏙️ (آذربایجان شرقی)",
    "35": "سایر شهرهای استان آذربایجان شرقی",
    "17": "ارومیه 🏙️ (آذربایجان غربی)",
    "37": "سایر شهرهای استان آذربایجان غربی",
    "91": "اردبیل 🏙️ و سایر شهرهای استان اردبیل",
    "53": "اصفهان 🏙️ (استان اصفهان)",
    "67": "سایر شهرهای استان اصفهان",
    "43": "سایر شهرهای استان اصفهان",
    "23": "سایر شهرهای استان اصفهان",
    "48": "کرج 🏙️ (البرز)",
    "78": "سایر شهرهای استان البرز با حرف 'ط'",
    "21": "سایر شهرهای استان البرز با حرف 'ص'",
    "98": "ایلام 🏙️ (استان ایلام)",
    "98": "سایر شهرهای استان ایلام",
    "48": "بوشهر 🏙️ (استان بوشهر)",
    "58": "سایر شهرهای استان بوشهر",
    "11": "تهران 🏙️ (استان تهران)",
    "22": "تهران 🏙️ (استان تهران)",
    "33": "تهران 🏙️ (استان تهران)",
    "44": "تهران 🏙️ (استان تهران)",
    "55": "تهران 🏙️ (استان تهران)",
    "66": "تهران 🏙️ (استان تهران)",
    "77": "تهران 🏙️ (استان تهران)",
    "88": "تهران 🏙️ (استان تهران)",
    "99": "تهران 🏙️ (استان تهران)",
    "01": "تهران 🏙️ (استان تهران)",
    "05": "تهران 🏙️ (استان تهران)",
    "09": "تهران 🏙️ (استان تهران)",
    "38": "سایر شهرهای استان تهران",
    "78": "سایر شهرهای استان تهران",
    "21": "سایر شهرهای استان تهران",
    "71": "شهرکرد 🏙️ (چهارمحال و بختیاری)",
    "81": "سایر شهرهای استان چهارمحال و بختیاری",
    "26": "بنجورد 🏙️ (خراسان شمالی)",
    "74": "سایر شهرهای استان خراسان شمالی با حرف 'ج'",
    "12": "مشهد 🏙️ (خراسان رضوی)",
    "36": "مشهد 🏙️ (خراسان رضوی)",
    "74": "مشهد 🏙️ (خراسان رضوی)",
    "42": "سایر شهرهای استان خراسان رضوی",
    "52": "بیرجند 🏙️ (خراسان جنوبی)",
    "14": "اهواز 🏙️ (خوزستان)",
    "24": "سایر شهرهای استان خوزستان",
    "34": "سایر شهرهای استان خوزستان",
    "87": "زنجان 🏙️ (زنجان)",
    "97": "سایر شهرهای استان زنجان",
    "86": "سمنان 🏙️ (سمنان)",
    "96": "سایر شهرهای استان سمنان",
    "85": "زاهدان 🏙️ (سیستان و بلوچستان)",
    "95": "سایر شهرهای استان سیستان و بلوچستان",
    "93": "شیراز 🏙️ (فارس)",
    "63": "شیراز 🏙️ (فارس)",
    "83": "سایر شهرهای استان فارس",
    "73": "سایر شهرهای استان فارس",
    "79": "قزوین 🏙️ (قزوین)",
    "89": "سایر شهرهای استان قزوین",
    "16": "قم 🏙️ (استان قم)",
    "5": "سنندج 🏙️ (استان کردستان)",
    "61": "سایر شهرهای استان کردستان",
    "45": "کرمان 🏙️ (استان کرمان)",
    "65": "سایر شهرهای استان کرمان",
    "75": "سایر شهرهای استان کرمان",
    "19": "کرمانشاه 🏙️ (استان کرمانشاه)",
    "39": "سایر شهرهای استان کرمانشاه",
    "29": "سایر شهرهای استان کرمانشاه",
    "49": "یاسوج 🏙️ (استان کهگیلویه و بویراحمد)",
    "49": "سایر شهرهای استان کهگیلویه و بویراحمد",
    "59": "گرگان 🏙️ (استان گلستان)",
    "69": "سایر شهرهای استان گلستان",
    "46": "رشت 🏙️ (استان گیلان)",
    "56": "سایر شهرهای استان گیلان",
    "76": "سایر شهرهای استان گیلان",
    "31": "خرم آباد 🏙️ (استان لرستان)",
    "41": "سایر شهرهای استان لرستان",
    "62": "ساری 🏙️ (استان مازندران)",
    "82": "سایر شهرهای استان مازندران",
    "72": "سایر شهرهای استان مازندران",
    "92": "سایر شهرهای استان مازندران",
    "47": "اراک 🏙️ (استان مرکزی)",
    "57": "سایر شهرهای استان مرکزی",
    "84": "بندرعباس 🏙️ (استان هرمزگان)",
    "94": "سایر شهرهای استان هرمزگان",
    "18": "همدان 🏙️ (استان همدان)",
    "28": "سایر شهرهای استان همدان",
    "54": "یزد 🏙️ (استان یزد)",
    "44": "سایر شهرهای استان یزد"
}

# وضعیت‌های مکالمه
CODE_DETECTION, LIST_CITIES = range(2)

# دستور شروع (/start)
async def start(update: Update, context):
    keyboard = [
        ["🔍 تشخیص کد شهر"],
        ["📋 لیست کد شهرها"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "سلام! 😊\n"
        "به ربات «پلاک یاب» خوش آمدید.\n\n"
        "من می‌تونم با کد پلاک، اسم شهر رو بهتون بگم! 🚗\n"
        "برای شروع، یکی از گزینه‌های زیر رو انتخاب کنید:\n"
        "یا از حالت Inline استفاده کنید: @pelak_yab_bot کد_پلاک",
        reply_markup=reply_markup
    )
    return CODE_DETECTION

# دستور /about
async def about(update: Update, context):
    await update.message.reply_text(
        "🤖 درباره ربات «پلاک یاب»:\n\n"
        "این ربات به شما کمک می‌کنه تا با وارد کردن کد پلاک، اسم شهر مربوطه رو پیدا کنید! 🌍\n\n"
        "ویژگی‌های ربات:\n"
        "✅ تشخیص نام شهر با کد پلاک\n"
        "✅ نمایش لیست کامل کد پلاک‌ها\n"
        "✅ پشتیبانی از جستجو در گروه‌ها\n"
        "✅ قابلیت استفاده به صورت Inline\n\n"
        "برای استفاده از حالت Inline، کافیه آیدی ربات رو در هر چتی تایپ کنید:\n"
        "@pelak_yab_bot کد_پلاک\n\n"
        "سازنده ربات: @mhm_moz 🧑‍💻\n"
        "با تشکر از حمایت شما! ❤️"
    )

# دستور /cancel
async def cancel(update: Update, context):
    await update.message.reply_text(
        "عملیات لغو شد. 😊\n"
        "برای شروع دوباره، دستور /start رو ارسال کنید."
    )
    return CODE_DETECTION

# تشخیص کد شهر
async def detect_city_code(update: Update, context):
    user_input = update.message.text.strip()
    if user_input.isdigit() and len(user_input) == 2:
        city_name = city_codes.get(user_input, None)
        if city_name:
            await update.message.reply_text(
                f"🎉 کد پلاک {user_input} مربوط به {city_name} هست!"
            )
        else:
            await update.message.reply_text(
                "❌ متاسفانه کد پلاک وارد شده معتبر نیست!"
            )
    else:
        await update.message.reply_text(
            "⚠️ لطفاً فقط یک عدد دو رقمی وارد کنید!"
        )
    return CODE_DETECTION

# نمایش لیست کد شهرها با دکمه‌های شیشه‌ای
async def list_city_codes(update: Update, context):
    query = update.callback_query
    if query:
        await query.answer()
        page_number = int(query.data.split("_")[-1])
    else:
        page_number = 0

    # محاسبه محدوده شهرها برای صفحه فعلی
    start_index = page_number * 5
    end_index = start_index + 5
    cities_subset = list(city_codes.items())[start_index:end_index]

    # ساخت دکمه‌های شیشه‌ای برای شهرها
    keyboard = []
    for code, city in cities_subset:
        keyboard.append([InlineKeyboardButton(f"{code} | {city}", callback_data=f"city_{code}")])

    # اضافه کردن دکمه‌های صفحه‌بندی
    pagination_buttons = []
    if page_number > 0:
        pagination_buttons.append(InlineKeyboardButton("◀️ قبلی", callback_data=f"list_cities_{page_number - 1}"))
    if end_index < len(city_codes):
        pagination_buttons.append(InlineKeyboardButton("بعدی ▶️", callback_data=f"list_cities_{page_number + 1}"))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(
            "📋 لیست کد پلاک‌ها:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "📋 لیست کد پلاک‌ها:",
            reply_markup=reply_markup
        )
    return LIST_CITIES

# مدیریت کلیک روی دکمه‌های شیشه‌ای
async def handle_inline_buttons(update: Update, context):
    query = update.callback_query
    await query.answer()

    # استخراج کد پلاک از دکمه
    data = query.data
    if data.startswith("city_"):
        city_code = data.split("_")[1]
        city_name = city_codes.get(city_code, "متاسفانه اطلاعاتی برای این کد پلاک وجود ندارد!")
        await query.edit_message_text(
            f"🎉 کد پلاک {city_code} مربوط به {city_name} هست!"
        )
        return CODE_DETECTION  # بازگشت به حالت اولیه

    elif data.startswith("list_cities_"):
        await list_city_codes(update, context)
        return LIST_CITIES  # بازگشت به حالت لیست شهرها

# مدیریت پیام‌های گروه
async def handle_group_messages(update: Update, context):
    message = update.message
    text = message.text.strip()

    # الگوی مورد نظر: "پلاک" + فاصله + عدد دو رقمی
    pattern = r"^پلاک\s+(\d{2})$"
    match = re.match(pattern, text)

    if match:
        # استخراج کد پلاک از متن
        city_code = match.group(1)
        city_name = city_codes.get(city_code, None)

        if city_name:
            # ریپلای به پیام کاربر
            await message.reply_text(
                f"🎉 کد پلاک {city_code} مربوط به {city_name} هست!",
                reply_to_message_id=message.message_id
            )
        else:
            await message.reply_text(
                "❌ متاسفانه کد پلاک وارد شده معتبر نیست!",
                reply_to_message_id=message.message_id
            )

# مدیریت Inline Query
async def inline_query(update: Update, context):
    query = update.inline_query.query
    if not query.isdigit() or len(query) != 2:
        results = [InlineQueryResultArticle(
            id="invalid",
            title="کد پلاک معتبر نیست!",
            input_message_content=InputTextMessageContent("لطفاً یک کد پلاک دو رقمی وارد کنید.")
        )]
    else:
        city_name = city_codes.get(query, "متاسفانه اطلاعاتی برای این کد پلاک وجود ندارد!")
        results = [InlineQueryResultArticle(
            id=query,
            title=f"کد پلاک {query}",
            input_message_content=InputTextMessageContent(f"🎉 کد پلاک {query} مربوط به {city_name} هست!")
        )]

    await update.inline_query.answer(results)

# مدیریت خطاها
async def error_handler(update: Update, context):
    """Log the error and send a message to the user."""
    print(f"An error occurred: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "⚠️ متاسفانه خطایی رخ داده است. لطفاً دوباره تلاش کنید!"
        )

# اجرای ربات
def main():
    token = "8152266250:AAGE7K9BHx431Hd7Gcdof3Uv_9cs3ripjJE"

    # ساخت Application با استفاده از ApplicationBuilder
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CODE_DETECTION: [
                MessageHandler(filters.Regex("^🔍 تشخیص کد شهر"), detect_city_code),
                MessageHandler(filters.Regex("^📋 لیست کد شهرها"), list_city_codes),
                MessageHandler(filters.TEXT & ~filters.COMMAND, detect_city_code),
            ],
            LIST_CITIES: [
                CallbackQueryHandler(handle_inline_buttons),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("cancel", cancel),
        ],
        per_chat=True,
        per_message=False,
    )

    # مدیریت پیام‌های گروه
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_group_messages))

    # مدیریت مکالمه‌ای
    application.add_handler(conv_handler)

    # مدیریت Inline Query
    application.add_handler(InlineQueryHandler(inline_query))

    # دستور /about
    application.add_handler(CommandHandler("about", about))

    # مدیریت خطاها
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == "__main__":
    main()