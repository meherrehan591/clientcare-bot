from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5628303960

NAME, PHONE, EMAIL, REQUIREMENT = range(4)

menu = ReplyKeyboardMarkup(
    [
        ["🛍 Our Services", "💰 Pricing"],
        ["📦 Place an Order", "📞 Contact Support"],
        ["❓ FAQ"],
    ],
    resize_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to ClientCare Bot!\n\nChoose an option:",
        reply_markup=menu,
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 Place an Order":
        await update.message.reply_text("👤 Please enter your Name:")
        return NAME

    elif text == "🛍 Our Services":
        await update.message.reply_text(
            "🤖 We provide:\n\n"
            "• AI Telegram Bots\n"
            "• Business Automation\n"
            "• Custom Chatbots"
        )

    elif text == "💰 Pricing":
        await update.message.reply_text(
            "💰 Pricing:\n\n"
            "Basic - $20\n"
            "Pro - $50\n"
            "Premium - $100"
        )

    elif text == "📞 Contact Support":
        await update.message.reply_text(
            "📩 Contact:\n@meherrehan591"
        )

    elif text == "❓ FAQ":
        await update.message.reply_text(
            "❓ Frequently Asked Questions\n\n"
            "Q: How long does delivery take?\n"
            "A: Usually 1-3 days."
        )

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📱 Enter your Phone Number:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📧 Enter your Email:")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("📝 What do you need?")
    return REQUIREMENT

async def get_requirement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["requirement"] = update.message.text

    msg = f"""
📥 NEW ORDER RECEIVED

👤 Name: {context.user_data['name']}
📱 Phone: {context.user_data['phone']}
📧 Email: {context.user_data['email']}
📝 Requirement: {context.user_data['requirement']}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    await update.message.reply_text(
        "✅ Thanks! Your order has been submitted.",
        reply_markup=menu,
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Order cancelled.",
        reply_markup=menu,
    )
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.TEXT & filters.Regex("^📦 Place an Order$"),
            handle_menu,
        )
    ],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        REQUIREMENT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_requirement)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_menu,
    )
)

print("🤖 ClientCare Bot Running...")
app.run_polling()