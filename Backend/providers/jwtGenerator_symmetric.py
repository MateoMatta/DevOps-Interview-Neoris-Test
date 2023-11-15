import datetime
import sys
import jwt


def encode_auth_token(e_message, e_to, e_from, e_timeToLifeSec, my_secret):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            "message" : e_message,
            "to": e_to,
            "from": e_from,
            "timeToLifeSec" : int(e_timeToLifeSec)
            #For a more secured way, used this payload
            
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            # 'iat': datetime.datetime.utcnow(),
            # 'sub': user_nickname
            
            #For the interview process purpose, it will be used this unsafe way. In this way the interviewer can test the solution
            # "sub": user_nickname
        }
        text =""
        text += str(jwt.encode(
            payload,
            my_secret,
            algorithm = 'HS256'
        ))
        return text
    except Exception as e:
        return e

# user_nickname = str(sys.argv[1])
# my_secret     = str(sys.argv[2])


# print(encode_   auth_token(user_nickname, my_secret))

#export JWT=$(python jwtGenerator_symmetric.py)