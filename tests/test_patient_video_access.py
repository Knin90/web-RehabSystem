# tests/test_patient_video_access.py
"""Unit tests for patient video access.

Run with:
    pytest -q
"""
import pytest
from flask import url_for
from app import create_app, db
from app.models import User, Therapist, Patient, SessionCapture, Routine, RoutineExercise, Exercise
import io
import os

def create_user_and_profile(username, password, role='therapist', specialty='General'):
    user = User(nombre_usuario=username, correo_electronico=f'{username}@rehab.com', rol=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    if role == 'therapist':
        profile = Therapist(id_usuario=user.id, nombre_completo=user.nombre_usuario, especialidad=specialty)
    elif role == 'patient':
        profile = Patient(id_usuario=user.id, nombre_completo=user.nombre_usuario)
    db.session.add(profile)
    db.session.commit()
    return user, profile

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "a secret key"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth(app):
    """Fixture for authenticated client."""
    def _auth(username, password):
        test_client = app.test_client() # Create a new client instance
        test_client.post('/login', data={'nombre_usuario': username, 'contrasena': password}, follow_redirects=True)
        return test_client
    return _auth

# --- Test Patient Access to Therapist Videos ---
def test_patient_can_see_permanent_therapist_video(auth, app):
    """Test that a patient can see a permanent video recorded by a therapist."""
    with app.app_context():
        therapist_user, therapist_profile = create_user_and_profile('therapist_test', 'therapist123', role='therapist')
        patient_user, patient_profile = create_user_and_profile('patient_test', 'patient123', role='patient')
        
        # Store IDs immediately after creation
        therapist_id = therapist_profile.id
        patient_id = patient_profile.id

        # Create a dummy routine to link therapist and patient (needed for assigned_patients in get_captures)
        exercise = Exercise(nombre='Test Exercise', descripcion='Desc', categoria='Cat', repeticiones='10')
        db.session.add(exercise)
        db.session.flush()

        routine = Routine(nombre='Test Routine', id_terapeuta=therapist_id, id_paciente=patient_id)
        db.session.add(routine)
        db.session.flush()

        routine_exercise = RoutineExercise(id_rutina=routine.id, id_ejercicio=exercise.id)
        db.session.add(routine_exercise)
        db.session.commit()

    # Log in as the therapist
    therapist_client = auth('therapist_test', 'therapist123')

    # Simulate a permanent video upload by the therapist for the patient
    video_data_permanent = {
        'video': (io.BytesIO(b"permanent video content"), 'permanent_test_therapist.webm'),
        'notes': 'Therapist permanent video for patient.',
        'duration': '10',
        'permanent': 'true',
        'patient_id': patient_id
    }
    response_perm = therapist_client.post('/api/save-video-permanent', data=video_data_permanent, content_type='multipart/form-data')
    assert response_perm.status_code == 200
    json_data_perm = response_perm.get_json()
    assert json_data_perm['success'] is True
    assert 'capture_id' in json_data_perm

    # Simulate a non-permanent video upload by the therapist for the patient
    video_data_non_perm = {
        'video': (io.BytesIO(b"non-permanent video content"), 'non_permanent_test_therapist.webm'),
        'notes': 'Therapist non-permanent video for patient.',
        'duration': '5',
        'permanent': 'false',
        'patient_id': patient_id
    }
    response_non_perm = therapist_client.post('/api/save-video-permanent', data=video_data_non_perm, content_type='multipart/form-data')
    assert response_non_perm.status_code == 200
    json_data_non_perm = response_non_perm.get_json()
    assert json_data_non_perm['success'] is True
    assert 'capture_id' in json_data_non_perm

    # Simulate a video upload by the patient themselves
    patient_client = auth('patient_test', 'patient123')
    with patient_client.session_transaction() as session:
        session['user_id'] = patient_user.id
        session['_fresh'] = True
    response_patient_self = patient_client.post('/api/save-patient-video', data=video_data_patient, content_type='multipart/form-data')
    assert response_patient_self.status_code == 200
    json_data_patient_self = response_patient_self.get_json()
    assert json_data_patient_self['success'] is True
    assert 'capture_id' in json_data_patient_self


    # Get the patient's captures
    response_patient_captures = patient_client.get('/api/get-captures')
    assert response_patient_captures.status_code == 200
    patient_captures_data = response_patient_captures.get_json()
    assert patient_captures_data['success'] is True
    
    # Patient should see their own video and the therapist's permanent video
    assert patient_captures_data['total'] == 2
    capture_ids = {c['id'] for c in patient_captures_data['captures']}
    assert json_data_perm['capture_id'] in capture_ids
    assert json_data_patient_self['capture_id'] in capture_ids
    assert json_data_non_perm['capture_id'] not in capture_ids # Patient should NOT see non-permanent therapist video

    # Clean up files created during the test
    if os.path.exists(json_data_perm['file_path']):
        os.remove(json_data_perm['file_path'])
    if os.path.exists(json_data_non_perm['file_path']):
        os.remove(json_data_non_perm['file_path'])
    # The patient's self-recorded video's path is relative, need to reconstruct absolute path
    # based on the static/uploads/videos structure
    patient_video_relative_path = os.path.join('static', 'uploads', 'videos', json_data_patient_self['filename'])
    patient_video_abs_path = os.path.join(app.root_path, '..', patient_video_relative_path) # Adjust as needed based on actual path
    if os.path.exists(patient_video_abs_path):
        os.remove(patient_video_abs_path)


# --- Test Therapist Filtering ---
def test_therapist_can_filter_by_patient(auth, app):
    """Test that a therapist can filter captures by a specific patient."""
    with app.app_context():
        therapist_user, therapist_profile = create_user_and_profile('therapist_filter_test', 'therapist123', role='therapist')
        patient1_user, patient1_profile = create_user_and_profile('patient1_filter_test', 'patient123', role='patient')
        patient2_user, patient2_profile = create_user_and_profile('patient2_filter_test', 'patient123', role='patient')
        
        # Store IDs immediately after creation
        therapist_id = therapist_profile.id
        patient1_id = patient1_profile.id
        patient2_id = patient2_profile.id

        # Link patients to therapist
        exercise = Exercise(nombre='Filter Exercise', descripcion='Desc', categoria='Cat', repeticiones='10')
        db.session.add(exercise)
        db.session.flush()

        routine1 = Routine(nombre='Routine 1', id_terapeuta=therapist_id, id_paciente=patient1_id)
        routine2 = Routine(nombre='Routine 2', id_terapeuta=therapist_id, id_paciente=patient2_id)
        db.session.add_all([routine1, routine2])
        db.session.flush()

        routine_exercise1 = RoutineExercise(id_rutina=routine1.id, id_ejercicio=exercise.id)
        routine_exercise2 = RoutineExercise(id_rutina=routine2.id, id_ejercicio=exercise.id)
        db.session.add_all([routine_exercise1, routine_exercise2])
        db.session.commit()


    therapist_client = auth('therapist_filter_test', 'therapist123')

    # Therapist uploads video for patient 1
    video_data_p1 = {
        'video': (io.BytesIO(b"video for patient 1"), 'video_p1.webm'),
        'notes': 'Video for patient 1.',
        'duration': '10',
        'permanent': 'true',
        'patient_id': patient1_id
    }
    response_p1 = therapist_client.post('/api/save-video-permanent', data=video_data_p1, content_type='multipart/form-data')
    assert response_p1.status_code == 200
    json_data_p1 = response_p1.get_json()
    assert json_data_p1['success'] is True

    # Therapist uploads video for patient 2
    video_data_p2 = {
        'video': (io.BytesIO(b"video for patient 2"), 'video_p2.webm'),
        'notes': 'Video for patient 2.',
        'duration': '10',
        'permanent': 'true',
        'patient_id': patient2_id
    }
    response_p2 = therapist_client.post('/api/save-video-permanent', data=video_data_p2, content_type='multipart/form-data')
    assert response_p2.status_code == 200
    json_data_p2 = response_p2.get_json()
    assert json_data_p2['success'] is True

    # Get all captures for the therapist (should see both)
    response_all = therapist_client.get('/api/get-captures')
    assert response_all.status_code == 200
    all_captures = response_all.get_json()
    assert all_captures['success'] is True
    assert all_captures['total'] == 2 # Therapist's own videos count as well, potentially.

    # Filter captures for patient 1
    response_filter_p1 = therapist_client.get(f'/api/get-captures?patient_id={patient1_id}')
    assert response_filter_p1.status_code == 200
    filtered_p1 = response_filter_p1.get_json()
    assert filtered_p1['success'] is True
    assert filtered_p1['total'] == 1
    assert filtered_p1['captures'][0]['patient_id'] == patient1_id

    # Filter captures for patient 2
    response_filter_p2 = therapist_client.get(f'/api/get-captures?patient_id={patient2_id}')
    assert response_filter_p2.status_code == 200
    filtered_p2 = response_filter_p2.get_json()
    assert filtered_p2['success'] is True
    assert filtered_p2['total'] == 1
    assert filtered_p2['captures'][0]['patient_id'] == patient2_id

    # Clean up files created
    if os.path.exists(json_data_p1['file_path']):
        os.remove(json_data_p1['file_path'])
    if os.path.exists(json_data_p2['file_path']):
        os.remove(json_data_p2['file_path'])

# --- Test Patient cannot see non-permanent therapist videos ---
def test_patient_cannot_see_non_permanent_therapist_video(auth, app):
    """Test that a patient cannot see a non-permanent video recorded by a therapist."""
    with app.app_context():
        therapist_user, therapist_profile = create_user_and_profile('therapist_non_perm', 'therapist123', role='therapist')
        patient_user, patient_profile = create_user_and_profile('patient_non_perm', 'patient123', role='patient')

        # Store IDs immediately after creation
        therapist_id = therapist_profile.id
        patient_id = patient_profile.id

        # Link patient to therapist
        exercise = Exercise(nombre='Non-Perm Exercise', descripcion='Desc', categoria='Cat', repeticiones='10')
        db.session.add(exercise)
        db.session.flush()

        routine = Routine(nombre='Non-Perm Routine', id_terapeuta=therapist_id, id_paciente=patient_id)
        db.session.add(routine)
        db.session.flush()

        routine_exercise = RoutineExercise(id_rutina=routine.id, id_ejercicio=exercise.id)
        db.session.add(routine_exercise)
        db.session.commit()

    therapist_client = auth('therapist_non_perm', 'therapist123')

    # Simulate a non-permanent video upload by the therapist for the patient
    video_data_non_perm = {
        'video': (io.BytesIO(b"non-permanent content"), 'non_perm_therapist.webm'),
        'notes': 'Therapist non-permanent video for patient.',
        'duration': '5',
        'permanent': 'false',
        'patient_id': patient_id
    }
    response_non_perm = therapist_client.post('/api/save-video-permanent', data=video_data_non_perm, content_type='multipart/form-data')
    assert response_non_perm.status_code == 200
    json_data_non_perm = response_non_perm.get_json()
    assert json_data_non_perm['success'] is True

    # Log in as the patient and get captures
    patient_client = auth('patient_non_perm', 'patient123')
    response_patient_captures = patient_client.get('/api/get-captures')
    assert response_patient_captures.status_code == 200
    patient_captures_data = response_patient_captures.get_json()
    assert patient_captures_data['success'] is True
    
    # Patient should NOT see the non-permanent therapist video
    capture_ids = {c['id'] for c in patient_captures_data['captures']}
    assert json_data_non_perm['capture_id'] not in capture_ids
    assert patient_captures_data['total'] == 0 # Patient hasn't uploaded any videos yet.

    # Clean up file
    if os.path.exists(json_data_non_perm['file_path']):
        os.remove(json_data_non_perm['file_path'])
