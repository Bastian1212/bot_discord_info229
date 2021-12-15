
import os, time
import pika
import wikipedia





########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="wiki", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="wiki")


##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	busqueda = body.decode('utf-8')
	print(busqueda)
	### REaliza la busqueda en  wikipedia 
	##busqueda = busqueda[16:len(busqueda)-1]
	##busquedaW = wikipedia.page(busqueda)
	busquedaW = wikipedia.summary(busqueda,sentences=1)
	##print(busquedaW)
	#busquedaW2 = "prueba"
	channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=busquedaW)
	
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()



#######################