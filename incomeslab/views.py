from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView

from incomeslab.forms import IDPinGenerateForm
from incomeslab.models import Referral
from registration.models import IDPinGenerate, User


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'incomeslab/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        refer_queryset = self.request.user.referrals.all()
        try:
            context['sponsor_income'] = refer_queryset.aggregate(referral_amount=Sum('referral_amount'))[
                'referral_amount']
            context['total_sponsor'] = refer_queryset.count()
            print(context['sponsor_income'])
            if context['sponsor_income']:
                context['total_income'] = float(self.request.user.share_price) + context['sponsor_income']
                context['profit_percentage'] = context['sponsor_income'] * 100 / context['total_income']
            else:
                context['total_income'] = float(self.request.user.share_price)
                context['profit_percentage'] = 0
        except Exception as e:
            print("Error", e)
        return context


class GenerateIDPin(LoginRequiredMixin, CreateView):
    model = IDPinGenerate
    form_class = IDPinGenerateForm
    template_name = 'incomeslab/id_pin_generate_table_view.html'

    @transaction.atomic()
    def form_valid(self, form):
        if form.is_valid():
            form.instance.created_by = self.request.user
            form.instance.modified_by = self.request.user
            form.instance.share_price = form.instance.share_no * 1000
            self.object: IDPinGenerate = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object:
            return reverse('incomeslab:generateIDPinDetail', kwargs={'pk_pin_id': self.object.id})
        else:
            return reverse('incomeslab:generateIDPin')

    def get_context_data(self, **kwargs):
        context = super(GenerateIDPin, self).get_context_data(**kwargs)
        context['generated_ids'] = IDPinGenerate.objects.all().order_by('-created_at')
        return context


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


class MyProfileDetail(LoginRequiredMixin, TemplateView):
    template_name = 'incomeslab/my_profile.html'
