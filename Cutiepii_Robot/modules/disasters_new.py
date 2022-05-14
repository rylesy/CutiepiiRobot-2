import html
import json
import os
from typing import Optional

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import CommandHandler
from telegram.helpers import mention_html
from telegram.ext import CallbackContext

from Cutiepii_Robot import CUTIEPII_PTB, OWNER_ID, DEV_USERS, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS
from Cutiepii_Robot.modules.helper_funcs.chat_status import dev_plus, sudo_plus, whitelist_plus
from Cutiepii_Robot.modules.log_channel import gloggable
from Cutiepii_Robot.modules.helper_funcs.extraction import extract_user
from Cutiepii_Robot.modules.sql import super_users_sql as sql


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        return "Nice try... Nope! Provide me an valid User ID."

    elif user_id == bot.id:
        return "This does not work that way."

    else:
        return None


@dev_plus
@gloggable
async def addsudo(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in SUDO_USERS:
        await message.reply_text("This member is already sudo")
        return ""
    if user_id in SUPPORT_USERS:
        await message.reply_text(
            "This user is already a support user. Promoting to sudo.")
        SUPPORT_USERS.remove(user_id)
    if user_id in WHITELIST_USERS:
        await message.reply_text(
            "This user is already a whitelisted user. Promoting to sudo.")
        WHITELIST_USERS.remove(user_id)
    sql.set_superuser_role(user_id, "sudos")
    SUDO_USERS.append(user_id)
    await update.effective_message.reply_text(
        "Successfully promoted {} to sudo!".format(
            user_member.user.first_name))
    return "<b>{}:</b>" \
           "\n#SUDO" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))


@sudo_plus
@gloggable
async def addsupport(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in DEV_USERS:
        await message.reply_text("Huh? he is more than support!")
        return ""
    if user_id in SUDO_USERS:
        if user.id in DEV_USERS:
            await message.reply_text(
                "This member is a sudo user. Demoting to support.")
            SUDO_USERS.remove(user_id)
        else:
            await message.reply_text("This user is already sudo")
            return ""
    if user_id in SUPPORT_USERS:
        await message.reply_text("This user is already a support user.")
        return ""
    if user_id in WHITELIST_USERS:
        await message.reply_text(
            "This user is already a whitelisted user. Promoting to support.")
        WHITELIST_USERS.remove(user_id)
    sql.set_superuser_role(user_id, "supports")
    SUPPORT_USERS.append(user_id)
    await update.effective_message.reply_text(
        "Successfully promoted {} to support!".format(
            user_member.user.first_name))
    return "<b>{}:</b>" \
           "\n#SUPPORT" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))


@sudo_plus
@gloggable
async def addwhitelist(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in DEV_USERS:
        await message.reply_text("Huh? he is more than whitelist!")
        return ""
    if user_id in SUDO_USERS:
        if user.id in DEV_USERS:
            await message.reply_text(
                "This member is a sudo user. Demoting to whitelist.")
            SUDO_USERS.remove(user_id)
        else:
            await message.reply_text("This user is already sudo")
            return ""
    if user_id in SUPPORT_USERS:
        await message.reply_text(
            "This user is already a support user. Demoting to whitelist.")
        SUPPORT_USERS.remove(user_id)
    if user_id in WHITELIST_USERS:
        await message.reply_text("This user is already a whitelisted user.")
        return ""
    sql.set_superuser_role(user_id, "whitelists")
    WHITELIST_USERS.append(user_id)
    await update.effective_message.reply_text(
        "Successfully promoted {} to whitelist!".format(
            user_member.user.first_name))
    return "<b>{}:</b>" \
           "\n#WHITELIST" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))


@dev_plus
@gloggable
async def removesudo(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in SUDO_USERS:
        await message.reply_text("Demoting to normal user")
        SUDO_USERS.remove(user_id)
        sql.remove_superuser(user_id)
        return "<b>{}:</b>" \
           "\n#UNSUDO" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))
    else:
        await message.reply_text("This user is not a sudo!")
        return ""


@sudo_plus
@gloggable
async def removesupport(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in SUPPORT_USERS:
        await message.reply_text("Demoting to normal user")
        SUPPORT_USERS.remove(user_id)
        sql.remove_superuser(user_id)
        return "<b>{}:</b>" \
           "\n#UNSUPPORT" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))
    else:
        await message.reply_text("This user is not a support user!")
        return ""


