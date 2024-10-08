import psycopg2
from psycopg2 import sql

#params
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# a function to get the chat history from the database
def fetchHistory():
    try:
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query
        query = "SELECT * FROM chatHistory ORDER BY timestamp DESC"

        #execute query
        cursor.execute(query)

        #fetch all results
        chat_history = cursor.fetchall()

        #close cursor and connection
        cursor.close()
        conn.close()

        print("Chat history successfully fetched")
        return chat_history

    except Exception as e:
        print(f"Error fetching chat history: {e}")

# a function to post AI response to the database
def postHistory(user_login, title_message, ai_response):
    try:
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query to insert data
        query = """
            INSERT INTO chatHistory (login, title, content, timestamp)
            VALUES (%s, %s, %s, NOW())
        """
        #execute query
        cursor.execute(query, (user_login, title_message, ai_response))

        #commit transaction 
        conn.commit()

        #close cursor & connection
        cursor.close()
        conn.close()

        print("AI response successfully posted to chatHistory")

    except Exception as e:
        print(f"Error posting to chat history: {e}")

