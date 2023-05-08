"""
    Simple file with just a few shortenings functions
"""

def fraction(full_size, fraction):
    one_frac = full_size / 100
    fraction *= one_frac
    return int(fraction)


def pb(data, text=None):
    data.progressbar_loc['value'] += 10
    data.progressbar_loc.update()
    if text:
        data.progressbar_text.config(text=text)
