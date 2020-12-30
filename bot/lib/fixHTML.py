def fixHTML(text):
    """replaces html-markup parts on tags"""
    return str(text).replace("&", "&amp;") \
                    .replace("<", "&lt;") \
                    .replace(">", "&gt;")
