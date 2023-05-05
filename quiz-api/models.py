from flask import Flask, request, jsonify


class Question:
    def __init__(self, id, text, title, image, position, possible_answers):
        self.id = id
        self.text = text
        self.title = title
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'title': self.title,
            'image': self.image,
            'position': self.position,
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