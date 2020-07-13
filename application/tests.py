from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse, reverse_lazy
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
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        self.assertIs(test_adress.street_adress, '20 rue Kirby54')

    def test_place_object(self):
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        self.assertIs(test_place.name, 'Bar à Chicha de Knuckles')

    def test_comment_object(self):
        test_user = User.objects.create(username="Yoshi69", email="petitprincedurai@caramail.com", password="VIVETOTOSS", gender='Femme trans', about_me='J\'aime la vie et le zouk')
        test_postal_code = '83720'
        test_values = GetCityDepartementAndRegion(test_postal_code)
        test_adress = Adress.objects.create(region=test_values[2], departement=test_values[1], postal_code=test_postal_code, city=test_values[0], street_adress='20 rue Kirby54')
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        test_place = Place.objects.create(name='Bar à Chicha de Knuckles', description='Un max de plaisir fruité !', category=test_category, adress=test_adress, website='http://perdu.com' ,picture='https://lvdneng.rosselcdn.net/sites/default/files/dpistyles_v2/ena_16_9_extra_big/2020/03/06/node_721377/45623951/public/2020/03/06/B9722830880Z.1_20200306172512_000%2BG3MFLV4IR.1-0.jpg?itok=eZf4my0Q1583511920')
        test_comment = Comment.objects.create(comment='J\'adore, un plaisir pour les sens !', user=test_user, place=test_place, score_global='P', can_you_enter=False, are_you_safe_enough=False, is_mixed_lockers=True, is_inclusive_lockers=False, has_respectful_staff=False)
        self.assertIs(test_comment.comment, 'J\'adore, un plaisir pour les sens !')


class UtilsTestsCase(TestCase):

	def test_getcitydepartmentandregion(self):
		test_postal_code = '83720'
		self.assertSequenceEqual(GetCityDepartementAndRegion(test_postal_code), ['TRANS EN PROVENCE', 'Var', "Provence-Alpes-Côte d'Azur"])

	def test_getzipcodefromdepartement(self):
		test_zipcode = 'Var'
		self.assertDictEqual(GetZipCodeFromDepartment(test_zipcode), {'postal_code': '83', 'department': 'Var'})

	def test_doeskeyexists_true(self):
		test_key = 'name'
		test_dict = {'age': 16, 'name': 'Miles Prowler', 'job': 'Mecanic'}
		self.assertIs(DoesKeyExists(test_key, test_dict), True)

	def test_doeskeyexists_false(self):
		test_key = 'pseudo'
		test_dict = {'age': 16, 'name': 'Miles Prowler', 'job': 'Mecanic'}
		self.assertIs(DoesKeyExists(test_key, test_dict), False)

	def test_getnote(self):
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
        # redirect_response = self.client.get(reverse('index'))
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
    def setUp(self):
        user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        user.save()

    def test_account_logged_in(self):
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_logged_in(self):
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


# class ModifyAccountTestCase(TestCase):
#     pass


# class ActivateAccountTestCase(TestCase):
#     pass


class SuggestingNewPlaceTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA", gender='Femme trans', is_active=True)
        test_user.save()

    def test_access_page_not_logged_in(self):
        response = self.client.get('/suggesting-new-place/')
        self.assertEqual(response.status_code, 404)

    def test_suggest_new_place(self):
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        # test_comment = Comment.objects.get(comment="très bon", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        response = self.client.get('/suggesting-new-place/', {'name': 'Bar à Chicha de Knuckles', 'picture': 'https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000', 'description': 'Un lieu convivial pour toute la famille !', 'category': test_category.id, 'website': 'perdu.com', 'contact_mail': 'salam@haleykoum.com', 'contact_phone': '0666666666', 'street_adress': '978 route de Draguignan', 'postal_code': '83720', 'comment': 'J\'ai apprécié', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_suggest_new_place_error(self):
        test_category = Category.objects.create(name='Kebabs', icon='https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000')
        # test_comment = Comment.objects.get(comment="très bon", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        response = self.client.get('/suggesting-new-place/', {'name': 'Bar à Chicha de Knuckles', 'picture': 'https://img.huffingtonpost.com/asset/5e690c9c230000841839f17d.jpeg?cache=m6hnJ2la6O&ops=1778_1000', 'description': 'Un lieu convivial pour toute la famille !', 'category': test_category.id, 'website': 'perdu.com', 'contact_mail': 'salam@haleykoum.com', 'contact_phone': '0666666666', 'street_adress': '978 route de Draguignan', 'postal_code': '83720', 'comment': 'J\'ai apprécié', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


    # def test_make_existing_comment(self):
    #     self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
    #     test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
    #     response = self.client.get('/all-places/' + str(test_place[0].id +1) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
    #     self.assertEqual(response.status_code, 302)

    # def test_make_comment_while_not_logged_in(self):
    #     # test_place = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
    #     test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
    #     # response = self.client.get(reverse('edit_comment', args=[test_place.id]), {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
    #     response = self.client.get('/all-places/' + str(test_place[0].id) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
    #     self.assertEqual(response.status_code, 302)





