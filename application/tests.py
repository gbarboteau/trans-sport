from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from .models import User, Category, Adress, Place, Comment
from .utils import GetCityDepartementAndRegion, GetZipCodeFromDepartment, DoesKeyExists, GetNote
from django.core import mail
from django.shortcuts import render, redirect, get_object_or_404


class ModelsTestCase(TestCase):
    """Tests of the models"""
    def test_user_object(self):
        """Test of the aliment model"""
        test_user = User.objects.create(username="Yoshi69", email="petitprincedurai@caramail.com", password="VIVETOTOSS", gender=['Femme'], situation=['Trans', 'Non-binaire'], is_admin=False, is_moderator=False, about_me='J\'aime la vie et le zouk')
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
        test_user = User.objects.create(username="Yoshi69", email="petitprincedurai@caramail.com", password="VIVETOTOSS", gender=['Femme'], situation=['Trans', 'Non-binaire'], is_admin=False, is_moderator=False, about_me='J\'aime la vie et le zouk')
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
        print(test_place_1.name)
        print(test_place_2.name)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