@sudo_plus
@gloggable
async def removewhitelist(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    user = update.effective_user
    user_id = extract_user(message, args)
    user_member = await update.effective_chat.get_member(user_id)
    reply = check_user_id(user_id, bot)
    if reply:
        await message.reply_text(reply)
        return ""
    if user_id in WHITELIST_USERS:
        await message.reply_text("Demoting to normal user")
        WHITELIST_USERS.remove(user_id)
        sql.remove_superuser(user_id)
        return "<b>{}:</b>" \
           "\n#UNWHITELIST" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(update.effective_chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))
    else:
        await message.reply_text("This user is not a whitelisted user!")
        return ""


@whitelist_plus
async def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    msg = "<b>Dev users:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        with contextlib.suppress(TelegramError):
            user = await bot.get_chat(user_id)
            msg += f"➛ {mention_html(user_id, user.first_name)}\n"
    await message.reply_text(msg, parse_mode=ParseMode.HTML)


@whitelist_plus
async def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    true_sudo = list(set(SUDO_USERS) - set(DEV_USERS))
    msg = "<b>Sudo users:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        with contextlib.suppress(TelegramError):
            user = await bot.get_chat(user_id)
            msg += f"➛ {mention_html(user_id, user.first_name)}\n"
    await message.reply_text(msg, parse_mode=ParseMode.HTML)


@whitelist_plus
async def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    msg = "<b>Support users:</b>\n"
    for each_user in SUPPORT_USERS:
        user_id = int(each_user)
        with contextlib.suppress(TelegramError):
            user = await bot.get_chat(user_id)
            msg += f"➛ {mention_html(user_id, user.first_name)}\n"
    await message.reply_text(msg, parse_mode=ParseMode.HTML)


@whitelist_plus
async def whitelistlist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    msg = "<b>Whitelist users:</b>\n"
    for each_user in WHITELIST_USERS:
        user_id = int(each_user)
        with contextlib.suppress(TelegramError):
            user = await bot.get_chat(user_id)
            msg += f"➛ {mention_html(user_id, user.first_name)}\n"
    await message.reply_text(msg, parse_mode=ParseMode.HTML)


__help__ = """
- /addsudo: adds a user as sudo
- /addsupport: adds a user as support
- /addwhitelist: adds a user as whitelist
- /removesudo: remove a sudo user
- /removesupport: remove support user
- /removewhitelist: remove a whitelist user
- /sudolist: lists all users which have sudo access to the bot
- /supportlist: lists all users which are allowed to gban, but can also be banned
- /whitelistlist: lists all users which cannot be banned, muted flood or kicked but can be manually banned by admins
"""

__mod_name__ = "Super Users"

SUDO_HANDLER = CommandHandler("addsudo", addsudo)
UNSUDO_HANDLER = CommandHandler("removesudo", removesudo)
SUPPORT_HANDLER = CommandHandler("addsupport", addsupport)
UNSUPPORT_HANDLER = CommandHandler("removesupport",
                                   removesupport)
WHITELIST_HANDLER = CommandHandler("addwhitelist",
                                   addwhitelist)
UNWHITELIST_HANDLER = CommandHandler("removewhitelist",
                                     removewhitelist)
DEVLIST_HANDLER = CommandHandler(("devlist"), devlist)
SUDOLIST_HANDLER = CommandHandler(("sudolist"), sudolist)
SUPPORTLIST_HANDLER = CommandHandler(("supportlist"),
                                     supportlist)
WHITELISTLIST_HANDLER = CommandHandler(("whitelistlist"),
                                       whitelistlist)

CUTIEPII_PTB.add_handler(SUDO_HANDLER)
CUTIEPII_PTB.add_handler(UNSUDO_HANDLER)
CUTIEPII_PTB.add_handler(SUPPORT_HANDLER)
CUTIEPII_PTB.add_handler(UNSUPPORT_HANDLER)
CUTIEPII_PTB.add_handler(WHITELIST_HANDLER)
CUTIEPII_PTB.add_handler(UNWHITELIST_HANDLER)

CUTIEPII_PTB.add_handler(DEVLIST_HANDLER)
CUTIEPII_PTB.add_handler(SUDOLIST_HANDLER)
CUTIEPII_PTB.add_handler(SUPPORTLIST_HANDLER)
CUTIEPII_PTB.add_handler(WHITELISTLIST_HANDLER)