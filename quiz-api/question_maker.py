import random, requests
import base64
import json
question = {
    'text': None,
    'title': None,
    'image': None,
    'possibleAnswers': []
}

def create_questions(date,number_of_questions):
    questions = []
    for i in range(number_of_questions):
        questions.append(create_geography_question())
    for i in range(number_of_questions):
        questions.append(create_history_question())
    for i in range(number_of_questions):
        questions.append(create_musique_question())
    for question in questions:
        question['date'] = date


def create_geography_question():
    question_types = [
        "guess_capital",
        "guess_flag",
        "find_the_flag",
        "guess_continent"
        "guess_language"
        "guess_currency"
    ]
    question_type = question_types[random.randint(0, len(question_types) - 1)]
    if question_type == "guess_capital":
        return guess_capital()
    if question_type == "guess_flag":
        return guess_flag()
    if question_type == "find_the_flag":
        return find_the_flag()
    if question_type == "guess_continent":
        return guess_continent()
    if question_type == "guess_language":
        return guess_language()
    if question_type == "guess_currency":
        return guess_currency()

def guess_capital():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question_img_url = country['flags']['png']
    question_img_base64 = base64.b64encode(requests.get(question_img_url).content).decode('utf-8')
    question['image'] = question_img_base64
    question['text'] = "Quelle est la capitale du pays nommé : " + country['name']['common'] + " ?"
    question['possibleAnswers'].append({
        'text': country['capital'][0],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['capital'][0] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['capital'][0],
                'isCorrect': False
            })
    return question

def guess_flag():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question_img_url = country['flags']['png']
    question_img_base64 = base64.b64encode(requests.get(question_img_url).content).decode('utf-8')
    question['image'] = question_img_base64
    question['text'] = "Quel est le pays représenté par ce drapeau ?"
    question['possibleAnswers'].append({
        'text': country['name']['common'],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['name']['common'] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['name']['common'],
                'isCorrect': False
            })
    return question

def find_the_flag():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question['text'] = "Quel est le dragpeau du pays : " + country['name']['common'] + " ?"
    question['possibleAnswers'].append({
        'text': country['flag'],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['name']['common'] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['flag'],
                'isCorrect': False
            })
    return question

def guess_continent():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question['text'] = "Quel est le continent du pays : " + country['name']['common'] + " ?"
    question['possibleAnswers'].append({
        'text': country['region'],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['region'] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['region'],
                'isCorrect': False
            })
    return question

def guess_language():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question['text'] = "Quelle est la langue parlée dans le pays : " + country['name']['common'] + " ?"
    question['possibleAnswers'].append({
        'text': country['languages'][0],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['languages'][0] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['languages'][0],
                'isCorrect': False
            })
    return question

def guess_currency():
    country = None
    while country is None:
        try:
            import random, requests
            country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
        except:
            pass
    question['title'] = "Géographie"
    question['text'] = "Quelle est la monnaie du pays : " + country['name']['common'] + " ?"
    question['possibleAnswers'].append({
        'text': country['currencies'][0],
        'isCorrect': True
    })
    # get 3 other random countries
    while len(question['possibleAnswers']) < 4:
        country = None
        while country is None:
            try:
                import random, requests
                country = requests.get('https://restcountries.com/v3.1/all').json()[random.randint(0, 250)]
            except:
                pass
        if country['currencies'][0] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': country['currencies'][0],
                'isCorrect': False
            })
    return question

def create_musique_question():
    # open json file at data/festivals.json
    with open('data/festivals.json') as json_file:
        festivals = json.load(json_file)
    # get random festival
    festival = festivals[random.randint(0, len(festivals) - 1)]
    question['title'] = "Musique"
    question['text'] = "Où se déroule le festival : " + festival['nom_du_festival'] + " ?"
    question['possibleAnswers'].append({
        'text': festival['region_principale_de_deroulement'],
        'isCorrect': True
    })

    # get 3 other random festivals
    while len(question['possibleAnswers']) < 4:
        festival = festivals[random.randint(0, len(festivals) - 1)]
        if festival['region_principale_de_deroulement'] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': festival['region_principale_de_deroulement'],
                'isCorrect': False
            })
    return question


def create_history_question():
    # https://data.culture.gouv.fr/explore/dataset/grands-documents-et-images-de-lhistoire-de-france-conserves-par-les-archives-/files/b500231e23fb4c775421f32072c86132/download/
    # open json file at data/histoire.json

    with open('data/histoire.json') as json_file:
        histoires = json.load(json_file)
    # get random histoire
    histoire = histoires[random.randint(0, len(histoires) - 1)]

    question['title'] = "Histoire"
    question['text'] = "De quand date ce document historique ?" 
    question_image_url = "https://data.culture.gouv.fr/explore/dataset/grands-documents-et-images-de-lhistoire-de-france-conserves-par-les-archives-/files/" + histoire["image"]["id"] + "/download/"
    question_image_base64 = base64.b64encode(requests.get(question_image_url).content).decode('ascii')
    question['image'] = question_image_base64

    question['possibleAnswers'].append({
        'text': histoire['date_du_document'],
        'isCorrect': True
    })

    # get 3 other random histoires
    while len(question['possibleAnswers']) < 4:
        histoire = histoires[random.randint(0, len(histoires) - 1)]
        if histoire['date_du_document'] not in [a['text'] for a in question['possibleAnswers']]:
            question['possibleAnswers'].append({
                'text': histoire['date_du_document'],
                'isCorrect': False
            })
    return question
