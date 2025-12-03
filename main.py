import pathlib
import pika
import os
import time

TARGET_PATH = os.getenv('SCAN_PATH', '/data')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

def get_connection():
    retries = 30
    while retries > 0:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready yet... waiting ({retries} retries left)")
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to RabbitMQ after multiple retries")

def main():
    print(f"Connecting to RabbitMQ at {RABBITMQ_HOST}...")
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='Files')

    def on_error(e):
        print(f"Skipped file/folder on error: {e}")

    print(f"Starting search in: {TARGET_PATH}")
    
    # Checking if the target path exists
    if not os.path.exists(TARGET_PATH):
        print(f"Error: The path '{TARGET_PATH}' does not exist inside the container.")
        connection.close()
        return

    count = 0
    for dir_path, _, file_names in os.walk(TARGET_PATH, onerror=on_error):
        for file_name in file_names:
            file_path = pathlib.Path(dir_path) / file_name
            
        
            channel.basic_publish(exchange='', routing_key='Files', body=f"Found file {file_path}")
            print(f"Sent: {file_name}")
            count += 1
            
    print(f"Finished. Sent {count} files.")
    connection.close()

if __name__ == '__main__':
    main()