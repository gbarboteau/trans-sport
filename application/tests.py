from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse, reverse_lazy
from .admin import UserAdmin, CategoryAdmin, PlaceAdmin, CommentAdmin, AdressAdmin
from .models import User, Category, Adress, Place, Comment
from .utils import GetCityDepartementAndRegion, GetZipCodeFromDepartment, DoesKeyExists, GetNote
from django.core import mail
from django.shortcuts import render, redirect, get_object_or_404


class ModelsTestCase(TestCase):
    """Tests of the models"""
    def test_user_object(self):
        """Test of the aliment model"""
        test_user = User.objects.create(username="Yoshi69", email="petitprincedurai@caramail.com", password="VIVETOTOSS", gender='Femme trans', about_me='J\'aime la vie et le zouk')
        self.assertIs(test_user.username, "Yoshi69")

    def test_category_object(self):
        """Test of the substitute model"""
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        self.assertIs(test_category.name, "Kebabs")

    def test_adress_object(self):
        """Test of the adress model"""
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        self.assertIs(test_adress.street_adress, '20 rue Kirby54')

    def test_place_object(self):
        """Test of the place model"""
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        self.assertIs(test_place.name, 'Bar à Chicha de Knuckles')

    def test_comment_object(self):
        """Test of the comment model"""
        test_user = User.objects.create(username="Yoshi69", email="petitprincedurai@caramail.com", password="VIVETOTOSS", gender='Femme trans', about_me='J\'aime la vie et le zouk')
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_comment = Comment.objects.create(comment='J\'adore, un plaisir pour les sens !', user=test_user, place=test_place, score_global='P', can_you_enter=False, are_you_safe_enough=False, is_mixed_lockers=True, is_inclusive_lockers=False, has_respectful_staff=False)
        self.assertIs(test_comment.comment, 'J\'adore, un plaisir pour les sens !')


class UtilsTestsCase(TestCase):
    """Tests all of the utils fonction"""
    def test_getcitydepartmentandregion(self):
        """Tests the GetCityDepartementAndRegion() function"""
        test_postal_code = '83720'
        self.assertSequenceEqual(GetCityDepartementAndRegion(test_postal_code), ['TRANS EN PROVENCE', 'Var', "Provence-Alpes-Côte d'Azur"])

    def test_getzipcodefromdepartement(self):
        """Tests the GetZipCodeFromDepartment() function"""
        test_zipcode = 'Var'
        self.assertDictEqual(GetZipCodeFromDepartment(test_zipcode), {'postal_code': '83', 'department': 'Var'})

    def test_doeskeyexists_true(self):
        """Tests the DoesKeyExists() function"""
        test_key = 'name'
        test_dict = {'age': 16, 'name': 'Miles Prowler', 'job': 'Mecanic'}
        self.assertIs(DoesKeyExists(test_key, test_dict), True)

    def test_doeskeyexists_false(self):
        """Tests the DoesKeyExists() function"""
        test_key = 'pseudo'
        test_dict = {'age': 16, 'name': 'Miles Prowler', 'job': 'Mecanic'}
        self.assertIs(DoesKeyExists(test_key, test_dict), False)

    def test_getnote(self):
        """Tests the GetNote() function"""
        note = 1.5
        positive_reviews = 3
        negative_reviews = 7
        self.assertEqual(note, GetNote(positive_reviews, negative_reviews))


