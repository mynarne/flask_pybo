import locale

locale.setlocale(locale.LC_ALL, '')

# 시간, 날짜 포매팅 함수
def format_datetime(value, fmt="%Y년 %m월 %d일 %p %I:%M"):
    return value.strftime(fmt)