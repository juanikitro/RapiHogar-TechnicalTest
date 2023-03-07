# Solucion
Hola! Soy Juan Ignacio y esta es mi solucion. Sinceramente no creo que sea la mejor solucion que puedo encontrar ya que tuve que hacerla en un tiempo muy reducido por trabajo y compromisos personales.
Las vistas de los endpoints estan basadas en funciones ya que me parecio la forma mas rapida de programarlo.
La informacion del modelo "Technician" la invente ya que no venia aclarado y quise que sea lo mas "practico y realista" posible considerando la prueba.
Me hubiese gustado tener mas tiempo para entregar la prueba y poder agregar algunos test cases que me quedaron afuera, documentar mejor el codigo y pasar la DB a un Postgre como lo tienen en RapiHogar.

### Recomiendo correr los tests para ver si todo esta funcionando bien:
```bash
python manage.py test
```

## 1. Creacion del modelo y carga de datos

Modelo:
```python
class Technician(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, default='-') # Default for avoid future problems
    last_name = models.CharField(max_length=100, default='-') # Default for avoid future problems
    company = models.ForeignKey(
            Company,
            on_delete=models.SET_NULL,
            null=True,
            blank=True
        ) # on_delete = set null to avoid problems with delete companies and don't loose data

    @staticmethod
    def pay_by_hours(hours_worked):
        # Table of rates and discounts:
        rates = {14: 200, 29: 250, 48: 300, float('inf'): 350}
        discounts = {14: 0.15, 29: 0.16, 48: 0.17, float('inf'): 0.18}

        for threshold, rate in rates.items():
            if hours_worked < threshold:
                discount = discounts[threshold]
                break

        return int(hours_worked * rate * (1 - discount))

    class Meta:
        app_label = 'rapihogar'
        verbose_name = _('Técnico')
        verbose_name_plural = _('Técnicos')
        ordering = ('id', )
```

Cargar datos:
```bash
python manage.py loaddata rapihogar/fixtures/technician.json --app rapihogar.technician
```

## 2. Comando para generar N pedidos

### Con N entre 1 y 100
Ejecucion:
```bash
N=10 # ejemplo con variable de bash
python manage.py create_random_pedidos $N
    ```

Output:
```bash
Pedido 1 de 10 creado con id: 63
Pedido 2 de 10 creado con id: 64
Pedido 3 de 10 creado con id: 65
Pedido 4 de 10 creado con id: 66
Pedido 5 de 10 creado con id: 67
Pedido 6 de 10 creado con id: 68
Pedido 7 de 10 creado con id: 69
Pedido 8 de 10 creado con id: 70
Pedido 9 de 10 creado con id: 71
Pedido 10 de 10 creado con id: 72
Se han creado 10 pedidos aleatorios
```

### Con N < 1 && N > 100
Ejecucion:
```bash
N=200 # ejemplo con variable de bash
python manage.py create_random_pedidos $N
    ```

Output:
```bash
N debe estar entre 1 y 100
```

## 3. Servicio web para listar tecnicos y el pago correspondiente

