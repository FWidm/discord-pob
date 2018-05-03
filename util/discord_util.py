def parse_nick_or_name(author):
    displayed_name = None
    try:
        displayed_name = author.nick
    except AttributeError:
        pass
    if not displayed_name:
        displayed_name = author.name
    return displayed_name
