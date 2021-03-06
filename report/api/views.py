from rest_framework import generics
from base_user.models import BaseUserModel
from sub_user.models import SubUserModel
from company.models import CompanyInfoModel
import datetime
from django.db.models import Q
from utils import utils
import uuid
today = datetime.datetime.today().strftime('%Y-%m-%d')


class DownloadReportPDF(generics.ListAPIView):

    permission_classes = []

    def get_base_user(self):
        if BaseUserModel.objects.filter(base_user=self.request.user).exists():
            return self.request.user.base_user
        elif SubUserModel.objects.filter(root_user=self.request.user).exists():
            return self.request.user.root_sub_user.base_user

    def get_credit_funds(self):
        return self.get_base_user().credit_funds.filter(is_deleted=False)
    
    def get_expend_records(self):
        return self.get_base_user().all_expenditure_records.filter(is_deleted=False)
    
    def get_remaining_credit_fund_amount(self, date_from, date_to):

        expend_obj = self.get_expend_records().filter(
            Q(is_verified=True),
            Q(added__date__lte=date_to),
            Q(added__date__gte=date_from)
            )
        credit_obj = self.get_credit_funds().filter(
            Q(added__date__lte=date_to),
            Q(added__date__gte=date_from)
        )

        all_expend_obj_amounts = [obj.amount for obj in expend_obj]
        all_credit_obj_amounts = [obj.amount for obj in credit_obj]

        total_expend_amount = utils.sum_int_of_array(all_expend_obj_amounts)
        total_credit_amount = utils.sum_int_of_array(all_credit_obj_amounts)

        remaining_credit_fund_amount = total_credit_amount - total_expend_amount

        return remaining_credit_fund_amount

        all_expend_amounts = [obj.amount for obj in expend_obj_ref_or_ret]
        all_credit_amounts = [obj.amount for obj in credit_obj]

        total_expend_amount = utils.sum_int_of_array(all_expend_amounts)
        total_credit_amount = utils.sum_int_of_array(all_credit_amounts)

        todays_open_credit_fund = total_credit_amount - total_expend_amount

        return todays_open_credit_fund
    
    def get_credit_amount(self, date_from, date_to):
        expend_obj_ref_or_ret = self.get_expend_records().filter(
            Q(is_verified=True),
            Q(added__date__lte=date_to),
            Q(added__date__gte=date_from),
            Q(is_for_refund=True) | Q(is_for_return=True)
            )

        credit_obj = self.get_credit_funds().filter(
            Q(added__date__lte=date_to),
            Q(added__date__gte=date_from),
            )

        all_expend_amounts = [obj.amount for obj in expend_obj_ref_or_ret]
        all_credit_amounts = [obj.amount for obj in credit_obj]

        total_expend_amount = utils.sum_int_of_array(all_expend_amounts)
        total_credit_amount = utils.sum_int_of_array(all_credit_amounts)

        credit_amount = total_credit_amount - total_expend_amount

        return credit_amount
    
    def get_debit_amount(self, date_from, date_to):
        expend_obj_non_ref_and_non_ret = self.get_expend_records().filter(
            Q(is_verified=True),
            Q(added__date__lte=date_to),
            Q(added__date__gte=date_from),
            Q(is_for_refund=False),
            Q(is_for_return=False)
            )
        all_expend_amounts = [obj.amount for obj in expend_obj_non_ref_and_non_ret]

        todays_open_debit_amount = utils.sum_int_of_array(all_expend_amounts)

        return todays_open_debit_amount
    
    def get(self, request, *args, **kwargs):
        date_from = self.request.query_params.get('date_from', datetime.date.today())
        date_to = self.request.query_params.get('date_to', datetime.date.today())

        company = CompanyInfoModel.objects.get(base_user=self.get_base_user())

        context = {
            'company': company,
            'pdf_name': f'Expenditure {today}',
            'date': datetime.datetime.now(),
            'page_unique_id': uuid.uuid4(),
            'credit_items': self.get_credit_funds().filter(
                Q(added__date__lte=date_to),
                Q(added__date__gte=date_from)
                ),
            'debit_items': self.get_expend_records().filter(
                Q(added__date__lte=date_to),
                Q(added__date__gte=date_from),
                is_verified=True
                ),
            'total_credit_amount': self.get_credit_amount(date_from=date_from, date_to=date_to),
            'total_debit_amount': self.get_debit_amount(date_from=date_from, date_to=date_to),
            'total_remaining_balance': self.get_remaining_credit_fund_amount()
        }

        pdf = utils.django_render_to_pdf('expenditure_pdf_template.html', context)
        return pdf