# def suggesting_new_place(request):
#     my_user = request.user
#     template = loader.get_template('application/suggesting-new-place.html')
#     context = {'user': my_user}
#     if request.method == 'POST':
#         form = PlaceSubmissionForm(request.POST)
#         if form.is_valid():
#             try:
#                 """Creating a new adress"""
#                 my_departement_and_region = GetCityDepartementAndRegion(form.data['postal_code'])
#                 new_adress = Adress(postal_code=form.data['postal_code'], street_adress=form.data['street_adress'], departement=my_departement_and_region[1], region=my_departement_and_region[2], city=my_departement_and_region[0]) 
#                 new_adress.save()
#                 """Creating a new place"""
#                 new_place = Place(name=form.data['name'], picture=form.data['picture'], description=form.data['description'], website=form.data['website'], contact_mail=form.data['contact_mail'], contact_phone=form.data['contact_phone'], can_be_seen=False, adress_id=new_adress.id, category_id=form.data['category'])
#                 new_place.save()
#                 """Creating a new comment"""
#                 new_comment = Comment(comment=form.data['comment'], score_global=form.data['score_global'], can_you_enter=DoesKeyExists('can_you_enter', form.data), are_you_safe_enough=DoesKeyExists('are_you_safe_enough', form.data), is_mixed_lockers=DoesKeyExists('is_mixed_lockers', form.data), is_inclusive_lockers=DoesKeyExists('is_inclusive_lockers', form.data), has_respectful_staff=DoesKeyExists('has_respectful_staff', form.data), place_id=new_place.id, user_id=my_user.id)
#                 new_comment.save()

#                 is_added = True
#             except IntegrityError as error:
#                 is_added = False
#             context = {'user': my_user, 'form': form, 'errors': form.errors}
#             messages.success(request, 'Form submission successful')
#             return HttpResponse(template.render(context,request=request))

#         else:
#             print(form.errors)
#     else:
#         form = PlaceSubmissionForm()
#         context = {'user': my_user, 'form': form, 'errors': form.errors}
#         return HttpResponse(template.render(context,request=request))






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
        test_place_1 = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place_2 = get_object_or_404(Place, name='Kebab de Robotnik')
        response = self.client.get(reverse('all_places'))
        self.assertEqual(response.status_code, 200)


class AllDepartmentsTestCase(TestCase):
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
        departments = Place.objects.filter(can_be_seen=True).values('adress__departement').distinct()
        departments_with_zip_code = []
        for department in departments:
            departments_with_zip_code.append(GetZipCodeFromDepartment(list(department.values())[0]))
        response = self.client.get(reverse('all_departments'))
        self.assertEqual(response.status_code, 200)


class PlacesByDepartmentTestCase(TestCase):
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
        test_place_1 = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place_2 = get_object_or_404(Place, name='Kebab de Robotnik')
        response = self.client.get('/all-departments/' + str(83) + '/')
        self.assertEqual(response.status_code, 200)


class ShowPlaceTestCase(TestCase):
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
        test_place.note_global = 4 #GetNote(test_comment.filter(score_global='P').count(), test_comment.filter(score_global='N').count())
        test_place.note_can_you_enter = 3 #GetNote(test_comment.filter(can_you_enter=True).count(), test_comment.filter(can_you_enter =False).count())
        test_place.note_are_you_safe_enough = 3 #GetNote(test_comment.filter(are_you_safe_enough=True).count(), test_comment.filter(are_you_safe_enough =False).count())
        test_place.note_is_mixed_lockers = 3 #GetNote(test_comment.filter(is_mixed_lockers=True).count(), test_comment.filter(is_mixed_lockers =False).count())
        test_place.note_is_inclusive_lockers = 3 #GetNote(test_comment.filter(is_inclusive_lockers=True).count(), test_comment.filter(is_inclusive_lockers =False).count())
        test_place.note_has_respectful_staff = 3 # GetNote(test_comment.filter(has_respectful_staff=True).count(), test_comment.filter(has_respectful_staff =False).count())
        test_place.save()

    def test_show_place(self):
        test_place = Place.objects.get(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_show_wrong_place(self):
        test_place = Place.objects.get(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place.id + 1) + '/')
        self.assertEqual(response.status_code, 404)





