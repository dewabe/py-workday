import datetime


class Workdays:
    """
    Generates working days between two dates
    Supported countries:
     * Finland

    Excludes
    * All weekends (Saturday, Sunday)
    * Specific public holidays, such an Christmas, Easter...

    Initializing:
    workdays = Workdays(dt_from, dt_to)
    where dt_from and dt_to are both datetime objects

    Attributes
        workdays: list of datetime objects

    TODO:
        Lots of Optimizing
    """
    def __init__(self, dt_from, dt_to):
        self.workdays = self._workdays(dt_from, dt_to)

    def _workdays(self, d, end, excluded=(6, 7)):
        days = []
        while d.date() <= end.date():
            if d.isoweekday() not in excluded and not self._public_holidays(d):
                days.append(d)
            d += datetime.timedelta(days=1)
        return days

    def _public_holidays(self, d):
        def calc_easter(year):
            """
            Pääsiäinen ja helatorstai
            https://code.activestate.com/recipes/576517-calculate-easter-western-given-a-year/
            """
            a = year % 19
            b = year // 100
            c = year % 100
            d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
            e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
            f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
            month = f // 31
            day = f % 31 + 1
            return datetime.datetime(year, month, day)

        def calc_midsummer(year):
            dt = datetime.datetime(year, 6, 19)
            while dt.weekday() != 4:
                dt += datetime.timedelta(days=1)
            return dt

        dt = datetime.datetime
        easter = calc_easter(d.year)
        midsummer = calc_midsummer(d.year)
        christmas = dt(d.year, 12, 24)
        excluded = [
            # Uuden vuoden päivä (1.1.)
            dt(d.year, 1, 1),
            # Loppiainen (6.1.)
            dt(d.year, 1, 6),
            # Pääsiäinen (oma laskenta)
            easter + datetime.timedelta(days=-2),
            easter + datetime.timedelta(days=1),
            # Vappu (5.1.)
            dt(d.year, 5, 1),
            # Helatorstai (40 päivää pääsisäisestä)
            easter + datetime.timedelta(days=39),
            # Juhannusaatto (20.-26.6. välinen perjantai)
            midsummer,
            # Itsenäisyyspäivä (6.12.)
            dt(d.year, 12, 6),
            # Joulun pyhät (24.-26.12.)
            christmas,
            christmas + datetime.timedelta(days=1),
            christmas + datetime.timedelta(days=2)
        ]

        return d in excluded