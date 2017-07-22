def clean_content(text):
    symbols = ['`', '"', '\'']
    out = text
    for symbol in symbols:
        out = out.replace(symbol, '')
    return out
