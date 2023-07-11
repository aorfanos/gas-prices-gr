import time
import datetime
import re

from unidecode import unidecode


def transliterate_gr2en(text):
    """Transliterate greek time period (AM/PM) to english."""
    time_text = ''

    # convert greek chars to unicode and translate to english
    if unidecode(text[-2:]) == 'pm':
        time_text = 'AM'
    elif unidecode(text[-2:]) == 'mm':
        time_text = 'PM'

    rm_greek_chars = text[:len(text) - 2]  # remove last 2 characters

    return f'{rm_greek_chars}{time_text}'


def greek_date_to_ts(date):
    """Convert Greek date to timestamp."""
    date_encoded = transliterate_gr2en(date)
    return time.mktime(
        datetime.datetime.strptime(
            date_encoded,
            '%d/%m/%Y %I:%M:%S %p',
        ).timetuple(),
    )


def extract_date(datestring):
    """Extracts the date from the gas station last update."""
    dtstr_fmt = datestring.replace('  ', '')
    pattern = r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2} ..'
    match = re.search(pattern, dtstr_fmt)
    if match:
        return match.group()
    else:
        return ''
