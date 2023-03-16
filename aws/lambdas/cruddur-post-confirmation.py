import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name = user['name']
    user_email        = user['email']
    user_cognito_id   = user['sub']
    user_handle       = user['preferred_username']
    try:


        sql = f"""
        INSERT INTO public.users (
            display_name,
            email, 
            handle, 
            cognito_user_id
            ) 
        VALUES(%s,%s,%s,%s)
        """ 
        print('-----SQL STATEMENT')
        print(sql)
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        params = [
            user_display_name,
            user_email,
            user_cognito_id,
            user_handle
        ]
        cur.execute(sql,*params) 
        conn.commit() 
        print('execute end')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event