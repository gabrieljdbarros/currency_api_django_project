from rest_framework import serializers
from .models import Rate, FxConfig

class RateSerializer(serializers.ModelSerializer):
    base = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rate
        fields = ['id', 'code', 'rate_per_base', 'base']

    def get_base(self, obj):
        return FxConfig.get_base()

    def validate_code(self, v):
        v = (v or '').strip().upper()
        if len(v) != 3 or not v.isalpha():
            raise serializers.ValidationError("Código ISO-4217 de 3 letras.")
        return v

    def validate_rate_per_base(self, v):
        if v is None or v <= 0:
            raise serializers.ValidationError("rate_per_base deve ser > 0.")
        return v
