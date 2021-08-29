import csv
from statistics import median
from typing import Dict

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from transactions.enums import TransactionType, TransactionTypeParseError
from transactions.models import FBATransaction
from transactions.serializers import FBATransactionSerializer
from transactions.service import TransactionService
from utils.time_conversions import get_utc_time

# *** This will be highly relevant ***
# https://docs.djangoproject.com/en/3.1/topics/db/queries/


def parse_request_params(request_data: Dict) -> Dict:
    transaction_type = request_data.get("type")
    sku_list = request_data.get("skus")
    start = request_data.get("start")
    end = request_data.get("end")
    city = request_data.get("city")
    state = request_data.get("state")
    postal = request_data.get("postal")

    query_params = {}

    if transaction_type:
        query_params["type"] = TransactionType.text_to_enum(transaction_type).value
    if sku_list:
        sku_list = sku_list.split(",") if "," in sku_list else [sku_list]
        query_params["sku__in"] = [sku.lower() for sku in sku_list]
    if start:
        query_params["date__gt"] = get_utc_time(start)
    if end:
        query_params["date__lt"] = get_utc_time(end)
    if city:
        query_params["city"] = city.lower()
    if state:
        query_params["state"] = state.lower()
    if postal:
        query_params["postal"] = postal.lower()
    return query_params


class TransactionsListView(GenericAPIView):
    """
    Handles retrieving and creating transactions
    """

    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest):
        """
        Returns a list of transactions by the given filters

        params:
        type (str): Returns transactions of this type
        skus (list): Returns transactions with this SKU, should be sent/parsed as a comma separated string if multiple SKU's
        start (str): Returns transactions occurring after this date/time
        end (str): Returns transactions occurring before this date/time
        city (str): Returns transactions in this city
        state (str): Returns transactions in this state
        postal (str): Returns transactions in this postal address

        note: added by cat
        page (int): page to use for pagination
        page_size (int): page size to paginate by
        """

        request_data = request.GET

        # get the first page if user does not provide page
        page = int(request_data.get("page", 1))
        # paginate by defailt if input not provided
        paginate_by = int(request_data.get("page_size", 100))
        query_params = parse_request_params(request_data)
        transactions = FBATransaction.objects.all()

        if query_params:
            transactions = transactions.filter(**query_params)

        paginator = Paginator(transactions, paginate_by)
        total_transactions = len(transactions)

        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        serializer = FBATransactionSerializer(transactions, many=True)

        return Response(
            {
                "page_number": page,
                "page_size": paginate_by,
                "total_transactions": total_transactions,
                "transactions": serializer.data,
            }
        )

    @csrf_exempt
    def post(self, request: HttpRequest):
        """
        Imports a CSV file of transactions
        """
        files_submitted = 0
        ts = TransactionService()

        result = "ok"

        # https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.HttpRequest.FILES
        for _, file in request.FILES.items():
            decoded_file = file.read().decode("ISO-8859-1").splitlines()
            reader = list(csv.DictReader(decoded_file, delimiter=",", quotechar='"'))
            for row in reader:
                try:
                    ts.parse_line_from_dict(row)
                except TransactionTypeParseError as e:
                    result = f"Error parsing Order type - {e}. Please fix data and try again."
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            file.close()

            files_submitted += 1

        if not files_submitted:
            result = "Be sure to include enctype='multipart/form-data' in your request. No data uploaded"

        return Response(result, status=status.HTTP_200_OK)


class TransactionsStatsView(GenericAPIView):
    """
    Returns aggregated stats of transactions by the given filters
    """

    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest):
        """
        Returns a response containing the summed, average, and median totals for transactions using any given filters.

        params:
        type (str): Returns transactions of this type
        skus (list): Returns transactions with this SKU, should be sent/parsed as a comma separated string if multiple SKU's
        start (str): Returns transactions occurring after this date/time
        end (str): Returns transactions occurring before this date/time
        city (str): Returns transactions in this city
        state (str): Returns transactions in this state
        postal (str): Returns transactions in this postal address
        """
        # Contains all parameters sent in the query string
        request_data = request.GET

        query_params = parse_request_params(request_data)
        transactions = FBATransaction.objects.all()
        if query_params:
            transactions = transactions.filter(**query_params)

        totals = transactions.values_list("total", flat=True)

        if not len(totals):
            return Response("not enough data for results", status=status.HTTP_200_OK)

        transactions_sum = sum(totals)
        transactions_avg = transactions_sum / len(totals)
        transactions_median = median(totals)

        return Response(
            {
                "sum": transactions_sum,
                "avg": transactions_avg,
                "median": transactions_median,
            },
            status=status.HTTP_200_OK,
        )