class IndexPageTestCase(TestCase):
    """Tests of the index view"""
    def setUp(self):
        test_postal_code_1 = '83720'
        test_values_1 = GetCityDepartementAndRegion(test_postal_code_1)
        test_adress_1 = Adress.objects.create(region=test_values_1[2], departement=test_values_1[1], postal_code=test_postal_code_1, city=test_values_1[0], street_adress='20 rue Kirby54')
        test_category_1 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_1 = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category_1, adress=test_adress_1, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_1.save()
        test_postal_code_2 = '33000'
        test_values_2 = GetCityDepartementAndRegion(test_postal_code_2)
        test_adress_2 = Adress.objects.create(region=test_values_2[2], departement=test_values_2[1], postal_code=test_postal_code_2, city=test_values_2[0], street_adress='20 rue Kirby54')
        test_category_2 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_2 = Place.objects.create(name='Kebab de Robotnik', description='Un max de plaisir non-fruité !', can_be_seen=True, category=test_category_2, adress=test_adress_2, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_2.save()

    def test_index_page(self):
        """Tests the access of the index page"""
        test_place_1 = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place_2 = get_object_or_404(Place, name='Kebab de Robotnik')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class UserCreationTestCase(TestCase):
    """Tests of the create-account view"""
    def test_create_account_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('create_account'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        """Checks if users can create an account"""
        response = self.client.post(reverse('create_account'), {'username':"Yoshi54", 'email':"yoshi54@caramail.com", 'password1':"FANDECYRILHANOUNA", 'password2':"FANDECYRILHANOUNA", 'gender': 'Femme trans'})
        self.assertEqual(response.status_code, 200)


class UserLoginTestCase(TestCase):
    """Tests of the account view"""
    def setUp(self):
        user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        user.save()

    def test_sign_in_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

    def test_signing_in(self):
        """Checks if users can log in"""
        response = self.client.post(reverse('login_view'), {'username':"Yoshi54", 'password':"FANDECYRILHANOUNA"}, follow=True)
        self.assertEqual(response.status_code, 200)


class LogoutTestCase(TestCase):
    """Tests of the logout view"""
    def setUp(self):
        user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        user.save()
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")

    def test_logout_page(self):
        """Checks if users can log out"""
        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)


class AccountTestCase(TestCase):
    """Tests of the account view"""
    def setUp(self):
        user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        user.save()

    def test_account_logged_in(self):
        """Checks if the user is logged in"""
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_logged_in(self):
        """Checks if the user is not logged in"""
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)


class CreateAccountTestCase(TestCase):
    """Tests of the create-account view"""
    def test_create_account_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('create_account'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        """Checks if users can create an account"""
        response = self.client.post(reverse('create_account'), {'username':"Yoshi54", 'email':"yoshi54@caramail.com", 'password1':"FANDECYRILHANOUNA", 'password2':"FANDECYRILHANOUNA", 'gender': 'Femme trans'})
        self.assertEqual(response.status_code, 200)


class ModifyAccountTestCase(TestCase):
    """Tests of the modify-account view"""
    def setUp(self):
        user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        user.save()

    def test_modify_account_page(self):
        """Checks if the user is logged in"""
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('modify_account'))
        self.assertEqual(response.status_code, 302)

    def test_modify_account_page_not_logged_in(self):
        """Checks if the user is not logged in"""
        response = self.client.get(reverse('modify_account'))
        self.assertEqual(response.status_code, 302)


class SuggestingNewPlaceTestCase(TestCase):
    """Tests of the suggesting-new-place view"""
    def setUp(self):
        test_user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user.save()

    def test_access_page_logged_in(self):
        """Checks if the user is logged in"""
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        response = self.client.get('/suggesting-new-place/')
        self.assertEqual(response.status_code, 302)

    def test_access_page_not_logged_in(self):
        """Checks if the user is not logged in"""
        response = self.client.get('/suggesting-new-place/')
        self.assertEqual(response.status_code, 302)

    def test_suggest_new_place(self):
        """Checks if you can add a place"""
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        # test_comment = Comment.objects.get(comment="très bon", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        response = self.client.get('/suggesting-new-place/', {'name': 'Bar à Chicha de Knuckles', 'picture': 'https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000', 'description': 'Un lieu convivial pour toute la famille !', 'category': test_category.id, 'website': 'perdu.com', 'contact_mail': 'salam@haleykoum.com', 'contact_phone': '0666666666', 'street_adress': '978 route de Draguignan', 'postal_code': '83720', 'comment': 'J\'ai apprécié', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_suggest_new_place_error(self):
        """Checks if an empty form does not add a place"""
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        # test_comment = Comment.objects.get(comment="très bon", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        response = self.client.get('/suggesting-new-place/', {'name': 'Bar à Chicha de Knuckles', 'picture': 'https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000', 'description': 'Un lieu convivial pour toute la famille !', 'category': test_category.id, 'website': 'perdu.com', 'contact_mail': 'salam@haleykoum.com', 'contact_phone': '0666666666', 'street_adress': '978 route de Draguignan', 'postal_code': '83720', 'comment': 'J\'ai apprécié', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


