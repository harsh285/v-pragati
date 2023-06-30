from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView
from django_tables2 import SingleTableView

from incomeslab.forms import IDPinGenerateForm
from incomeslab.models import Referral
from incomeslab.table import IDPinGenerateTable
from registration.models import IDPinGenerate, User


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'incomeslab/dashboard.html'


class GenerateIDPin(LoginRequiredMixin, CreateView, SingleTableView):
    model = IDPinGenerate
    table_class = IDPinGenerateTable
    form_class = IDPinGenerateForm
    template_name = 'incomeslab/id_pin_generate_table_view.html'
    table_pagination = {"per_page": 50}

    def get_queryset(self):
        query = super(GenerateIDPin, self).get_queryset()
        if not self.request.user.is_superuser:
            query = query.none()
        return query

    @transaction.atomic()
    def form_valid(self, form):
        if form.is_valid():
            form.instance.created_by = self.request.user
            form.instance.modified_by = self.request.user
            self.object: IDPinGenerate = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object:
            return reverse('incomeslab:generateIDPinDetail', kwargs={'pk_pin_id': self.object.id})
        else:
            return reverse('incomeslab:generateIDPin')


class GenerateIDPinDetail(LoginRequiredMixin, DetailView):
    model = IDPinGenerate
    template_name = 'incomeslab/generate_id_pin_detail.html'
    pk_url_kwarg = 'pk_pin_id'


class ReferralDetail(LoginRequiredMixin, TemplateView):
    template_name = 'incomeslab/sponser_detail.html'


class AddReferralCode(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        referral_code = request.POST['referral_code']
        flag1 = Referral.objects.filter(referred_user=request.user).exists()
        flag2 = User.objects.filter(referral_code=referral_code).first()
        flag3 = flag2 != request.user
        if not flag1 and flag2 and flag3:
            referral_amount = (request.user.share_price * 5) / 100
            print(request.user)
            Referral.objects.create(referrer=flag2, referred_user=request.user, referral_code=referral_code,
                                    referral_amount=referral_amount)
            messages.success(request, 'You have successfully applied the referral code.')
        else:
            messages.error(request, "Invalid referral code.", 'danger')
        return HttpResponseRedirect(reverse('incomeslab:referralDetail'))
