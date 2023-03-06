from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import viewsets, serializers
from rapihogar.models import Company, Technician, Pedido


class CompanySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Company
        fields = '__all__'


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()
    

@api_view(['GET'])
def technician_list(request):
    name = request.GET.get('name', '')
    queryset = list(Technician.objects.all().values("id", "first_name", "last_name"))

    if name:
        queryset = list(Technician.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)).values("id", "first_name", "last_name"))

    for i in queryset:
        orders = Pedido.objects.filter(technician=i["id"]).values("id", "hours_worked")

        orders_ids = [id["id"] for id in orders]
        
        i["full_name"] = f"{i['first_name']} {i['last_name']}"
        i.pop("first_name")
        i.pop("last_name")
        i["orders_id"] = orders_ids
        i["hours_worked"] = sum(i["hours_worked"] for i in orders)
        i["pay_by_hours"] = Technician.pay_by_hours(i["hours_worked"])
    
    return JsonResponse(queryset, safe=False)


# def get_report(request):
#     response = {
#         monto_promedio: 0,
#         tecnicos_debajo_del_promedio: [],
#         ultimo_mas_bajo: [],
#         ultimo_mas_alto: [],
#     }
#     Technician.objects.all()