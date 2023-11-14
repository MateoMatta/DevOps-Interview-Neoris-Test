### Second way to initialize and configure MongoDB administrator access ###
    # Prerequisites
    # Required Access
    # You must have the createUser action on a database to create a new user on that database.

    # You must have the grantRole action on a role’s database to grant the role to another user.

    # If you have the userAdmin or userAdminAnyDatabase role, you have those actions.
#--------------------------
#Or better watch  the configuration here: https://phoenixnap.com/kb/kubernetes-mongodb
#--------------------------

#Script executed inside the primary MongoDB instance
# MainRepSet:PRIMARY>
        # Create the system user administrator.
    # db.getSiblingDB("admin").createUser({
    #     user : "other",
    #     pwd  : "admin",
    #     roles: [ { role: "root", db: "admin" } ]
    # });

#Call this MongoDB script executed with Linux bash...
# sh mongodb-administrator.sh $MONGO_INITDB_ROOT_USERNAME $MONGO_INITDB_ROOT_PASSWORD
#$1 = $MONGO_INITDB_ROOT_USERNAME
#$2 = $MONGO_INITDB_ROOT_PASSWORD

DB_USER=$1
DB_PASSWORD=$2

# EVAL='db.getSiblingDB("admin").createUser({
#     user : "'$DB_USER'",
#     pwd  : "'$DB_PASSWORD'",
#     roles: [ { role: "root", db: "admin" } ]
# });'
# # echo $EVAL


# mongosh --quiet --eval 'use admin' --eval "$EVAL" mongodb://$1:$2@localhost/


    #Or
#Script executed inside the primary MongoDB instance
# use admin
# db.createUser(
#   {
#     user: "<NEW_USER>",
#     pwd: "<NEW_PASSW>",
#     roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
#   }
# )

#----------------------

    # messagesCreate a user administrator for a single database.

#Script executed inside the primary MongoDB instance
# use messages
# db.createUser(
# {
#     user: "admin",
#     pwd: "admin",
#     roles: [ { role: "userAdmin", db: "messages" } ]
# }
# )
EVAL='db.createUser(
{
    user: "'$DB_USER'",
    pwd: "'$DB_PASSWORD'",
    roles: [ { role: "userAdmin", db: "messages" } ]
})'

mongosh --quiet --eval 'use messages' --eval "$EVAL" mongodb://$DB_USER:$DB_PASSWORD@localhost/

# Successfully added user: {
# 	"user" : "<MONGO_USER>",
# 	"roles" : [
# 		{
# 			"role" : "root",
# 			"db" : "admin"
# 		}
# 	]
# }

#Commands to test database to check its proper use...
# mongosh --eval 'MONGO_DB_COMMAND' mongodb://<MONGO_USER>:<MONGO_PASSW>@localhost/
# mongosh --eval 'db.user.update({"name":"foo"},{$set:{"this":"that"}});'

# mongosh --quiet --eval 'use thisDB' --eval 'db.user.insert({name: "Ada Wong", age: 25})' --eval 'show dbs' mongodb://<MONGO_USER>:<MONGO_PASSW>@localhost/
# mongosh --quiet --eval 'use thisDB' --eval 'db.user.insert({name: "Ada Wong", age: 25})' --eval 'db.user.findOne()' mongodb://<MONGO_USER>:<MONGO_PASSW>@localhost/
