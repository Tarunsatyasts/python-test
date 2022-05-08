from pymongo import MongoClient



client  = MongoClient("_connectionurl_")
# Get a new db client ... 

events = client.events_db.activeEvents
bookmakers = client.bookmakers.bookmakers
# Get collections from db ... 




mapped_events = [] # New list to store mapped events

for event in events.find({"isActive" : True}): # Iterating through every event ( which is an active event)
    for bookmaker in bookmakers({"isActive" : True}): # Iterating through every bookmaker 
        event.update(
            {
                "bookmakerId" : bookmaker["id"],
                "bookmakerName" : bookmaker['name']
            }
        ) # Updating bookmaker detials on mapped events 
        
    mapped_events.append(
        event
    ) # Appending to new list 


client.oddsandmore.mapping.insert_many(
    mapped_events
) # Inserting mapped data to database 


# Pros
# 1. Filtering documents  via inbuild Mongo filters 
# 2. using pymongo to connect mongodb 
# 3. We can save time and complexity by mapping single event data with multiple bookmakers using this process. 

# Cons
# 1. Using two loops
# 2. Code runs in n^2 runtime
# 3. Using linear iteration 
# 4. The disadvantage of this method is that we don't know who is accessing the event in advance.
