import os
import json
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from calendar_planner import create_calendar
from generator import generate_post
from publisher import publish_post
from image import generate_image

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

CALENDAR_FILE = "calendar.json"
NICHE_FILE = "niche.json"
STATUS_FILE = "bot_status.json"

def load_niche():
    try:
        with open(NICHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"niche": "", "issues": [], "language": "English"}

def save_niche(data):
    with open(NICHE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_calendar():
    try:
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_calendar(data):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_bot_active():
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f).get("active", True)
    except:
        return True

def set_bot_active(active: bool):
    with open(STATUS_FILE, "w") as f:
        json.dump({"active": active}, f)

def parse_message_fields(text):
    """Parse any combination of niche/language/problem from a message"""
    result = {}
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        line_lower = line.lower()

        if line.startswith("নিশ:"):
            result["niche"] = line.replace("নিশ:", "").strip()
        elif line.startswith("সমস্যা:"):
            result["issues"] = [i.strip() for i in line.replace("সমস্যা:", "").strip().split(",")]
        elif line.startswith("ভাষা:"):
            result["language"] = line.replace("ভাষা:", "").strip()
        elif line_lower.startswith("niche:") or line_lower.startswith("niche :"):
            result["niche"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("language:") or line_lower.startswith("language :"):
            result["language"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("problem:") or line_lower.startswith("issue:"):
            result["issues"] = [i.strip() for i in line.split(":", 1)[1].strip().split(",")]

    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_bot_active(True)
    text = """
🤖 *FB Auto Poster Bot চালু হয়েছে!*

*Commands:*
/setniche - নিশ সেট করো
/calendar - ৭ দিনের calendar তৈরি করো
/viewcalendar - Calendar দেখো
/postnow - এখনই একটা post করো
/status - Bot এর status দেখো
/end - Bot বন্ধ করো

*একসাথে সেট করো:*
```
niche: Email Marketing
language: Bangla
```

অথবা আলাদাভাবে:
`ভাষা: Bangla` বা `language: English`
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_bot_active(False)
    await update.message.reply_text(
        "⏹️ *Bot বন্ধ হয়েছে।*\n\nআবার চালু করতে /start দাও।",
        parse_mode="Markdown"
    )

async def set_niche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active():
        return
    if context.args:
        niche = " ".join(context.args)
        data = load_niche()
        data["niche"] = niche
        save_niche(data)
        await update.message.reply_text(
            f"✅ নিশ সেট: *{niche}*\n\nএখন /calendar দাও!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "📌 Example:\n`/setniche Digital Marketing`\nঅথবা:\n`niche: AI`",
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active():
        return

    text = update.message.text.strip()

    # Parse all fields from the message
    fields = parse_message_fields(text)

    if fields:
        data = load_niche()
        changed = []

        if "niche" in fields:
            data["niche"] = fields["niche"]
            changed.append(f"📌 নিশ: {fields['niche']}")

        if "language" in fields:
            data["language"] = fields["language"]
            changed.append(f"🌐 ভাষা: {fields['language']}")

        if "issues" in fields:
            data["issues"] = fields["issues"]
            changed.append(f"⚠️ সমস্যা: {', '.join(fields['issues'])}")

        if changed:
            save_niche(data)
            response = "✅ *সেট হয়েছে!*\n\n" + "\n".join(changed)

            if "niche" in fields:
                response += "\n\nএখন /calendar দাও!"
            elif "language" in fields:
                response += f"\n\n/postnow দিলে {data['language']} তে content আসবে!"

            await update.message.reply_text(response, parse_mode="Markdown")

async def make_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active():
        return

    niche_data = load_niche()
    niche = niche_data.get("niche", "")
    if not niche:
        await update.message.reply_text(
            "❌ আগে নিশ সেট করো!\n\nExample: `niche: AI`",
            parse_mode="Markdown"
        )
        return

    await update.message.reply_text(
        f"⏳ *{niche}* এর জন্য ৭ দিনের calendar তৈরি হচ্ছে...",
        parse_mode="Markdown"
    )
    issues = niche_data.get("issues", [])

    try:
        calendar = await asyncio.to_thread(create_calendar, niche, issues)
        save_calendar(calendar)

        text = f"📅 *{niche} — ৭ দিনের Calendar*\n\n"
        for day in calendar:
            text += f"*Day {day['day']}:* {day['topic']}\n"
            text += f"_{day['tone']} | {day['content_type']}_\n\n"

        keyboard = [[
            InlineKeyboardButton("✅ Approve", callback_data="approve_calendar"),
            InlineKeyboardButton("🔄 Regenerate", callback_data="regenerate_calendar")
        ]]
        await update.message.reply_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def view_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active():
        return

    calendar = load_calendar()
    if not calendar:
        await update.message.reply_text("❌ কোনো calendar নেই। /calendar দিয়ে তৈরি করো।")
        return

    posted = sum(1 for d in calendar if d.get("posted"))
    text = f"📅 *Calendar ({posted}/{len(calendar)} posted):*\n\n"
    for day in calendar:
        status = "✅" if day.get("posted") else "⏳"
        text += f"{status} *Day {day['day']}:* {day['topic']}\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active():
        await update.message.reply_text("⏹️ Bot বন্ধ আছে। /start দিয়ে চালু করো।")
        return

    calendar = load_calendar()
    niche_data = load_niche()
    niche = niche_data.get("niche", "")
    language = niche_data.get("language", "English")

    if not calendar:
        await update.message.reply_text("❌ কোনো calendar নেই। /calendar দিয়ে তৈরি করো।")
        return

    next_day = None
    next_index = None
    for i, day in enumerate(calendar):
        if not day.get("posted"):
            next_day = day
            next_index = i
            break

    if not next_day:
        await update.message.reply_text("✅ সব posts শেষ! /calendar দিয়ে নতুন calendar বানাও।")
        return

    await update.message.reply_text(
        f"⏳ Content তৈরি হচ্ছে...\n📌 *{next_day['topic']}*\n🌐 Language: {language}",
        parse_mode="Markdown"
    )

    try:
        content = await asyncio.to_thread(
            generate_post, next_day['topic'], next_day['tone'], niche, language
        )
        preview = content[:500] + "..." if len(content) > 500 else content
        calendar[next_index]["content"] = content
        save_calendar(calendar)

        keyboard = [[
            InlineKeyboardButton("✅ Post করো", callback_data=f"confirm_post_{next_index}"),
            InlineKeyboardButton("🔄 Regenerate", callback_data=f"regen_post_{next_index}"),
            InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_post_{next_index}")
        ]]
        await update.message.reply_text(
            f"📝 *Preview (Day {next_day['day']}):*\n\n{preview}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    niche_data = load_niche()
    calendar = load_calendar()
    posted = sum(1 for d in calendar if d.get("posted"))
    active = is_bot_active()
    text = f"""
📊 *Bot Status*

{"🟢 Active" if active else "🔴 Stopped — /start দিয়ে চালু করো"}

📌 নিশ: {niche_data.get('niche') or 'সেট হয়নি'}
🌐 ভাষা: {niche_data.get('language', 'English')}
⚠️ সমস্যা: {', '.join(niche_data.get('issues', [])) or 'নেই'}
📅 Calendar: {posted}/{len(calendar)} posts সম্পন্ন
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "approve_calendar":
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("✅ Calendar approved! /postnow দিয়ে post শুরু করো।")

    elif data == "regenerate_calendar":
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("🔄 নতুন calendar তৈরি হচ্ছে...")
        niche_data = load_niche()
        try:
            calendar = await asyncio.to_thread(
                create_calendar, niche_data['niche'], niche_data.get('issues', [])
            )
            save_calendar(calendar)
            text = "📅 *নতুন Calendar:*\n\n"
            for day in calendar:
                text += f"*Day {day['day']}:* {day['topic']}\n_{day['tone']}_\n\n"
            keyboard = [[InlineKeyboardButton("✅ Approve", callback_data="approve_calendar")]]
            await query.message.reply_text(
                text, parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")

    elif data.startswith("confirm_post_"):
        index = int(data.split("_")[-1])
        calendar = load_calendar()

        if index >= len(calendar):
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("⚠️ Calendar reset হয়েছে। /postnow দিয়ে আবার চেষ্টা করো।")
            return

        day = calendar[index]
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("📤 Facebook এ post হচ্ছে...")

        try:
            content = day.get("content", "")
            image_path = None

            try:
                await query.message.reply_text("🎨 Image তৈরি হচ্ছে...")
                image_path = await asyncio.to_thread(generate_image, day['topic'])
                if image_path:
                    await query.message.reply_text("✅ Image ready!")
                else:
                    await query.message.reply_text("⚠️ Image হয়নি, text-only post হবে।")
            except Exception as e:
                await query.message.reply_text(f"⚠️ Image error: {e}\nText-only post হবে।")

            await asyncio.to_thread(publish_post, content, image_path)
            calendar[index]["posted"] = True
            calendar[index]["posted_at"] = str(datetime.now())
            save_calendar(calendar)

            await query.message.reply_text(
                f"✅ *Post সফল!*\n📌 {day['topic']}\n\nপরেরটার জন্য /postnow দাও।",
                parse_mode="Markdown"
            )

        except Exception as e:
            await query.message.reply_text(f"❌ Post failed: {e}")

    elif data.startswith("regen_post_"):
        index = int(data.split("_")[-1])
        calendar = load_calendar()

        if index >= len(calendar):
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("⚠️ Calendar reset হয়েছে। /postnow দিয়ে আবার চেষ্টা করো।")
            return

        day = calendar[index]
        niche_data = load_niche()
        language = niche_data.get("language", "English")
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("🔄 নতুন content তৈরি হচ্ছে...")
        try:
            content = await asyncio.to_thread(
                generate_post, day['topic'], day['tone'], niche_data.get('niche', ''), language
            )
            preview = content[:500] + "..." if len(content) > 500 else content
            calendar[index]["content"] = content
            save_calendar(calendar)
            keyboard = [[
                InlineKeyboardButton("✅ Post করো", callback_data=f"confirm_post_{index}"),
                InlineKeyboardButton("🔄 Regenerate", callback_data=f"regen_post_{index}"),
                InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_post_{index}")
            ]]
            await query.message.reply_text(
                f"📝 *নতুন Preview:*\n\n{preview}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")

    elif data.startswith("skip_post_"):
        index = int(data.split("_")[-1])
        calendar = load_calendar()

        if index >= len(calendar):
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("⚠️ Calendar reset হয়েছে। /postnow দিয়ে আবার চেষ্টা করো।")
            return

        calendar[index]["posted"] = True
        calendar[index]["skipped"] = True
        save_calendar(calendar)
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("⏭️ Skip হয়েছে। /postnow দিয়ে পরেরটা করো।")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(CommandHandler("setniche", set_niche))
    app.add_handler(CommandHandler("calendar", make_calendar))
    app.add_handler(CommandHandler("viewcalendar", view_calendar))
    app.add_handler(CommandHandler("postnow", post_now))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Bot চালু হয়েছে!")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
