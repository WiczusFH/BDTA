import re

pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


def validate(telegram_message):
    if telegram_message.text is None or telegram_message.date is None:
        return False
    if len(telegram_message.text)<2:
        return False
    if bool(pattern.match(telegram_message.text)):
        return False
    return True
