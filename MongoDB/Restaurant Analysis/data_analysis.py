# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------

import json
import codecs
import sys
import pymongo

# ------------------------------------------
# FUNCTION 1: most_popular_cuisine
# ------------------------------------------
def most_popular_cuisine(my_collection):
    pipeline=[]

    # 1.1.1 variable to get the count of rows
    nums=my_collection.count()

    # 1.1.2. Project to get just the cuisine
    command0={"$project":{"_id" : 0,"cuisine":"$cuisine"}}
    pipeline.append(command0)

    # 1.1.3. Group them by cuisine
    command1 ={"$group":{
            "_id":"$cuisine","count":{"$sum":1}
                }}
    pipeline.append(command1)

    # 1.1.4. Project to get just the ratio in percentage
    command2 = {"$project": {
                             "ratio": {
                                 "$multiply": [{"$divide": ["$count", {"$literal":nums}]}, 100]}
    }}
    pipeline.append(command2)

    # 1.1.5. Sort them in decreasing order by ratio
    command3={"$sort": {"ratio": -1}}
    pipeline.append(command3)

    # 1.1.6. Limit the collection to one document, to get just the one with more ratio
    command4={"$limit": 1}
    pipeline.append(command4)

    res=list(my_collection.aggregate(pipeline))

    result = (res[0]["_id"], res[0]["ratio"])

    return result

# ------------------------------------------
# FUNCTION 2: ratio_per_borough_and_cuisine
# ------------------------------------------
def ratio_per_borough_and_cuisine(my_collection, cuisine):

    pipeline1=[]

    # 2.1.1. Project to get just the borough and cuisine
    command0={ "$project" : { "borough" : 1, "cuisine": 1 } }
    pipeline1.append(command0)

    # 2.1.2. Group them by borough with condition of cuisine
    command1={"$group":{"_id":"$borough","total":{"$sum":1},
                        "count":{"$sum":
                                     {"$cond":[
                                         {
                                             "$eq":["$cuisine",cuisine]
                                         },1,0
                                     ]}
                                 }
                       }}
    pipeline1.append(command1)

    # 2.1.3. Project to get just the borough and ratio of count and total in percentage
    command2 = {"$project": {"borough" : 1,
        "ratio": {
            "$multiply": [{"$divide": ["$count", "$total"]}, 100]}
    }}
    pipeline1.append(command2)

    # 2.1.4. Sort them in decreasing order by ratio
    command3 = {"$sort": {"ratio": 1}}
    pipeline1.append(command3)

    # 2.1.5. Limit the collection to one document, to get just the one with more ratio
    command4 = {"$limit": 1}
    pipeline1.append(command4)

    res1 = list(my_collection.aggregate(pipeline1))

    result = (res1[0]["_id"], res1[0]["ratio"])

    return result

 # ------------------------------------------
# FUNCTION 3: ratio_per_zipcode
# ------------------------------------------
def ratio_per_zipcode(my_collection, cuisine, borough):
    # First Pipeline
    pipeline1=[]

    # 3.1.1 filter to get borough
    command0={"$match":{"borough":borough}}
    pipeline1.append(command0)

    # 3.1.2 Unfold the address
    command1={"$unwind":"$address"}
    pipeline1.append(command1)

    # 3.1.3 Project to get just the zipcode
    command2={"$project":{"_id":0,"pincode":"$address.zipcode","cuisine":"$cuisine"}}
    pipeline1.append(command2)

    # 3.1.4 Group them by zipcode
    command3={"$group":{"_id":"$pincode","total":{"$sum":1}}}
    pipeline1.append(command3)

    # 3.1.5 Sort them in decreasing order by total
    command4={"$sort":{"total":-1}}
    pipeline1.append(command4)

    # 3.1.6  Limit the collection to five document, to get just the top five total
    command5={"$limit": 5}
    pipeline1.append(command5)

    res1 = list(my_collection.aggregate(pipeline1))

    # Second Pipeline
    pipeline2=[]

    # 3.2.1 Project to get just address,borough and cuisine
    command6={"$project":{"address":"$address","borough":"$borough","cuisine":"$cuisine"}}
    pipeline2.append(command6)

    # 3.2.2 filter the document by borough and cuisine
    command7={"$match":{"borough":borough,"cuisine":cuisine}}
    pipeline2.append(command7)

    # 3.2.3 Unfold the address
    command8={"$unwind":"$address"}
    pipeline2.append(command8)

    # 3.2.4 Project to get just the zipcode
    command9={"$project":{"_id":0,"pincode":"$address.zipcode"}}
    pipeline2.append(command9)

    # 3.2.5 Group them by zipcode
    command10={"$group":{"_id":"$pincode","count":{"$sum":1}}}
    pipeline2.append(command10)

    # 3.2.6 Sort them in ascending order by count
    command11={"$sort":{"count": 1}}
    pipeline2.append(command11)

    res2 = list(my_collection.aggregate(pipeline2))

    # 3.3 For loop to get the ratio of count and total
    res = {}
    for i in range(len(res1)):
        for j in range(len(res2)):
            if (res1[i]['_id'] == res2[j]['_id']):
                k = res1[i]['_id']
                t = (int(res2[j]['count']) * 100) / (int(res1[i]['total']))
                res[k] = t

    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}

    return (list(res.keys())[0], list(res.values())[0])

