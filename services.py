import sys, collections
import sqlite3
from flask import Flask, Response, jsonify, request

from database.db import Database
from database.connection import Connection
from service_requests import *
from service_responses import *

db = Database()

class Services:

    def add_train(self, add_request):
        add_response = None
        try:
            my_connection = Connection.get_db_connection()
            # add the new trainline
            db.set_trainline(add_request.id, 1, my_connection)
        except sqlite3.IntegrityError as e:
            # if the train already exists in database
            my_connection.close()
            add_response = Add_response(False)
            return self.bad_service_response(add_response, "Trains already been added.")
        except Exception as e:
            # if database error
            my_connection.close()
            add_response = Add_response(False)
            return self.error_service_response(add_response, "Internal server error.")
        else:
            # otherwise add its times to schedule
            add_response = self.add_trainschedule(add_request, my_connection)
            my_connection.close()
        
        return add_response


    # helper function for add_train to add schedules
    def add_trainschedule(self, add_request, my_connection): 
        add_response = None
        for time in add_request.schedule:
            try:
                # add each time for schedule
                db.set(add_request.id, time, my_connection)
            except Exception as e:
                # if database error
                add_response = Add_response(False)
                return self.error_service_response(add_response, "Internal server error.")
            else:
                # successfully added time for trainline
                add_response = Add_response(True)
                add_response = self.good_service_response(add_response, "Success adding the train line.")
        
        return add_response
    
    def get_schedule(self, schedule_request):
        schedule_response = None
        try:
            my_connection = Connection.get_db_connection()
            # get schedule for trainline
            schedules = db.get(schedule_request.id, my_connection)
            my_connection.close()
        except Exception as e:
            # if database error
            schedule_response = Schedule_response(False, None)
            return self.error_service_response(schedule_response, "Internal server error.")
        else:
            if len(schedules) == 0:
                # train line has no schedule and does not exist
                schedule_response = Schedule_response(False, None)
                return self.bad_service_response(schedule_response, "This train line does not exist.")
            else:
                # success let's return the schedule
                schedule = []
                for time in schedules:
                    schedule.append(time)
                schedule_response = Schedule_response(True, schedule)
                schedule_response = self.good_service_response(schedule_response, "Check response data for schedule.")

        return schedule_response

    def get_next(self, next_request):
        next_response = None
        try:
            target_time = next_request.time
            my_connection = Connection.get_db_connection()
            # get the schedules for trainlines
            keys = db.keys(my_connection)
            my_connection.close()
        except Exception as e:
            # if database error
            next_response = Next_response(False, None)
            return self.error_service_response(next_response, "Internal server error.") 
        else:
            # create dict from times to stations
            time_to_line = self.get_time_to_line(keys)
            if time_to_line is not None:
                # find next time
                for key in filter(lambda y: y >= target_time, time_to_line.keys()):
                    if len(time_to_line[key]) > 1:
                        next_response = Next_response(True, key)
                        return self.good_service_response(next_response, "Next time two or more trains will be in station: " + str(key))

                for key in filter(lambda y: y < target_time, time_to_line.keys()):
                    # wrap around to before specified time
                    if len(time_to_line[key]) > 1:
                        next_response = Next_response(True, key)
                        return self.good_service_response(next_response, "Next time two or more trains will be in station: " + str(key))
            else:
                # database error when getting schedule for a line
                next_response = Next_response(False, None)
                return self.error_service_response(next_response, "Internal server error.") 

        # did not find a time
        next_response = Next_response(True, "No time")
        return self.good_service_response(next_response, "Next time two or more trains will be in station: " + str(key))


    # helper function for get_next to build dict from times to stations
    def get_time_to_line(self, keys):
        time_to_line = {}
        for id in keys:
            schedule_request = Schedule_request(id)
            schedule_response = self.get_schedule(schedule_request)
            if schedule_response.success:
                # for each time corresponding to the trainline add it to
                # the map as a key and add that trainline to corresponding list
                for time in schedule_response.schedule:
                    if time in time_to_line.keys():
                        time_to_line[time].append(id)
                    else:
                        lines = []
                        lines.append(id)
                        time_to_line[time] = lines
            else:
                # database error when getting schedule for a line
                return None
        
        time_to_line = collections.OrderedDict(sorted(time_to_line.items()))
        return time_to_line



    # Helper functions to build service_response objects when necessary
    def bad_service_response(self, response_obj, message):
        response_obj.set_message(message)
        response_obj.set_typecode(400)
        return response_obj

    def error_service_response(self, response_obj, message):
        response_obj.set_message(message)
        response_obj.set_typecode(500)
        return response_obj

    def good_service_response(self, response_obj, message):
        response_obj.set_message(message)
        response_obj.set_typecode(200)
        return response_obj
            

        