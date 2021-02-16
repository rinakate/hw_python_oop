import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(
            record.amount
            for record in self.records
            if record.date == dt.date.today()
        )

    def get_week_stats(self):
        today = dt.date.today()
        last_week = today - dt.timedelta(days=7)
        return sum(
            record.amount
            for record in self.records
            if last_week < record.date <= today
        )

    def get_today_remainder(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    RUB_RATE = 1.00
    EURO_RATE = 89.61
    USD_RATE = 73.94

    def get_today_cash_remained(self, currency):
        currency_values = {
            'usd': tuple([self.USD_RATE, 'USD']),
            'eur': tuple([self.EURO_RATE, 'Euro']),
            'rub': tuple([self.RUB_RATE, 'руб'])
        }

        val_course, val_name = currency_values[currency]

        remaning_money = self.get_today_remainder()
        conv_remaning_money = self.get_today_remainder() / val_course
        if remaning_money > 0:
            return (f'На сегодня осталось {conv_remaning_money:.2f} '
                    f'{val_name}')
        elif remaning_money == 0:
            return 'Денег нет, держись'
        conv_module = abs(conv_remaning_money)
        return (f'Денег нет, держись: твой долг - {conv_module:.2f} '
                f'{val_name}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remaning_calories = self.get_today_remainder()
        if remaning_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remaning_calories} кКал')
        return 'Хватит есть!'


if __name__ == "__main__":

    cach_calculator = CashCalculator(6000)
    r1 = Record(amount=145, comment="Безудержный шопинг", date="15.02.2021")
    r2 = Record(amount=5600, comment="Наполнение потребительской корзины")
    r3 = Record(amount=691, comment="Катание на такси", date="16.02.2021")

    cach_calculator.add_record(r1)
    cach_calculator.add_record(r2)
    cach_calculator.add_record(r3)

    print(cach_calculator.get_week_stats())
    print(cach_calculator.get_today_cash_remained('rub'))

    calories_calculator = CaloriesCalculator(1700)
    r4 = Record(amount=1200, comment="Кусок тортика. И ещё один.")
    r5 = Record(amount=84, comment="Йогурт")
    r6 = Record(amount=1140, comment="Баночка чипсов.", date="16.02.2021")

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_calories_remained())
