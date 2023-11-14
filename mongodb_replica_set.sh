#!/bin/bash #REPLACE
### Initialize MongoDB replicaset, acknowledging the mongo instances to be used as a HA cluster NoSQL database ### #REPLACE
 #REPLACE
#Call this script with...  #REPLACE
# apt update -y; apt install nano -y; nano mongodb_replica_set.sh #REPLACE
# bash mongodb_replica_set.sh $MONGO_INITDB_ROOT_USERNAME $MONGO_INITDB_ROOT_PASSWORD #REPLACE
 #REPLACE
## IMPORTANT ## Use "bash" instead of "sh" to execute the script  #REPLACE
 #REPLACE
#$1 = $MONGO_INITDB_ROOT_USERNAME #REPLACE
#$2 = $MONGO_INITDB_ROOT_PASSWORD #REPLACE
 #REPLACE
#Perform initialization, if this actual machine is the primary MongoDB instance ([direct: primary]) #REPLACE
# mongosh  --quiet --eval 'db.runCommand("ismaster")' mongodb://localhost/ > test.txt #REPLACE
# export isMasterAnswer="$(grep --line-buffered "ismaster: true," test.txt)" #REPLACE
# echo $isMasterAnswer #REPLACE
if [[ "$(hostname)" != "mongod-0" ]]; then #REPLACE
sleep 5 #REPLACE
mongod --bind_ip_all --replSet MainRepSet #REPLACE
echo "Okay" #REPLACE
fi #REPLACE
 #REPLACE
echo "Waiting for MongoDB nodes to be recognized..." #REPLACE
sleep 15 #REPLACE
# Cycles/loops
if [[ "$(hostname)" == "mongod-0" ]]; then #REPLACE
# export DB_USER=$MONGO_INITDB_ROOT_USERNAME #REPLACE
# export DB_PASSWORD=$MONGO_INITDB_ROOT_PASSWORD #REPLACE
DB_USER=$1 #REPLACE
DB_PASSWORD=$2 #REPLACE
 #REPLACE
mongod --bind_ip_all --replSet MainRepSet --fork --logpath /var/log/mongodb/mongod.log #REPLACE
echo I am $(hostname), the primary MongoDB instance. I will perform this... #REPLACE
sleep 10 #REPLACE
    ### 1) Initialize the whole database. #REPLACE
mongosh  --quiet --eval 'rs.initiate({ _id: "MainRepSet", version: 1, #REPLACE
members: [ #REPLACE
{ _id: 0, host: "mongod-0.mongodb-service.default.svc.cluster.local:27017" }, #REPLACE
{ _id: 1, host: "mongod-1.mongodb-service.default.svc.cluster.local:27017" }, #REPLACE
{ _id: 2, host: "mongod-2.mongodb-service.default.svc.cluster.local:27017" } ]});' mongodb://localhost/; echo Initialized! #REPLACE
echo "Waiting for MongoDB database to be initialized..." #REPLACE
sleep 25 #REPLACE
 #REPLACE
#MainRepSet [direct: primary] test> #REPLACE
    ### 2) Create administrator for the whole database. #REPLACE
export EVAL='db.createUser({ #REPLACE
    user : "'$DB_USER'", #REPLACE
    pwd  : "'$DB_PASSWORD'", #REPLACE
    roles: [ { role: "root", db: "admin" } ] #REPLACE
});' #REPLACE
mongosh --quiet --eval 'use admin' --eval "$EVAL" mongodb://localhost/ #REPLACE
 #REPLACE
    # 3.1) Create a user administrator for a admin database. #REPLACE
export EVAL='db.createUser( #REPLACE
{ #REPLACE
    user: "'$DB_USER'", #REPLACE
    pwd: "'$DB_PASSWORD'", #REPLACE
    roles: [ { role: "userAdmin", db: "admin" } ] #REPLACE
})' #REPLACE
mongosh --quiet --eval 'use admin' --eval "$EVAL" mongodb://$DB_USER:$DB_PASSWORD@localhost/ #REPLACE
 #REPLACE
    # 3.2) Create a user administrator for a config database. #REPLACE
# mongosh --quiet --eval 'use local' --eval "$EVAL" mongodb://localhost/ #REPLACE
export EVAL='db.createUser( #REPLACE
{ #REPLACE
    user: "'$DB_USER'", #REPLACE
    pwd: "'$DB_PASSWORD'", #REPLACE
    roles: [ { role: "userAdmin", db: "config" } ] #REPLACE
})' #REPLACE
mongosh --quiet --eval 'use config' --eval "$EVAL" mongodb://$DB_USER:$DB_PASSWORD@localhost/ #REPLACE
 #REPLACE
    # 3.3) Create a user administrator for a messages database. #REPLACE
# mongosh --quiet --eval 'use messages' --eval "$EVAL" mongodb://localhost/ #REPLACE
export EVAL='db.createUser( #REPLACE
{ #REPLACE
    user: "'$DB_USER'", #REPLACE
    pwd: "'$DB_PASSWORD'", #REPLACE
    roles: [ { role: "userAdmin", db: "messages" } ] #REPLACE
})' #REPLACE
mongosh --quiet --eval 'use messages' --eval "$EVAL" mongodb://$DB_USER:$DB_PASSWORD@localhost/ #REPLACE
 #REPLACE
mongosh  --quiet --eval 'rs.status();' mongodb://$DB_USER:$DB_PASSWORD@localhost/ #REPLACE
# mongosh  --quiet --eval 'db.runCommand("ismaster")' mongodb://localhost/ #REPLACE
mongod --bind_ip_all --replSet MainRepSet #REPLACE
fi
