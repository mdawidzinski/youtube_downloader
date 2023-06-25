

def check_url_invalidity(url: str):
    # Check given url for any content and length of the content
    if url is None:
        return 'Invalid link', 'Cannot continue with empty link.\nPlease, provide a valid link.'
    # https://www.youtube.com/watch?v= has 33 characters
    if len(url) < 33:
        return 'Invalid link', 'Cannot continue with too short link.\nPlease, check, if it was copied in full.'
    beginning = 'https://www.youtube.com/watch'
    if not url.startswith(beginning):
        return 'Invalid link', f'Link must start with {beginning}.\nPlease, check, if the right link was copied.'
    return None, None
