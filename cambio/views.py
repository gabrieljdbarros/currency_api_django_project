from decimal import Decimal
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Rate, FxConfig
from .serializers import RateSerializer

class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('code')
    serializer_class = RateSerializer

    def update(self, request, *args, **kwargs):
     response = super().update(request, *args, **kwargs)
     obj = self.get_object()
     from .models import RateHistory
     RateHistory.objects.create(rate=obj, value_per_base=obj.rate_per_base)
     return response

    @action(detail=False, methods=['get'], url_path='convert')
    def convert(self, request):
        src = (request.query_params.get('from') or '').strip().upper()
        dst = (request.query_params.get('to') or '').strip().upper()
        amount_str = (request.query_params.get('amount') or '0').strip()

        if len(src) != 3 or not src.isalpha() or len(dst) != 3 or not dst.isalpha():
            return Response({"detail": "from/to devem ter 3 letras."}, status=400)
        try:
            amount = Decimal(amount_str)
            if amount < 0:
                raise ValueError()
        except Exception:
            return Response({"detail": "amount deve ser numérico >= 0."}, status=400)

        base = FxConfig.get_base()

        def get_rate(code):
            if code == base:
                return Decimal('1')
            return Rate.objects.get(code=code).rate_per_base

        try:
            rate_src = get_rate(src)
            rate_dst = get_rate(dst)
        except Rate.DoesNotExist:
            return Response({"detail": "Moeda ausente nas taxas cadastradas."}, status=400)

        converted = amount * (rate_src / rate_dst)
        return Response({
            "base": base,
            "from": src, "to": dst, "amount": str(amount),
            "rate_src_per_base": str(rate_src),
            "rate_dst_per_base": str(rate_dst),
            "converted": str(converted)
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='set-base')
    def set_base(self, request):
        code = (request.data.get('base') or '').strip().upper()
        if len(code) != 3 or not code.isalpha():
            return Response({"detail": "base deve ter 3 letras."}, status=400)
        FxConfig.objects.all().delete()
        FxConfig.objects.create(base_code=code)
        return Response({"message": "Base atualizada", "base": code}, status=200)
