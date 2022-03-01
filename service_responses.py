class Add_response:
    message = ""
    typecode = 0

    def __init__(self, success):
        # super().__init__ (success)# self.success = success
        self.success = success

    def set_message(self, message):
        self.message = message
    
    def set_typecode(self, typecode):
        self.typecode = typecode

class Schedule_response:
    message = ""
    typecode = 0

    def __init__(self, success, schedule):
        self.success = success
        self.schedule = schedule

    def set_message(self, message):
        self.message = message

    def set_typecode(self, typecode):
        self.typecode = typecode

class Next_response:
    message = ""
    typecode = 0

    def __init__(self, success, time):
        self.success = success
        self.time = time
    
    def set_message(self, message):
        self.message = message

    def set_typecode(self, typecode):
        self.typecode = typecode