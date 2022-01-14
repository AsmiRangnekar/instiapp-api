"""Views for mess menu."""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from messmenu.models import Hostel, MessCalEvent
from messmenu.serializers import HostelSerializer, MessCalEventSerializer
from roles.helpers import login_required_ajax
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings


@api_view(['GET', ])
def get_mess(request):
    """Get mess menus of all hostels."""
    queryset = Hostel.objects.all()
    queryset = HostelSerializer.setup_eager_loading(queryset)
    return Response(HostelSerializer(queryset, many=True).data)

@api_view(['GET', ])
def getUserMess(request):
    """Get mess status for a user"""

    if not request.user:
        return Response({
            'message': 'unauthenticated',
            'detail': 'Log in to continue!'
        }, status=401)

    user = request.user.profile
    rollno = user.roll_no
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    
    curr = start
    
    items = []
    
    while curr<=end:
        res = requests.get(f"{settings.MESSI_BASE_URL}/api/get_details?roll={rollno}&year={curr.year}&month={curr.month}")

        if res.status_code!=200:
            curr = curr + relativedelta(months=1)
            continue
            # print("Error in getting details")
            # return Response({"error":"Error in getting mess calendar"})
        
        data = res.json()

        try:
            details = data["details"]
            
            for d in details:
                k = binaryDecode(d)
                mealnum = k["meal"]
                if(mealnum == "000"):
                    title = "Breakfast"
                elif(mealnum == "001"):
                    title = "Lunch"
                elif(mealnum == "010"):
                    title = "Snacks"
                elif(mealnum == "011"):
                    title = "Dinner"
                else:
                    title = "Error"
                
                date = datetime(curr.year, curr.month, k["day"], k["time"]//60, k["time"]%60)
                hostel = k["hostel"]
                
                item, c = MessCalEvent.objects.get_or_create(user = user, datetime = date, hostel = hostel)
                if c:
                    item.title = title
                    item.save()
                
                items.append(item)

        except KeyError:
            curr = curr + relativedelta(months=1)
            continue
            
        curr = curr + relativedelta(months=1)
    
    return Response(MessCalEventSerializer(items, many=True).data)    
    

def binaryDecode(x):
    b_x = "{0:b}".format(int(x))
    day = int(b_x[len(b_x)-5:len(b_x)],2)
    meal = b_x[len(b_x)-8:len(b_x)-5]
    time = int(b_x[len(b_x)-19:len(b_x)-8],2)
    hostel = int(b_x[0:len(b_x)-19],2)
    return {'hostel':hostel, 'time':time, 'meal':meal, 'day':day}