class SearchPlacesTestCase(TestCase):
    """Tests of the index view"""
    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans')
        user.save()

    def test_search_page_not_logged_in(self):
        """Checks if the page is not accessible when
        users aren't logged in
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_search_page_logged_in(self):
        """Checks if the page is accessible when
        users are logged in
        """
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)


class AllPlacesTestCase(TestCase):
    """Tests of the all-places view"""
    def setUp(self):
        test_postal_code_1 = '83720'
        test_values_1 = GetCityDepartementAndRegion(test_postal_code_1)
        test_adress_1 = Adress.objects.create(region=test_values_1[2], departement=test_values_1[1], postal_code=test_postal_code_1, city=test_values_1[0], street_adress='20 rue Kirby54')
        test_category_1 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_1 = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category_1, adress=test_adress_1, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_1.save()
        test_postal_code_2 = '33000'
        test_values_2 = GetCityDepartementAndRegion(test_postal_code_2)
        test_adress_2 = Adress.objects.create(region=test_values_2[2], departement=test_values_2[1], postal_code=test_postal_code_2, city=test_values_2[0], street_adress='20 rue Kirby54')
        test_category_2 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_2 = Place.objects.create(name='Kebab de Robotnik', description='Un max de plaisir non-fruité !', can_be_seen=True, category=test_category_2, adress=test_adress_2, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_2.save()

    def test_places_page(self):
        """Checks if the page is accessible"""
        test_place_1 = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place_2 = get_object_or_404(Place, name='Kebab de Robotnik')
        response = self.client.get(reverse('all_places'))
        self.assertEqual(response.status_code, 200)


class AllDepartmentsTestCase(TestCase):
    """Tests of the all-departments view"""
    def setUp(self):
        test_postal_code_1 = '83720'
        test_values_1 = GetCityDepartementAndRegion(test_postal_code_1)
        test_adress_1 = Adress.objects.create(region=test_values_1[2], departement=test_values_1[1], postal_code=test_postal_code_1, city=test_values_1[0], street_adress='20 rue Kirby54')
        test_category_1 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_1 = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category_1, adress=test_adress_1, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_1.save()
        test_postal_code_2 = '33000'
        test_values_2 = GetCityDepartementAndRegion(test_postal_code_2)
        test_adress_2 = Adress.objects.create(region=test_values_2[2], departement=test_values_2[1], postal_code=test_postal_code_2, city=test_values_2[0], street_adress='20 rue Kirby54')
        test_category_2 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_2 = Place.objects.create(name='Kebab de Robotnik', description='Un max de plaisir non-fruité !', can_be_seen=True, category=test_category_2, adress=test_adress_2, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_2.save()

    def test_places_page(self):
        """Checks if the page is accessible"""
        departments = Place.objects.filter(can_be_seen=True).values('adress__departement').distinct()
        departments_with_zip_code = []
        for department in departments:
            departments_with_zip_code.append(GetZipCodeFromDepartment(list(department.values())[0]))
        response = self.client.get(reverse('all_departments'))
        self.assertEqual(response.status_code, 200)


class PlacesByDepartmentTestCase(TestCase):
    """Tests of the places-by-departments view"""
    def setUp(self):
        test_postal_code_1 = '83720'
        test_values_1 = GetCityDepartementAndRegion(test_postal_code_1)
        test_adress_1 = Adress.objects.create(region=test_values_1[2], departement=test_values_1[1], postal_code=test_postal_code_1, city=test_values_1[0], street_adress='20 rue Kirby54')
        test_category_1 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_1 = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category_1, adress=test_adress_1, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_1.save()
        test_postal_code_2 = '33000'
        test_values_2 = GetCityDepartementAndRegion(test_postal_code_2)
        test_adress_2 = Adress.objects.create(region=test_values_2[2], departement=test_values_2[1], postal_code=test_postal_code_2, city=test_values_2[0], street_adress='20 rue Kirby54')
        test_category_2 = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place_2 = Place.objects.create(name='Kebab de Robotnik', description='Un max de plaisir non-fruité !', can_be_seen=True, category=test_category_2, adress=test_adress_2, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place_2.save()

    def test_places_page(self):
        """Checks if the page is accessible"""
        test_place_1 = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place_2 = get_object_or_404(Place, name='Kebab de Robotnik')
        response = self.client.get('/all-departments/' + str(83) + '/')
        self.assertEqual(response.status_code, 200)


class ShowPlaceTestCase(TestCase):
    """Tests of the show-place view"""
    def setUp(self):
        test_user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user.save()
        test_postal_code = '75001'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='13 rue saint-denis')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place.save()
        test_comment = Comment.objects.create(comment="j'adore", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False, place_id=test_place.id, user_id=test_user.id)
        test_comment.save()
        test_place.note_global = 4 
        test_place.note_can_you_enter = 3 
        test_place.note_are_you_safe_enough = 3 
        test_place.note_is_mixed_lockers = 3 
        test_place.note_is_inclusive_lockers = 3
        test_place.note_has_respectful_staff = 3 
        test_place.save()

    def test_show_place(self):
        """Checks if the page is accessible"""
        test_place = Place.objects.get(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_show_wrong_place(self):
        """Checks if a non-existent page is 
        not accessible
        """
        test_place = Place.objects.get(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place.id + 1) + '/')
        self.assertEqual(response.status_code, 404)


class MakeCommentDepartmentTestCase(TestCase):
    """Tests of the make-comment view"""
    def setUp(self):
        test_user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user.save()
        test_user_clone = User.objects.create(username="Kirby54", email="kirby54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user_clone.save()
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place.save()
        test_comment = Comment.objects.create(comment="j'adore", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False, place_id=test_place.id, user_id=test_user.id)
        test_comment.save()
        test_place.note_global = 4 
        test_place.note_can_you_enter = 3 
        test_place.note_are_you_safe_enough = 3 
        test_place.note_is_mixed_lockers = 3 
        test_place.note_is_inclusive_lockers = 3
        test_place.note_has_respectful_staff = 3
        test_place.save()

    def test_make_comment(self):
        """Tests if a logged in user can post a comment"""
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


    def test_make_existing_comment(self):
        """Tests if a logged in user cannot post a comment
        while one already exists
        """
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id +1) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_make_comment_while_not_logged_in(self):
        """Tests if a not logged in user cannot post a comment"""
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


class EditCommentDepartmentTestCase(TestCase):
    """Tests of the edit-comment view"""
    def setUp(self):
        test_user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user.save()
        test_user_clone = User.objects.create(username="Kirby54", email="kirby54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user_clone.save()
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', can_be_seen=True, category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_place.save()
        test_comment = Comment.objects.create(comment="j'adore", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False, place_id=test_place.id, user_id=test_user.id)
        test_comment.save()
        test_place.note_global = 4 
        test_place.note_can_you_enter = 3 
        test_place.note_are_you_safe_enough = 3
        test_place.note_is_mixed_lockers = 3
        test_place.note_is_inclusive_lockers = 3 
        test_place.note_has_respectful_staff = 3 
        test_place.save()

    def test_edit_comment(self):
        """Tests if a logged in user can edit an existing 
        comment
        """
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        test_comment = Comment.objects.get(comment="j'adore", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        print(test_place[0].id)
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


    def test_edit_nonexisting_comment(self):
        """Tests if a logged in user cannot edit a 
        non-existing comment
        """
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id +1) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_edit_comment_while_not_logged_in(self):
        """Tests if a not logged in user cannot edit a comment"""
        # response = self.client.get(reverse('edit_comment', args=[test_place.id]), {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)
