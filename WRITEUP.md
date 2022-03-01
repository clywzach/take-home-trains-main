
### TESTING

1. in venv
2. use ``` flask run```
3. before testing, initalize the database by running ``` python init_db.py``` from /database
4. use ``` pytest ```


### NOTES

- When first reading the README, I didn't realize that key-value store referred to a specific type of database. So I didn't think too much of it and implemented a SQLite database. Jake informed me that it shouldn't be a huge issue and to just note down it's implications, trade offs, etc. (see section below)

- The README says "Initially the service will support a single train station..." so I decided to add a table for stations. For this project, trains added to the database simply have a foreign key of '1' referring to the only station present in this table.


### SQLite database vs nonrelational key-value store

- Because SQLite has a specified structure, it can be better for complex queries and building relationships between different tables and keys. This could be useful if the database were to grow and it became necessary to keep track of a very complex train system.

- A nonrelational key-value store could, however, be quicker for read and write operations. It also would have made this project a bit simpler. For example:
    - Because I made a table for station, and required a trainline to store the station it belongs to in the database, it became necessary to add another method to db.py
    - I also had to rework the test_db.py a bit to work with the SQLite database.


### REGARDING THREADING

- From what I read online regarding Flask, it appears to run in threaded mode by default.

- As far as I know, SQLite by default allows for only one writer at a time (locking the database in a sense), however, it can have multiple readers. So if there are multiple threads, one is trying to write, and one is trying to read, then there is a race condition. 

- To tackle this issue, I researched it a bit online and believe that setting the isolation level of the database connection to EXCLUSIVE makes it so it'll only allow one reader or one writer at a time. One other idea I had for handling this was importing lock and using a lock/release system for when operations are performed on the database.


### TIME COMPLEXITY OF NEXT

- O(n*m) where n is the number of train lines in the database and m is the number of times in its schedule

- It has a double nested loop where the outside loop is the trainlines and the inside is the times in the schedule

- It builds a map where the keys are the times and the value is a list of the trainlines that arrive at that time

- Ideally I'd like to rework the algorithm to make it more efficient but it wasn't immediately obvious to me what could be changed. I thought about how I could potentially stop looping as soon as I found the next earliest time that existed in multiple schedules, however, worst case you can still get O(n*m). Perhaps average case would be better.

- A very easy way to improve efficiency of next would be to simply have a db method that returns the times greater than the target time that appear more than once in the column of the table. This way you don't have to create a new structure. However, I was under the assumption that the functionality of `/trains`, `/trains/<train_id>`, and `/trains/next` needed to be handled with just *db.set(key, value)*, *db.get(key)*, and *db.keys()* so I didn't create a new db method to do so. The only db method I created was to associate a trainline to a station which is an extra feature I added myself.


### MY ASSUMPTIONS

`/trains`
   - id must be a string (so 1234 must come in as "1234")
   - requests made with ids that exist in the database, regardless of if the request has new times in its schedule, will not be accepted. for this I return a 400 error
   - the schedule must not be empty, must be a list, and must contain numbers
   - times in schedule must be between 0 and 2400
   - requests that fail to abide by these constraints are rejected

`/trains/<train_id>`
   - trying to get a schedule for a nonexistent line returns a 400 error

`/trains/next`
   - in the assumptions of README, it talked about a "specified time" to which `/trains/next` should return the time after such where two or more trains are in the station. as this is a GET request with no url arguments, I assumed this "specified time" comes from a header.
   - if a request is made when there are no trains in the database, it simply returns no time but is considered a valid request. there can be no time two or more trains are in the station when there are no trainlines.

`etc`
   - other assumptions made about validity regarding inputs and requests can be seen in code of service_requests.py
