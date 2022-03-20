from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from Account.models import Person
from Account.views import CreateAccountForm


# Create your tests here.
class PersonTestCase(TestCase):
    def setUp(self):
        self.create_user()
        self.create_person()

    def create_user(self):
        User = get_user_model()
        return User.objects.create_user('test_user', 'test_user@mybank.com', 'test_user')

    def create_person(self):
        User = get_user_model()
        user = User.objects.get(username='test_user')
        return Person.objects.create(first_name='John',
                                     last_name='Sand',
                                     iban='NL48RABO5641531316',
                                     created_timestamp=timezone.now(),
                                     updated_timestamp=timezone.now(),
                                     created_by=user,
                                     updated_by=user)

    # TESTING MODELS
    def test_person_created(self):
        person = Person.objects.get(iban="NL48RABO5641531316")

        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Sand')

    def test_person_updated(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        person.iban = 'FR3512739000709681586494V41'
        person.save()
        person = Person.objects.get(iban="FR3512739000709681586494V41")

        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Sand')

    def test_person_deleted(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        person.delete()
        persons = Person.objects.filter(iban="NL48RABO5641531316")

        self.assertEqual(len(persons), 0)

    def test_user_authentication(self):
        user = authenticate(username='test_user', password='test_user')

        self.assertIsNot(user, None)

    # TESTING VIEWS
    def test_person_list_view(self):
        url = reverse("account-list")
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_person_create_view(self):
        url = reverse("account-create")
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_person_detail_view(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        url = reverse("account-detail", args={person.pk})
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_person_update_view(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        url = reverse("account-update", args={person.pk})
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_person_delete_view(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        url = reverse("account-delete", args={person.pk})
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    # TESTING FORMS
    def test_valid_form(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        data = {'first_name': 'Lucy',
                'last_name': 'Hawk',
                'iban': 'PT57003506514378815181673', }
        form = CreateAccountForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        person = Person.objects.get(iban="NL48RABO5641531316")
        data = {'first_name': 'Lucy',
                'last_name': 'Hawk',
                'iban': 'PT57003506514378815181675', }
        form = CreateAccountForm(data=data)
        self.assertFalse(form.is_valid())
