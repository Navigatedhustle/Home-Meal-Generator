import re
from app import app, MEALS

def test_index_ok():
    app.testing=True
    c=app.test_client()
    r=c.get('/')
    assert r.status_code==200
    assert b'Your Inputs' in r.data

def test_db_size():
    assert len(MEALS) >= 450

def test_generate_with_tdee():
    app.testing=True
    c=app.test_client()
    r=c.post('/generate', data={'tdee':'2400','days':'3','meals_per_day':'3','activity':'light'})
    assert r.status_code==200
    assert b'Target:' in r.data
    assert b'Day 1' in r.data
    assert re.search(rb'/pdf/(\d+)', r.data)

def test_generate_from_stats():
    app.testing=True
    c=app.test_client()
    r=c.post('/generate', data={'sex':'male','age':'28','height_cm':'170','weight_kg':'90','activity':'moderate','days':'2','meals_per_day':'4'})
    assert r.status_code==200
    assert b'TDEE:' in r.data

def test_generate_from_imperial_stats():
    app.testing=True
    c=app.test_client()
    r=c.post('/generate', data={'sex':'female','age':'30','height_ft':'5','height_in':'6','weight_lb':'165','activity':'light','days':'2','meals_per_day':'3'})
    assert r.status_code==200
    assert b'TDEE:' in r.data
