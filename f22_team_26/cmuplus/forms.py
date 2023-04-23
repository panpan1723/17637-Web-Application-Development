from django import forms
from cmuplus.models import CourseExperience, Post, Comment
from bootstrap_modal_forms.forms import BSModalModelForm

class CourseExperienceForm(forms.ModelForm):

    # Customize validations
    def clean(self):
        # Calls parent (forms.Form) .clean function, gets a dict of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        grade = cleaned_data.get('grade')
        semester = cleaned_data.get('semester').strip()
        # grade validation
        if grade != -1 and (grade < 0 or grade > 100):
            raise forms.ValidationError("Grade is not valid.")
        # semester validation
        if len(semester) != 3 or semester[0] not in ['F', 'S', 'M'] or not semester[1:].isnumeric():
            raise forms.ValidationError("Semester format is wrong. Enter F/M/S with two numbers.")
        return cleaned_data

    class Meta:
        model = CourseExperience
        fields = ('course_number', 'course_name', 'semester', 'credit', 'professor_firstname', 'professor_lastname', 
                  'subject', 'content', 'credit', 'load', 'grade_satisfication', 'difficulty','grade', 'is_anonymous')
        widgets = {
            'content': forms.Textarea(attrs={'rows': '3', 'cols': '70', 'placeholder': 'can get sufficient sleep?'}),
            'subject': forms.Textarea(attrs={'rows': '1'}),
            'grade': forms.NumberInput(attrs={'style': 'width:21ch', 'placeholder': 'Enter -1 if not disclose'}),
            'course_number': forms.TextInput(attrs={'placeholder': 'e.g. 17637'}),
            'course_name': forms.TextInput(attrs={'readonly': True, 'style': 'width:65ch'}),
            'professor_lastname': forms.TextInput(attrs={'readonly': True, 'rows': '1', 'cols': '20'}),
            'semester': forms.TextInput(attrs={'placeholder': 'F22/M21/S23'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'title': forms.Textarea(attrs={'rows':1}),
            'text': forms.Textarea(attrs={'rows':3}),
        }

class CommentForm(BSModalModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows':2}),
        }