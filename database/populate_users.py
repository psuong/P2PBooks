import os
from database_objects import serialize_user, User

USER_LIST = ["Chris",
             "MD",
             "Porrith",
             "Fioger"]

EMAIL_LIST = ["chris@gmail.com",
              "md@gmail.com",
              "porrith@gmail.com",
              "fioger@gmail.com"]

DOB_LIST = ["01/26/1995"
            "01/01/1993"
            "07/17/1995"
            "12/26/1995"]

for i in range(4):
    serialize_user(User(username=USER_LIST[i],
                        password="pw",
                        email=EMAIL_LIST[i],
                        dob=DOB_LIST[i],
                        ), USER_LIST[i])

