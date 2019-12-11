class Car(object):
    def __init__(self, make, model, year, color):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def get_color(self):
        return self.color

    def get_model(self):
        return self.model

    def get_year(self):
        return self.year

    def get_make(self):
        return self.make