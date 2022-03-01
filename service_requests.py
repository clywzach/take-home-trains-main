class Add_request():

    def __init__(self, id, schedule):
        self.schedule = []
        # checking id validity
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if id.isalnum() and len(id) <= 4:
            self.id = id
        else:
            raise Exception

        # checking schedule validity
        if not isinstance(schedule, list):
            raise TypeError("schedule must be a list")
        if schedule is not None and len(schedule) > 0:
            for time in schedule:
                curTime = -1
                if isinstance(time, str):
                    try:
                        curTime = int(time)
                    except:
                        raise Exception
                    else:
                        if curTime >= 0 and curTime <= 2400:
                            self.schedule.append(curTime)
                        else:
                            raise Exception
                elif isinstance(time, int) and time >= 0 and time <= 2400:
                    self.schedule.append(time)
                else:
                    raise Exception
        else:
            raise Exception

class Schedule_request():

    def __init__(self, id):
        # checking id validity
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if id.isalnum() and len(id) <= 4:
            self.id = id
        else:
            raise Exception

class Next_request():

    def __init__(self, time):
        # checking time validity
        if time is not None:
            curTime = -1
            try: 
                curTime = int(time)
            except:
                raise Exception
            else:
                if curTime >= 0 and curTime <= 2400:
                    self.time = curTime
                else:
                    raise Exception
            
        else:
            raise Exception

