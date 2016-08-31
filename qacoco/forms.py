from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import *
from base_models import QACocoModel
from models import VideoContentApproval, VideoQualityReview, DisseminationQuality, AdoptionVerification

from geographies.models import District
from videos.models import Video, Category, SubCategory, NonNegotiable


def save_all(instances, user, id):
    for instance in instances:
        if(id):
            if instance.user_created_id == None:
                instance.user_created_id = user
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        instance.save()

class UserModelDistrictMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.district_name)

class UserModelVideoMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s) (%s)" % (obj.title, obj.village.block.district.district_name, obj.language.language_name)

class QACocoUserForm(forms.ModelForm):
    districts = UserModelDistrictMultipleChoiceField(
        widget=FilteredSelectMultiple(
                                      verbose_name='districts',
                                      is_stacked=False
                                     ),
        queryset=District.objects.all()
        )
    videos = UserModelVideoMultipleChoiceField(
        widget=FilteredSelectMultiple(
                                      verbose_name='videos',
                                      is_stacked=False
                                     ),
        queryset=Video.objects.all().prefetch_related('language', 'village__block__district'),
        required=False
        )

class QACocoModelForm(ModelForm):
    def save(self, commit=True, user = None, id = None,  *args, **kwargs):
        instance = super(QACocoModelForm, self).save(commit=False)
        if (id):
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        if commit:
            instance.save()
            self.save_m2m()  
        return instance
        
    class Meta:
        model = QACocoModel
        exclude = ('user_modified',)

class VideoContentApprovalForm(QACocoModelForm):
    class Meta:
        model = VideoContentApproval
        exclude = ()

class VideoQualityReviewForm(QACocoModelForm):
    class Meta:
        model = VideoQualityReview
        exclude = ()

class DisseminationQualityForm(QACocoModelForm):
    class Meta:
        model = DisseminationQuality
        exclude = ()

class NonNegotiableForm(QACocoModelForm):       
    class Meta:
        model = NonNegotiable
        exclude = ()

class AdoptionVerificationForm(QACocoModelForm):
    class Meta:
        model = AdoptionVerification
        exclude = ()