# ------------------------------------------
# FUNCTION 4: best_restaurants
# ------------------------------------------
def best_restaurants(my_collection, cuisine, borough, zipcode):

     pipeline1=[]

    # 4.1.1 Filter the document by cuisine ,borough and zipcode
     command0={"$match":{"cuisine":cuisine,"borough":borough,"address.zipcode":zipcode}}
     pipeline1.append(command0)

    # 4.1.2 Project to get just the name,grades and grade count
     command1={"$project":{"_id":0,"name":"$name","grades":"$grades","grades_count":{"$size":"$grades"}}}
     pipeline1.append(command1)

    # 4.1.3 Filter the  grade count greater than 3
     command3={"$match": {"grades_count": { "$gte": 4 }}}
     pipeline1.append(command3)

    # 4.1.4 Project to get just the name and review
     command4={"$project":{"_id":0,"name":"$name","reviews":{"$avg":"$grades.score"}}}
     pipeline1.append(command4)

    # 4.1.5 Sort them in decreasing order by reviews
     command5={"$sort":{"reviews": -1}}
     pipeline1.append(command5)

    # 4.1.6 Limit the collection to three document, to get just the top three total
     command6={"$limit":3}
     pipeline1.append(command6)

     res1=list(my_collection.aggregate(pipeline1))

     best=[]
     review=[]
     for i in range(len(res1)):
         best.append(res1[i]["name"])
         review.append(res1[i]["reviews"])

     return (best,review)

# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------/
def my_main(database_name, collection_name):
    # 1. We set up the connection to mongos.exe allowing us to access to the cluster
    mongo_client = pymongo.MongoClient()

    # 2. We access to the desired database
    db = mongo_client.get_database(database_name)

    # 3. We access to the desired collection
    collection = db.get_collection(collection_name)

    # 4. What is the kind of cuisine with more restaurants in the city?
    (cuisine, ratio_cuisine) = most_popular_cuisine(collection)
    print("1. The kind of cuisine with more restaurants in the city is", cuisine, "(with a", ratio_cuisine, "percentage of restaurants of the city)")

    # 5. Which is the borough with smaller ratio of restaurants of this kind of cuisine?
    (borough, ratio_borough) = ratio_per_borough_and_cuisine(collection, cuisine)
    print("2. The borough with smaller ratio of restaurants of this kind of cuisine is", borough, "(with a", ratio_borough, "percentage of restaurants of this kind)")

    # 6. Which of the 5 biggest zipcodes of the borough has a smaller ratio of restaurants of the cuisine we are looking for?
    (zipcode, ratio_zipcode) = ratio_per_zipcode(collection, cuisine, borough)
    print("3. The zipcode of the borough with smaller ratio of restaurants of this kind of cuisine is zipcode =", zipcode, "(with a", ratio_zipcode, "percentage of restaurants of this kind)")

    # 7. Which are the best 3 restaurants (of the kind of cuisine we are looking for) of our zipcode?
    (best, reviews) = best_restaurants(collection, cuisine, borough, zipcode)
    print("4. The best three restaurants (of this kind of couisine) at these zipcode are:", best[0], "(with average reviews score of", reviews[0], "),", best[1], "(with average reviews score of", reviews[1], "),", best[2], "(with average reviews score of", reviews[2], ")")

    # 8. Close the client
    mongo_client.close()

# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We get the input arguments
    my_database = "test"
    my_collection = "restaurants"

    # 2. We call to my_main
    my_main(my_database, my_collection)
