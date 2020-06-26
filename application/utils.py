

FRANCE = {
    '75': ("Paris", "Ile-de-France"),
    '92': ("Hauts-de-Seine", "Ile-de-France"),
    '93': ("Seine-Saint-Denis", "Ile-de-France"),
    '94': ("Val-de-Marne", "Ile-de-France")
    }

def GetDepartementAndRegion(postal_code):
    print(postal_code[:2])
    return FRANCE.get(postal_code[:2])

def DoesKeyExists(my_key, my_dict):
    if my_key in my_dict.keys():
        return True
    else:
        return False

def GetNote(positive_reviews, negative_reviews):
    total_notes = positive_reviews + negative_reviews
    ratio = positive_reviews / total_notes
    note = ratio * 5
    return round(note, 1) 