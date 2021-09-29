def hashtag_splitter(tag_string):
    return [t.strip() for t in tag_string.split('#') if t.strip()]


def hashtag_joiner(tags):
    return '#' + ' #'.join(t.name for t in tags).lstrip()