### Consulta GET sin filtrar
Consulta en cURL:
```bash
curl --location 'http://localhost:8000/api/technicians/'
```
Output:
```bash
[
    {
        "id": 1,
        "full_name": "Juan Ignacio Portilla Kitroser",
        "orders_id": [
            257,
            248,
            219,
            206,
            179,
            172,
            167,
            164,
            137,
            117,
            116,
            110,
            107,
            103,
            99,
            97,
            94,
            92,
            90,
            55,
            44,
            35,
            34,
            33,
            27,
            17,
            12,
            10,
            9,
            6,
            2,
            1
        ],
        "hours_worked": 159,
        "pay_by_hours": 45633
    },
    {
        "id": 2,
        "full_name": "Lautaro Martinez",
        "orders_id": [
            277,
            266,
            265,
            255,
            246,
            232,
            227,
            216,
            213,
            211,
            199,
            182,
            173,
            169,
            168,
            163,
            158,
            151,
            143,
            127,
            98,
            70,
            66,
            65,
            57,
            52,
            51,
            48,
            45,
            43,
            40,
            36,
            31,
            26,
            25,
            24,
            14,
            8
        ],
        "hours_worked": 236,
        "pay_by_hours": 67732
    },
    {
        "id": 3,
        "full_name": "Nicolas De Tracy",
        "orders_id": [
            276,
            272,
            264,
            262,
            251,
            249,
            247,
            235,
            234,
            224,
            195,
            186,
            185,
            175,
            170,
            165,
            152,
            150,
            148,
            146,
            134,
            106,
            105,
            87,
            83,
            81,
            77,
            73,
            61,
            59,
            49,
            46,
            38,
            21,
            19,
            16,
            7,
            5,
            4,
            3
        ],
        "hours_worked": 211,
        "pay_by_hours": 60557
    },
    {
        "id": 4,
        "full_name": "Javier Cuenca",
        "orders_id": [
            278,
            260,
            259,
            217,
            207,
            202,
            180,
            154,
            149,
            130,
            123,
            109,
            101,
            88,
            72,
            62,
            60,
            58,
            54,
            50,
            47,
            41,
            39,
            30,
            29,
            15,
            13,
            11
        ],
        "hours_worked": 166,
        "pay_by_hours": 47642
    },
    {
        "id": 5,
        "full_name": "Lionel Andres Messi",
        "orders_id": [
            275,
            273,
            252,
            239,
            237,
            231,
            222,
            214,
            204,
            188,
            178,
            174,
            160,
            159,
            144,
            142,
            138,
            133,
            128,
            85,
            79,
            78,
            74,
            56,
            53,
            42,
            37,
            32,
            28,
            23,
            22,
            20,
            18
        ],
        "hours_worked": 163,
        "pay_by_hours": 46781
    },
    {
        "id": 6,
        "full_name": "Stephany Gonzalez",
        "orders_id": [
            267,
            253,
            243,
            238,
            233,
            223,
            218,
            208,
            190,
            177,
            176,
            162,
            135,
            124,
            118,
            115,
            112,
            93,
            80,
            71
        ],
        "hours_worked": 102,
        "pay_by_hours": 29274
    },
    {
        "id": 7,
        "full_name": "Alfredo Leuco",
        "orders_id": [
            274,
            271,
            270,
            258,
            250,
            225,
            220,
            200,
            196,
            192,
            191,
            171,
            161,
            156,
            153,
            147,
            141,
            140,
            139,
            96,
            86,
            84,
            67,
            63
        ],
        "hours_worked": 127,
        "pay_by_hours": 36449
    },
    {
        "id": 8,
        "full_name": "Luciano Mellera",
        "orders_id": [
            261,
            254,
            242,
            215,
            210,
            205,
            189,
            166,
            157,
            91,
            82,
            69,
            68
        ],
        "hours_worked": 59,
        "pay_by_hours": 16933
    },
    {
        "id": 9,
        "full_name": "Pepe Argento",
        "orders_id": [
            269,
            263,
            245,
            240,
            236,
            221,
            212,
            203,
            198,
            194,
            187,
            181,
            155,
            136,
            126,
            125,
            122,
            114,
            102,
            89,
            75,
            64
        ],
        "hours_worked": 112,
        "pay_by_hours": 32144
    },
    {
        "id": 10,
        "full_name": "Juan De Ejemplos",
        "orders_id": [
            268,
            256,
            244,
            241,
            230,
            229,
            228,
            226,
            209,
            201,
            197,
            193,
            184,
            183,
            145,
            132,
            131,
            129,
            121,
            120,
            119,
            113,
            111,
            108,
            104,
            100,
            95,
            76
        ],
        "hours_worked": 143,
        "pay_by_hours": 41041
    }
]
```

### Consulta GET filtrando por name=juan
Consulta en cURL:
```bash
curl --location 'http://localhost:8000/api/technicians/?name=juan'
```
Output:
```bash
[
    {
        "id": 1,
        "full_name": "Juan Ignacio Portilla Kitroser",
        "orders_id": [
            257,
            248,
            219,
            206,
            179,
            172,
            167,
            164,
            137,
            117,
            116,
            110,
            107,
            103,
            99,
            97,
            94,
            92,
            90,
            55,
            44,
            35,
            34,
            33,
            27,
            17,
            12,
            10,
            9,
            6,
            2,
            1
        ],
        "hours_worked": 159,
        "pay_by_hours": 45633
    },
    {
        "id": 10,
        "full_name": "Juan De Ejemplos",
        "orders_id": [
            268,
            256,
            244,
            241,
            230,
            229,
            228,
            226,
            209,
            201,
            197,
            193,
            184,
            183,
            145,
            132,
            131,
            129,
            121,
            120,
            119,
            113,
            111,
            108,
            104,
            100,
            95,
            76
        ],
        "hours_worked": 143,
        "pay_by_hours": 41041
    }
]
```

### Consulta POST (invalida)
Consulta en cURL:
```bash
curl --location --request POST 'http://localhost:8000/api/technicians/'
```

Output:
```bash
{
    "detail": "Method \"POST\" not allowed."
}
```

## 4. Servicio web para crear reporte

Consulta en cURL:
```bash
curl --location 'http://localhost:8000/api/report/'
```
Output:
```bash
{
    "average_amount": 25126.0,
    "below_average_technicians": {
        "Stephany Gonzalez": 17340,
        "Alfredo Leuco": 21590,
        "Luciano Mellera": 10030,
        "Pepe Argento": 19040,
        "Juan De Ejemplos": 24310
    },
    "with_higher_amount": "Lautaro Martinez",
    "with_lower_amount": "Luciano Mellera"
}
```
