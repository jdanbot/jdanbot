def fixHTML(text):
    """replaces html-markup parts on tags"""
    return text.replace("&", "&amp;") \
               .replace("<", "&lt;") \
               .replace(">", "&gt;")
