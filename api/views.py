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


@api_view(['GET']) # El "request" como argumento porque si no no funciona como vista
def get_report(request):
    technicians = Technician.objects.all()
    technician_with_payments = {}
    all_technicians_pay = 0

    for t in technicians:
        orders_hours = list(Pedido.objects.filter(technician=t.id).values("hours_worked"))
        technician_sum = 0
        
        for i in orders_hours:
            all_technicians_pay += Technician.pay_by_hours(i["hours_worked"])
            technician_sum += Technician.pay_by_hours(i["hours_worked"])
        technician_with_payments[f"{t.first_name} {t.last_name}"] = technician_sum      
    

    response = {
        "average_amount": all_technicians_pay / technicians.count() if technicians.count() != 0 else 0,
        "below_average_technicians": {k:v for (k,v) in technician_with_payments.items() if v < (all_technicians_pay / technicians.count() if technicians.count() != 0 else 0)}, 
        "with_higher_amount": max(technician_with_payments.items(), key=lambda x: x[1])[0] if technician_with_payments else None,
        "with_lower_amount": min(technician_with_payments.items(), key=lambda x: x[1])[0] if technician_with_payments else None
    }

    return JsonResponse(response, safe=False)