# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

# (c) Shrimadhav U K - UniBorg
# Thanks to Prakasaka for porting.
# Thanks to laciamemeframe for optimization and translate

import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto
from userbot import CMD_HELP, REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY


@register(outgoing=True, pattern="^.remove(?: |$)(.*)")
async def kbg(remob):
    """ .rbg Удаляет фон на изображении. """
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        await remob.edit("`Обработка..`")
        try:
            if isinstance(
                    reply_message.media, MessageMediaPhoto
            ) or "image" in reply_message.media.document.mime_type.split('/'):
                downloaded_file_name = await remob.client.download_media(
                    reply_message, TEMP_DOWNLOAD_DIRECTORY)
                await remob.edit("`Удаляем фон..`")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await remob.edit("`Как мне удалить фон из этого?`"
                                 )
        except Exception as e:
            await remob.edit(str(e))
            return
    elif input_str:
        await remob.edit(
            f"`Удаление фона из онлайн-изображения, размещенного на`\n{input_str}")
        output_file_name = await ReTrieveURL(input_str)
    else:
        await remob.edit("`Мне нужно что-то, чтобы удалить фон из.`")
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(
                remob.chat_id,
                remove_bg_image,
                caption="Фон удален",
                force_document=True,
                reply_to=message_id)
            await remob.delete()
    else:
        await remob.edit("**Ошибка (Неверный API ключ)**\n`{}`".format(
            output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": 'Dm8j3oiP2hkLwE3LTi37NWKy',
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      files=files,
                      allow_redirects=True,
                      stream=True)
    return r


async def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": 'Dm8j3oiP2hkLwE3LTi37NWKy',
    }
    data = {"image_url": input_url}
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      data=data,
                      allow_redirects=True,
                      stream=True)
    return r


CMD_HELP.update({
    "rbg":
    ".rbg <ссылока на изображение> или ответ на изображение (Внимание: не работает на стикерах.)\
\nИспользование: Удаляет фон изображений, используя API remove.bg."
})