class MakeCommentDepartmentTestCase(TestCase):
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
        test_place.note_global = 4 #GetNote(test_comment.filter(score_global='P').count(), test_comment.filter(score_global='N').count())
        test_place.note_can_you_enter = 3 #GetNote(test_comment.filter(can_you_enter=True).count(), test_comment.filter(can_you_enter =False).count())
        test_place.note_are_you_safe_enough = 3 #GetNote(test_comment.filter(are_you_safe_enough=True).count(), test_comment.filter(are_you_safe_enough =False).count())
        test_place.note_is_mixed_lockers = 3 #GetNote(test_comment.filter(is_mixed_lockers=True).count(), test_comment.filter(is_mixed_lockers =False).count())
        test_place.note_is_inclusive_lockers = 3 #GetNote(test_comment.filter(is_inclusive_lockers=True).count(), test_comment.filter(is_inclusive_lockers =False).count())
        test_place.note_has_respectful_staff = 3 # GetNote(test_comment.filter(has_respectful_staff=True).count(), test_comment.filter(has_respectful_staff =False).count())
        test_place.save()

    def test_make_comment(self):
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        # test_comment = Comment.objects.get(comment="très bon", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


    def test_make_existing_comment(self):
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id +1) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_make_comment_while_not_logged_in(self):
        # test_place = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        # response = self.client.get(reverse('edit_comment', args=[test_place.id]), {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/make-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


class EditCommentDepartmentTestCase(TestCase):
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
        test_place.note_global = 4 #GetNote(test_comment.filter(score_global='P').count(), test_comment.filter(score_global='N').count())
        test_place.note_can_you_enter = 3 #GetNote(test_comment.filter(can_you_enter=True).count(), test_comment.filter(can_you_enter =False).count())
        test_place.note_are_you_safe_enough = 3 #GetNote(test_comment.filter(are_you_safe_enough=True).count(), test_comment.filter(are_you_safe_enough =False).count())
        test_place.note_is_mixed_lockers = 3 #GetNote(test_comment.filter(is_mixed_lockers=True).count(), test_comment.filter(is_mixed_lockers =False).count())
        test_place.note_is_inclusive_lockers = 3 #GetNote(test_comment.filter(is_inclusive_lockers=True).count(), test_comment.filter(is_inclusive_lockers =False).count())
        test_place.note_has_respectful_staff = 3 # GetNote(test_comment.filter(has_respectful_staff=True).count(), test_comment.filter(has_respectful_staff =False).count())
        test_place.save()

    def test_edit_comment(self):
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        test_comment = Comment.objects.get(comment="j'adore", score_global='P', can_you_enter=True, are_you_safe_enough=True, is_mixed_lockers=False, is_inclusive_lockers=False, has_respectful_staff=False)
        print(test_place[0].id)
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)


    def test_edit_nonexisting_comment(self):
        self.client.login(username="Kirby54", password="FANDECYRILHANOUNA")
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        response = self.client.get('/all-places/' + str(test_place[0].id +1) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)

    def test_edit_comment_while_not_logged_in(self):
        # test_place = get_object_or_404(Place, name='Bar à Chicha de Knuckles')
        test_place = Place.objects.get_or_create(name='Bar à Chicha de Knuckles')
        # response = self.client.get(reverse('edit_comment', args=[test_place.id]), {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        response = self.client.get('/all-places/' + str(test_place[0].id) + '/edit-comment/', {'comment': 'Bonjour', 'score_global': 'P', 'can_you_enter': False, 'are_you_safe_enough': True, 'is_mixed_lockers': True, 'is_inclusive_lockers': False, 'has_respectful_staff': True})
        self.assertEqual(response.status_code, 302)




# class AlimentTestCase(TestCase):

#     def setUp(self):
#         """Setting up the tests"""
#         user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
#         user.save()
#         aliment = Aliment.objects.create(name="Chou Rouge")
#         aliment.save()

#     def test_aliment_wrong_page(self):
#         """Checks if the page is not accessible when
#         you try to access a non-existing aliment
#         """
#         aliment = Aliment.objects.get(name="Chou Rouge")
#         aliment_id = aliment.id + 1
#         self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
#         response = self.client.get('/aliment/' + str(aliment_id) + '/')
#         self.assertEqual(response.status_code, 404)

#     def test_aliment_page_not_logged_in(self):
#         """Checks if the page is not accessible when
#         users aren't logged in
#         """
#         aliment = Aliment.objects.get(name="Chou Rouge")
#         aliment_id = aliment.id
#         response = self.client.get('/aliment/' + str(aliment_id) + '/')
#         self.assertEqual(response.status_code, 302)

