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

@pytest.fixture
def question_with_zombie_choices():
    question = Question(title="Zombie Quiz", max_selections=1)
    question.add_choice("Cérebro", True)  
    question.add_choice("Coração", False)
    question.add_choice("Osso", False)
    
    original_set_correct = question.set_correct_choices
    def zombie_set_correct(*args, **kwargs):
        original_set_correct(*args, **kwargs)
        for choice in question.choices:
            choice.is_correct = False 
    question.set_correct_choices = zombie_set_correct
    
    return question

def test_zombie_choices_never_stay_correct(question_with_zombie_choices):
    question = question_with_zombie_choices
    question.set_correct_choices([1])  

    assert not question.choices[0].is_correct  
    assert len(question._correct_choice_ids()) == 0 

@pytest.fixture
def question_with_controlled_ghost_choice():
    question = Question(title="Controlled Ghost Quiz")
    question.add_choice("Valid Choice", True)
    
    original_method = question._choice_by_id
    def wrapped_choice_by_id(choice_id, *args, **kwargs):
        if choice_id == 999: 
            raise Exception("Invalid choice id 999")
        return original_method(choice_id, *args, **kwargs)
    question._choice_by_id = wrapped_choice_by_id
    
    return question

def test_controlled_ghost_choice(question_with_controlled_ghost_choice):
    question = question_with_controlled_ghost_choice
    
    assert question._choice_by_id(1).text == "Valid Choice" 
    with pytest.raises(Exception, match="Invalid choice id 999"):
        question._choice_by_id(999)  