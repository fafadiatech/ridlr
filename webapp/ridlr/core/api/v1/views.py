from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import QuestionBank, Invitation

class QuestionsAPI(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        invitation_code = request.GET.get("invitation_code", "")

        # error handing
        if invitation_code == "":
            raise APIException("Invalid Invitation Code")

        if Invitation.objects.filter(invitation_code=invitation_code, consumed=True).exists():
            raise APIException("Invitation code already consumed")

        contents = QuestionBank.generate(invitation_code)
        return Response(contents)