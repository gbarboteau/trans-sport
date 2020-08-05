import json, requests, os
from django.conf import settings
from tastypie.resources import ModelResource
from .models import Place

def GetCityDepartementAndRegion(postal_code):
    """Get the city, the department and the region
    linked to a postal code
    """
    city_name = None
    department_name = None
    region_code = None
    region_name = None
    with open("application/data/france.json", encoding="utf-8") as cities_data:
        all_cities = json.load(cities_data)
        # parsed_all_cities = json.dumps(all_cities)
        for city in all_cities:
            if city['Code_postal'] == int(postal_code):
                city_name = city['Nom_commune']
    cities_data.close()
    with open("application/data/departments.json", encoding="utf-8") as departments_data:
        all_departments = json.load(departments_data)
        for department in all_departments:
            if department["code"] == str(postal_code[:2]):
                department_name = department["name"]
                region_code = department["region_code"]
    departments_data.close()
    with open("application/data/regions.json", encoding="utf-8") as region_data:
        all_region = json.load(region_data)
        for region in all_region:
            if region["code"] == str(region_code):
                region_name = region["name"]
    region_data.close()
    my_list = [city_name, department_name, region_name]
    return my_list

def GetZipCodeFromDepartment(my_department):
    """Get the zip code of a department"""
    postal_code = None
    with open("application/data/departments.json", encoding="utf-8") as departments_data:
        all_departments = json.load(departments_data)
        for department in all_departments:
            if department["name"] == my_department:
                postal_code = department["code"]
    departments_data.close()
    new_department = {'postal_code': postal_code, 'department': my_department}
    return(new_department)

def DoesKeyExists(my_key, my_dict):
    """Checks if a key exists in a dictionnary"""
    if my_key in my_dict.keys():
        return True
    else:
        return False

def GetNote(positive_reviews, negative_reviews):
    """Makes a note with all the existing reviews"""
    total_notes = positive_reviews + negative_reviews
    if positive_reviews == 0:
        ratio = 0
    else:
        ratio = positive_reviews / total_notes
    note = ratio * 5
    return round(note, 1) 

def GetCoordinates(street_adress, postal_code):
    """Get the coordinates of a given place"""
    myRequest = requests.get("https://nominatim.openstreetmap.org/search?q=" + street_adress + " " + postal_code + "&format=json") 
    myInfos = myRequest.json()
    latitude = myInfos[0]["lat"]
    longitude = myInfos[0]["lon"]
    return(latitude, longitude)


class PlaceResource(ModelResource):
    class Meta:
        queryset = Place.objects.filter(can_be_seen=True)
        resource_name = 'place'
        excludes = ['can_be_seen']
        allowed_methods = ['get']
