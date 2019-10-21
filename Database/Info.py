class Info:
    def __init__(self):
        self.end = 1

    def get_end_of_the_file(self):
        return self.end

    def inc_end_of_the_file(self):
        self.end = self.end + 1
