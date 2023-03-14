from util.http import build_response
from rest_framework.decorators import api_view

@api_view(['POST'])
def index(request):
    return build_response(200, None, {"PERFECT":"OKAY"})
    