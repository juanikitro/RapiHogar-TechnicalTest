from django.core.management.base import BaseCommand, CommandError
from rapihogar.models import Pedido, Scheme, Company, User, Technician
import random

class Command(BaseCommand):
    help = 'Create N random pedidos'

    def add_arguments(self, parser):
        parser.add_argument('N', type=int, help='Number of pedidos to create')

    def handle(self, *args, **options):
        n = options['N']

        if n < 1 or n > 100:
            print('N debe estar entre 1 y 100')
            return None

        technicians = list(Technician.objects.all())
        if not technicians:
            print('No hay técnicos registrados en la base de datos')
            return None

        clients = list(User.objects.all())
        if not clients:
            print('No hay clientes registrados en la base de datos')
            return None

        for i in range(n):
            pedido = Pedido()
            pedido.technician = random.choice(technicians)
            pedido.client = random.choice(clients)
            pedido.hours_worked = random.randint(1, 10)
            pedido.save()

            print(f'Pedido {i+1} de {n} creado con id: {pedido.id}')

        print(f'Se han creado {n} pedidos aleatorios')
