# (c) @AbirHasan2005

import re
import os
import time

from bot import Bot
from presets import Presets
from base64 import b64encode
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def ForceSub(client: Bot, message: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @AbirHasan2005.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param client: Pass Bot.
    :param message: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    
    try:
        invite_link = await client.create_chat_invite_link(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, message)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {Config.UPDATES_CHANNEL}\n\nError: {err}\n\nContact Support Group: https://t.me/DevsZone")
        return 200
    try:
        user = await client.get_chat_member(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL), user_id=message.from_user.id)
        if user.status == "kicked":
            await client.send_message(
                chat_id=message.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/DevsZone).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=message.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await client.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=message.message_id
        )
        return 400
    except FloodWait as e:
        await time.sleep(e.x)
        fix_ = await ForceSub(client, message)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/DevsZone")
        return 200
