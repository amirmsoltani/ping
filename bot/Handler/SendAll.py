def send_all(bot, update, users=[]):
    sender = bot.sendMessage
    keys = {}
    if update.message.text:
        sender = bot.sendMessage
        keys['text'] = update.message.text
    elif update.message.photo:
        sender = bot.sendPhoto
        keys['photo'] = update.message.photo[0].file_id
        keys['caption'] = update.message.caption or ""
    elif update.message.voice:
        sender = bot.sendVoice
        keys['voice'] = update.message.voice.file_id
        keys['caption'] = update.message.caption or ""
    elif update.message.video:
        sender = bot.sendVideo
        keys['video'] = update.message.video.file_id
        keys['caption'] = update.message.caption or ""
    elif update.message.document:
        sender = bot.sendDocument
        keys['document'] = update.message.document.file_id
        keys['caption'] = update.message.caption or ""
    elif update.message.audio:
        sender = bot.sendAudio
        keys['audio'] = update.message.audio.file_id
        keys['caption'] = update.message.caption or ""
    for user in users:
        sender(user, parse_mode="HTML", **keys)
