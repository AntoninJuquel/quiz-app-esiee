from flask import Flask, request, jsonify


class Question:
    def __init__(self, id, text, title, image, position, possible_answers, date=None):
        self.id = id
        self.text = text
        self.title = title
        self.image = image
        self.position = position
        self.date = date
        self.possible_answers = possible_answers

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'title': self.title,
            'image': self.image,
            'position': self.position,
            'date' : self.date,
            'possibleAnswers': self.possible_answers
        }

class PossibleAnswer:
    def __init__(self, id, text, isCorrect):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'isCorrect': self.isCorrect
        }

class Participation:
    def __init__(self,id,name,points, difficulty):
        self.id = id
        self.name = name
        self.points = points
        self.difficulty = difficulty

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'points': self.points,
            'difficulty': self.difficulty
        }