import datetime
import re

yesterday_date = datetime.date.today() - datetime.timedelta(days=1)

class timestamp_re:
    yesterday = r"%d%02d%02d" % (yesterday_date.year, yesterday_date.month, yesterday_date.day)
    date = r"(19|20)\d\d[01]\d[0123]\d"
    time = r"(0[0-9]|1[0-9]|2[0-3])[0-5][0-9]"
    date_time = date + r"_" + time

    def fullmatch_yesterday(str):
        return re.fullmatch(timestamp_re.yesterday, str)

    def search_date(str):
        return re.search(timestamp_re.date, str)

    def search_date_time(str):
        return re.search(timestamp_re.date_time, str)


