def slug(text):
    '''In reality you may need to implement a better version of it'''
    text = text.lower()
    text = text.replace(" ", "-")
    return text