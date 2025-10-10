from django import template

register = template.Library()

BAD_WORDS = [
     'падла', 'тварь', 'урод', 'дебил'
]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value
    words = value.split()
    censored_words = []
    for word in words:
        original_word = word
        word_lower = word.lower()
        is_bad = False
        for bad_word in BAD_WORDS:
            if bad_word in word_lower:
                is_bad = True
                break
        if is_bad and len(original_word) > 1:
            censored_word = original_word[0] + '*' * (len(original_word) - 1)
            censored_words.append(censored_word)
        else:
            censored_words.append(original_word)
    return ' '.join(censored_words)
