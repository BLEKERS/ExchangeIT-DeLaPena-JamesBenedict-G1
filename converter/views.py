from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import user_required

from .forms import ConversionForm, FavoritePairForm
from .models import ConversionHistory, Currency, FavoritePair
from .services import get_exchange_rate


@login_required
@user_required
def convert_view(request):
    initial = {}
    if request.method == "GET":
        codes = [request.GET.get("from", ""), request.GET.get("to", "")]
        currencies = Currency.objects.filter(
            is_active=True, currency_code__in=[code for code in codes if code]
        )
        by_code = {currency.currency_code: currency for currency in currencies}
        if codes[0] in by_code:
            initial["from_currency"] = by_code[codes[0]]
        if codes[1] in by_code:
            initial["to_currency"] = by_code[codes[1]]

    form = ConversionForm(request.POST or None, initial=initial or None)

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
        elif result.get("error") == "unsupported_currency":
            messages.error(
                request, "This currency pair is not supported by our rate provider."
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


@login_required
@user_required
def favorite_list_view(request):
    favorites = FavoritePair.objects.filter(user=request.user).select_related(
        "from_currency", "to_currency"
    )
    form = FavoritePairForm(user=request.user)
    return render(
        request, "converter/favorites.html", {"favorites": favorites, "form": form}
    )


@login_required
@user_required
def favorite_add_view(request):
    if request.method == "POST":
        form = FavoritePairForm(request.POST, user=request.user)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
            messages.success(request, "Favorite pair added.")
            return redirect("converter:favorites")
    else:
        form = FavoritePairForm(user=request.user)

    favorites = FavoritePair.objects.filter(user=request.user).select_related(
        "from_currency", "to_currency"
    )
    return render(
        request, "converter/favorites.html", {"favorites": favorites, "form": form}
    )


@login_required
@user_required
def favorite_edit_view(request, pk):
    favorite = get_object_or_404(FavoritePair, pk=pk, user=request.user)
    if request.method == "POST":
        form = FavoritePairForm(request.POST, instance=favorite, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Favorite pair updated.")
            return redirect("converter:favorites")
    else:
        form = FavoritePairForm(instance=favorite, user=request.user)

    favorites = FavoritePair.objects.filter(user=request.user).select_related(
        "from_currency", "to_currency"
    )
    return render(
        request,
        "converter/favorites.html",
        {"favorites": favorites, "form": form, "edit_pk": favorite.pk},
    )


@login_required
@require_POST
def favorite_delete_view(request, pk):
    favorite = get_object_or_404(FavoritePair, pk=pk, user=request.user)
    favorite.delete()
    messages.success(request, "Favorite pair deleted.")
    return redirect("converter:favorites")
