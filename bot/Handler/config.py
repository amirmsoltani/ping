from bot.models import Chat


def CHATS():
    chat = Chat.objects.get(status=3)
    return chat.username


def fallow():
    chat = Chat.objects.get(status=1)
    return chat.username


def rel():
    chat = Chat.objects.get(status=2)
    return Chat.username


Bot = "soltanikbot"