#     def test_aliment_page_logged_in(self):
#         """Checks if the page is accessible when
#         users are logged in
#         """
#         aliment = Aliment.objects.get(name="Chou Rouge")
#         aliment_id = aliment.id
#         self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
#         response = self.client.get('/aliment/' + str(aliment_id) + '/')
#         self.assertEqual(response.status_code, 200)


# class MesProduitsTestCase(TestCase):
#     """Tests of the mesproduits view"""
#     def setUp(self):
#         """Setting up the tests"""
#         user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
#         user.save()

#     def test_mesproduits_page_not_logged_in(self):
#         """Checks if the page is not accessible when
#         users aren't logged in
#         """
#         response = self.client.get(reverse('mesproduits'))
#         self.assertEqual(response.status_code, 302)

#     def test_mesproduits_page_logged_in(self):
#         """Checks if the page is accessible when
#         users are logged in
#         """
#         self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
#         response = self.client.get(reverse('mesproduits'))
#         self.assertEqual(response.status_code, 200)


# class MentionsLegalesTestCase(TestCase):
#     """Tests of the mentionslegales view"""
#     def test_index_page(self):
#         """Checks if the page is accessible"""
#         response = self.client.get(reverse('mentionslegales'))
#         self.assertEqual(response.status_code, 200)


# class ResetPasswordTestCase(TestCase):
#     """Tests for the password reset functionnality"""
#     def test_reset_password_page(self):
#         """Checks if the page is accessible"""
#         response = self.client.get(reverse('password_reset'))
#         self.assertEqual(response.status_code, 200)

#     def test_send_reset_password(self):
#         """Check if an email has been sent"""
#         user = User.objects.create_user(username="Yoshi54", email="g.barboteau@gmail.com", password="FANDECYRILHANOUNA")
#         user.save()
#         response = self.client.post(reverse('password_reset'),{'email':'g.barboteau@gmail.com'})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')


# class AddSubstituteTestCase(TestCase):
#     """Test for the adding substitute functionnality"""
#     def setUp(self):
#         """Set up the tests"""
#         user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
#         user.save()
#         aliment1 = Aliment.objects.create(name="Coca-Cola", category="Soda", nutriscore="e")
#         aliment1.save()
#         aliment2 = Aliment.objects.create(name="Coca Light", category="Soda", nutriscore="d")
#         aliment2.save()

#     def test_add_substitute_not_logged_in(self):
#         """Checks if the page is not accessible when
#         users aren't logged in
#         """
#         aliment = Aliment.objects.get_or_create(name="Coca-Cola", category="Soda", nutriscore="e")
#         response = self.client.get('/add-product/' + str(aliment[0].id) + '/')
#         self.assertEqual(response.status_code, 302)

#     def test_add_substitute_logged_in(self):
#         """Checks if the page is accessible when
#         users are logged in
#         """
#         self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
#         aliment = Aliment.objects.get_or_create(name="Coca Light")
#         response = self.client.get('/add-product/' + str(aliment[0].id) + '/')
#         self.assertEqual(response.status_code, 200)


# class RemoveSubstituteTestCase(TestCase):
#     """Test for the removing substitute functionnality"""
#     def setUp(self):
#         """Set up the tests"""
#         user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
#         user.save()
#         aliment = Aliment.objects.create(name="Coca-Cola", category="Soda", nutriscore="e")
#         aliment.save()
#         substitute = Substitute.objects.create(user_id=user, aliment_id=aliment)
#         substitute.save()

#     def test_add_substitute_not_logged_in(self):
#         """Checks if the page is not accessible when
#         users aren't logged in
#         """
#         my_user = User.objects.get(username="Yoshi54")
#         my_aliment = Aliment.objects.get(name="Coca-Cola")
#         my_substitute = Substitute.objects.get(user_id=my_user, aliment_id=my_aliment)
#         response = self.client.get('/remove-product/' + str(my_substitute.aliment_id_id) + '/')
#         self.assertEqual(response.status_code, 302)

#     def test_add_substitute_logged_in(self):
#         """Checks if the page is accessible when
#         users are logged in
#         """
#         self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
#         my_user = User.objects.get(username="Yoshi54")
#         my_aliment = Aliment.objects.get(name="Coca-Cola")
#         my_substitute = Substitute.objects.get(user_id=my_user, aliment_id=my_aliment)
#         response = self.client.get('/remove-product/' + str(my_substitute.aliment_id_id) + '/')
#         self.assertEqual(response.status_code, 200)


# def account(request):
#     my_user = request.user
#     template = loader.get_template('application/account.html')
#     context = {'user': my_user}
#     return HttpResponse(template.render(context,request=request))