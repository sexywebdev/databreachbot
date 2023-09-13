import logging
from telegram import __version__ as TG_VER
from telegram.ext import filters, Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler
from telegram import Update
import telegram
import requests
import json
from telegram.constants import ParseMode
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    userid = str(update.effective_user.id)
    db = open("db.json")
    dbf = json.load(db)
    db.close()
    if userid not in dbf.keys():
        try:
            appendx = {userid: {"limit": 3}}
            with open('db.json', "r+") as filex:
                usx = json.load(filex)
                usx.update(appendx)
                filex.seek(0)
                json.dump(usx, filex, indent=4)
                filex.close()
                db = open('db.json')
                dbf = json.load(db)
                dbf.close()
        except:
            pass
        finally:
            custom_keyboard = [['My Profile 👤'], 
                    ['Help 🆘 & About ℹ️']]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
            await update.message.reply_text(f"*Hello {user.first_name}!*\nSend email get list of breached site and password as well!", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Export DB."""
    userid = update.effective_user.id
    if userid == 1248688275:
        document = open('db.json', 'rb')
        await context.bot.send_document(chat_id=userid, document=document, caption="User DataBase")
        document = open('data.json', 'rb')
        await context.bot.send_document(chat_id=userid, document=document, caption="Data DataBase")


async def help_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help & about."""
    await update.message.reply_text("The bot collects data from a variety of sources, such as dark web forums, social media, and news articles. It can then analyze this data to identify potential data leaks. The bot can also be used to notify users of potential data leaks. This can be done by sending messages to users, or by creating an alert system.", parse_mode=ParseMode.MARKDOWN)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistic."""
    db = open("db.json")
    dbf = json.load(db)
    db.close()
    userid = update.effective_user.id
    if userid == 1248688275:
        c = 0
        for _ in dbf.keys():
            c += 1
        await update.message.reply_text(f"*Statistics*\n\nUsers: {c}", parse_mode=ParseMode.MARKDOWN)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast to users."""
    userid = update.effective_user.id
    if userid == Enter USER ID:
        db = open("db.json")
        dbf = json.load(db)
        db.close()
        msg = update.message.text
        if msg != "/broadcast":
            msg = msg.replace('/broadcast ', '')
            for uid in dbf.keys():
                await context.bot.send_message(chat_id=uid, text=msg)
        else:
            await update.message.reply_text("Please, add a message content to broadcast!")

async def core(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text
    userid = update.effective_user.id
    if '@' in email:
        db = open("db.json")
        dbf = json.load(db)
        db.close()
        msg = ''
        res = requests.get(f" ENTER API KEY HERE ").json()
        if dbf[str(userid)]['limit'] > 0:
            

            if res['success'] == True:
                if res['found'] > 0:
                    
                    for site in res['result']:
                        for src in site['sources']:
                            msg += f"{src}\n"
                        msg += f"Credential: {site['line']}\nLast Breached: {site['last_breach']}\n\n"
                    with open("db.json", "r+") as dmbf:
                        dbf[str(userid)]['limit'] = dbf[str(userid)]['limit'] - 1
                        json.dump(dbf, dmbf, indent=4)
                        dmbf.close()
                        db = open("db.json")
                        dbf = json.load(db)
                        db.close()
                            
                    await update.message.reply_text(msg)
                else:
                    await update.message.reply_text("Not breached!")
            else:
                await update.message.reply_text("Not breached!")
        else:
            await update.message.reply_text("Limit exceeded!")



async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db = open("db.json")
    dbf = json.load(db)
    db.close()
    userid = update.effective_user.id
    await update.message.reply_text(f"*Limit:  {dbf[str(userid)]['limit']}*", parse_mode=ParseMode.MARKDOWN)


def main() -> None:
    application = Application.builder().token("").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("db", db))

    application.add_handler(MessageHandler(filters.Regex(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$"), core))

    application.add_handler(MessageHandler(filters.Regex('My Profile 👤') & ~filters.COMMAND, profile))
    application.add_handler(MessageHandler(filters.Regex('Help 🆘 & About ℹ️') & ~filters.COMMAND, help_about))


    application.run_polling()


if __name__ == "__main__":
    main()
