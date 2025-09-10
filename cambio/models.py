from django.db import models

class FxConfig(models.Model):
    base_code = models.CharField(max_length=3, default='BRL', unique=True)

    def save(self, *args, **kwargs):
        if self.base_code:
            self.base_code = self.base_code.strip().upper()
        super().save(*args, **kwargs)

    @classmethod
    def get_base(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create(base_code='BRL')
        return obj.base_code

class Rate(models.Model):
    code = models.CharField(max_length=3, unique=True)
    rate_per_base = models.DecimalField(max_digits=16, decimal_places=6)

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} = {self.rate_per_base} (por 1 {FxConfig.get_base()})"

class RateHistory(models.Model):
    rate = models.ForeignKey('Rate', on_delete=models.CASCADE, related_name='history')
    value_per_base = models.DecimalField(max_digits=16, decimal_places=6)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rate.code}@{self.changed_at:%Y-%m-%d %H:%M} = {self.value_per_base}"