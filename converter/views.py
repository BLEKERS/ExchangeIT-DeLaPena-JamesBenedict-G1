from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import user_required

from .forms import ConversionForm
from .models import ConversionHistory
from .services import get_exchange_rate


@login_required
@user_required
def convert_view(request):
    form = ConversionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        from_currency = form.cleaned_data["from_currency"]
        to_currency = form.cleaned_data["to_currency"]
        amount = form.cleaned_data["amount"]
        result = get_exchange_rate(
            from_currency.currency_code, to_currency.currency_code
        )

        if result is None:
            messages.error(
                request,
                "Could not fetch exchange rate for this pair. Please try again later.",
            )
        else:
            rate = Decimal(str(result["rate"]))
            converted_amount = (amount * rate).quantize(Decimal("0.01"))
            ConversionHistory.objects.create(
                user=request.user,
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                exchange_rate=rate,
                converted_amount=converted_amount,
            )
            messages.success(
                request,
                f"Successfully converted {amount} {from_currency.currency_code} "
                f"to {converted_amount} {to_currency.currency_code}.",
            )
            return redirect("converter:convert")

    return render(request, "converter/convert.html", {"form": form})


@login_required
@user_required
def history_view(request):
    history = ConversionHistory.objects.filter(user=request.user)
    return render(request, "converter/history.html", {"history": history})


@login_required
@require_POST
def delete_history_view(request, pk):
    record = get_object_or_404(ConversionHistory, pk=pk, user=request.user)
    record.delete()
    messages.success(request, "Conversion record deleted.")
    return redirect("converter:history")
