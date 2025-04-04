import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_choice_with_max_length_text():
    question = Question(title='q1')
    max_text = 'a' * 100  
    question.add_choice(max_text)
    assert question.choices[0].text == max_text

def test_add_empty_choice_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('') 

def test_remove_nonexistent_choice_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_select_more_choices_than_allowed():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', True)
    question.add_choice('b', True)
    with pytest.raises(Exception):
        question.select_choices([1, 2])

def test_set_correct_choices_after_creation():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.set_correct_choices([1]) 
    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct

def test_choice_ids_sequential_after_removal():
    question = Question(title='q1')
    question.add_choice('a')  
    question.add_choice('b')  
    question.remove_choice_by_id(1)
    question.add_choice('c')  
    assert question.choices[-1].id == 3

def test_question_points_edge_cases():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101) 

def test_select_no_correct_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    assert question.select_choices([]) == [] 

def test_set_correct_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.set_correct_choices([999]) 

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0