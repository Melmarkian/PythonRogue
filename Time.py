class Time:

    tick = 0

    seconds = 0
    minutes = 0
    hours = 0
    days = 0
    months = 0
    years = 0
    daytime = ""



    def __init__(self):

        self.seconds = 1277770
        self.standardize()
        self.check_daytime()

    def increment(self, tick = 10):

        self.seconds += tick
        self.tick += 1
        if self.seconds >= 60:
            self.standardize()

    def standardize(self):
        if self.seconds >= 60:
            self.minutes += self.seconds / 60
            self.seconds %= 60

        if self.minutes >= 60:
            self.hours += self.minutes / 60
            self.minutes %= 60
            self.check_every_hour()


        if self.hours >= 24:
            self.days += self.hours / 24
            self.hours %= 24


    def check_every_hour(self):

        self.check_daytime()


    def check_daytime(self):

        if self.hours >= 5 and self.hours < 8:
            self.daytime = "Early Morning"
        elif self.hours >= 8 and self.hours < 12:
            self.daytime = "Morning"
        elif self.hours >= 12 and self.hours < 4:
            self.daytime = "Noon"
        elif self.hours >= 4 and self.hours < 7:
            self.daytime = "Afternoon"
        elif self.hours >= 7 and self.hours < 11:
            self.daytime = "Evening"
        elif self.hours >= 11 and self.hours < 2:
            self.daytime = "Night"
        elif self.hours >= 2 and self.hours < 5:
            self.daytime = "After Midnight"


    def get_timestamp(self):
        timestamp = self.daytime + " " + str(self.days) + ":" + str(self.months) + ":" + str(self.years)
        return timestamp