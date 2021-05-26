# Copyright (C) 2021 TeamDaisyX


# This file is part of Daisy (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import events, functions
from telethon.tl.types import ChatBannedRights

from DaisyX import BOT_ID
from DaisyX.function.telethonbasics import is_admin
from DaisyX.services.sql.night_mode_sql import (
    add_nightmode,
    get_all_chat_id,
    is_nightmode_indb,
    rmnightmode,
)
from DaisyX.services.telethon import tbot

CLEAN_GROUPS = False
hehes = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhehe = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)


@tbot.on(events.NewMessage(pattern="/nightmode (.*)"))
async def close_ws(event):

    if not event.is_group:
        await event.reply("You Can Only Nsfw Watch in Groups.")
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID):
        await event.reply("`lu bukan admin Tolol!`")
        return
    if await is_admin(event, event.message.sender_id):
        if (
            input_str == "on"
            or input_str == "On"
            or input_str == "ON"
            or input_str == "enable"
        ):
            if is_nightmode_indb(str(event.chat_id)):
                await event.reply("Grub sudah masuk mode malam.")
                return
            add_nightmode(str(event.chat_id))
            await event.reply(
                f"**Added Chat {event.chat.title} With Id {event.chat_id} To Database. Grub akan ditutup jam 18:00 WIB dan dibuka lagi jam 18:30 WIB. **"
            )
        elif (
            input_str == "off"
            or input_str == "Off"
            or input_str == "OFF"
            or input_str == "disable"
        ):

            if not is_nightmode_indb(str(event.chat_id)):
                await event.reply("Grub ini belum memasuki mode malam.")
                return
            rmnightmode(str(event.chat_id))
            await event.reply(
                f"**Removed Chat {event.chat.title} With Id {event.chat_id} From Database. Grub akan ditutup jam 18:00 WIB dan dibuka lagi jam 18:30 WIB.**"
            )
        else:
            await event.reply("ketik `/nightmode on` atau `/nightmode off` only")
    else:
        await event.reply("`lu bukan admin tolol!`")
        return


async def job_close():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                "`18:00 WIB, Group akan ditutup sampai jam 18:30.!` \n**Selamat menjalankan sholat maghrib bagi yang menjalankan ❤️** \n**Powered By @assistenrobot**",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=hehes
                )
            )
            if CLEAN_GROUPS:
                async for user in tbot.iter_participants(int(warner.chat_id)):
                    if user.deleted:
                        await tbot.edit_permissions(
                            int(warner.chat_id), user.id, view_messages=False
                        )
        except Exception as e:
            print(f"Maaf tidak bisa {warner} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=58)
scheduler.start()


async def job_open():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                "`06:00 Am, Group Is Opening.`\n**Powered By @DaisyXBot**",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=openhehe
                )
            )
        except Exception as e:
            print(f"Unable To Open Group {warner.chat_id} - {e}")


# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_open, trigger="cron", minute=30)
scheduler.start()

__mod_name__ = "Night Mode"

__help__ = """
<b> The Night mode </b>
Grub ditutup mulai 18.00 WIB dan dibuka 18.30 WIB
<i> Hanya untuk negara Asia (Indonesia Standard time)</i>

- /nightmode [ON/OFF]: Enable/Disable Night Mode.

"""
