import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Rate, FxConfig
from .forms import RateForm, BatchForm, ConvertForm

def home(request):
    return render(request, "cambio/home.html", {"base": FxConfig.get_base()})

def rate_list(request):
    rates = Rate.objects.order_by("code")
    return render(request, "cambio/rate_list.html", {"rates": rates, "base": FxConfig.get_base()})

def rate_edit(request, pk):
    rate = get_object_or_404(Rate, pk=pk)
    old_val = rate.rate_per_base
    if request.method == "POST":
        form = RateForm(request.POST, instance=rate)
        if form.is_valid():
            obj = form.save()
            # só cria o historico se tiver mudança
            if old_val != obj.rate_per_base:
                from .models import RateHistory
                RateHistory.objects.create(rate=obj, value_per_base=obj.rate_per_base)
            messages.success(request, "Taxa atualizada.")
            return redirect("rate_list")
    else:
        form = RateForm(instance=rate)
    return render(request, "cambio/rate_edit.html", {"form": form, "rate": rate, "base": FxConfig.get_base()})

def rate_history(request, pk):
    rate = get_object_or_404(Rate, pk=pk)
    hist = rate.history.order_by('-changed_at')
    return render(
        request,
        "cambio/rate_history.html",
        {"rate": rate, "history": hist, "base": FxConfig.get_base()}
    )
def rate_delete(request, pk):
    rate = get_object_or_404(Rate, pk=pk)
    if request.method == "POST":
        rate.delete()
        messages.success(request, "Taxa removida.")
        return redirect("rate_list")
    return render(request, "cambio/rate_delete.html", {"rate": rate, "base": FxConfig.get_base()})

def rate_create(request):
    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Taxa salva.")
            return redirect("rate_list")
    else:
        form = RateForm()
    return render(request, "cambio/rate_create.html", {"form": form, "base": FxConfig.get_base()})

def rate_batch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            try:
                import json
                from decimal import Decimal
                from .models import RateHistory

                data = json.loads(form.cleaned_data["rates_json"])
                if not isinstance(data, dict) or not data:
                    raise ValueError("JSON deve ser {moeda: taxa}.")

                for code, val in data.items():
                    obj, created = Rate.objects.update_or_create(
                        code=str(code).strip().upper(),
                        defaults={"rate_per_base": Decimal(str(val))}
                    )
                    RateHistory.objects.create(
                        rate=obj,
                        value_per_base=obj.rate_per_base
                    )

                messages.success(request, "Taxas atualizadas e histórico registrado.")
                return redirect("rate_list")
            except Exception as e:
                messages.error(request, f"Erro no JSON: {e}")
    else:
        form = BatchForm()
    return render(request, "cambio/rate_batch.html", {"form": form, "base": FxConfig.get_base()})

def convert_view(request):
    result = None
    if request.method == "POST":
        form = ConvertForm(request.POST)
        if form.is_valid():
            src = form.cleaned_data["source"].strip().upper()
            dst = form.cleaned_data["target"].strip().upper()
            amt = form.cleaned_data["amount"]
            try:
                rate_src = Decimal('1') if src == FxConfig.get_base() else Rate.objects.get(code=src).rate_per_base
                rate_dst = Decimal('1') if dst == FxConfig.get_base() else Rate.objects.get(code=dst).rate_per_base
                result = (amt * rate_src) / rate_dst
            except Rate.DoesNotExist:
                messages.error(request, "Moeda não cadastrada. Cadastre em Rates.")
    else:
        form = ConvertForm()
    return render(request, "cambio/convert.html", {"form": form, "result": result, "base": FxConfig.get_base()})
