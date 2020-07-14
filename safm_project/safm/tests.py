import os, re, json, tempfile
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.test import Client
from django.test import tag
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from .models import *

# Test user properties
USERNAME = 'test'
EMAIL = 'test@test.com'
PASSWORD = 'foobar2020'

def _create_test_user():
    '''
    Creates a test user.
    '''
    user = User.objects.create(
        username=USERNAME,
        email=EMAIL
    )
    user.set_password(PASSWORD)
    user.save()

    return user

def _login_user_and_get_token(instance):
    '''
    Logs in the test user and returns its authentication token.
    '''
    response = instance.client.post('/api/login', { 'username': USERNAME, 'password': PASSWORD })
    instance.assertEqual(response.status_code, status.HTTP_200_OK)
    token = json.loads(response.content)['token']

    headers = {
        'HTTP_AUTHORIZATION': 'Token ' + token
    }

    return headers

# Create your tests here.

class AuthTest(TestCase):
    '''
    Authentication unit testing
    '''
    def setUp(self):
        self.client = Client()

        self.user = _create_test_user()

    @tag('login')
    def test_login(self):
        # Login with username
        response = self.client.post('/api/login', { 'username': USERNAME, 'password': PASSWORD })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Successful login returns an authentication token and the username
        json_response = json.loads(response.content)
        self.assertIn('token', json_response)
        self.assertEqual(json_response['username'], USERNAME)

        # Login with email address
        response = self.client.post('/api/login', { 'email': EMAIL, 'password': PASSWORD })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Successful login returns an authentication token and the username
        json_response = json.loads(response.content)
        self.assertIn('token', json_response)
        self.assertEqual(json_response['username'], USERNAME)

        # Wrong credentials
        response = self.client.post('/api/login', { 'username': USERNAME, 'password': 'password' })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('logout')
    def test_logout(self):
        # Login
        headers = _login_user_and_get_token(self)
        response = self.client.post('/api/logout', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Unauthorized route if user is not logged in
        response = self.client.post('/api/logout')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('registration')
    def test_registration(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': 'foobar@safmarket.com',
            'password': PASSWORD,
            'password_confirm': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Successful registration returns an authentication token
        json_response = json.loads(response.content)
        self.assertIn('token', json_response)
        self.assertIn('userid', json_response)
        self.assertIn('username', json_response)

        # User Profile creation at registration
        user_id = json_response['userid']
        user_profile = UserProfile.objects.get(user=user_id)
        self.assertEqual(user_profile.user.id, user_id)
        self.assertEqual(user_profile.description, 'No description provided.')
        self.assertEqual(user_profile.email_public, False)

    @tag('registration_valid_username')
    def test_registration_valid_username(self):
        response = self.client.post('/api/register', {
            'username': 'not valid',
            'email': 'foobar@safmarket.com',
            'password': PASSWORD,
            'password_confirm': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('registration_unique_username')
    def test_registration_unique_username(self):
        response = self.client.post('/api/register', {
            'username': USERNAME,
            'email': 'foobar@safmarket.com',
            'password': PASSWORD,
            'password_confirm': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('registration_unique_email')
    def test_registration_unique_email(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': EMAIL,
            'password': PASSWORD,
            'password_confirm': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('registration_password_min_length')
    def test_registration_password_min_length(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': 'foobar@safmarket.com',
            'password': 'foo',
            'password_confirm': 'foo'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('registration_confirm_password')
    def test_registration_confirm_password(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': 'foobar@safmarket.com',
            'password': PASSWORD,
            'password_confirm': PASSWORD + PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPatchTest(TestCase):
    '''
    User patch unit testing
    '''
    def setUp(self):
        self.client = APIClient()

        self.user = _create_test_user()

        self.other_user = User.objects.create(
            username='Other',
            email='other@user.com'
        )

    @tag('user_patch_requires_authentication')
    def test_user_patch_requires_authentication(self):
        response = self.client.patch('/api/user/{0}'.format(self.user.id))
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Authentication credentials were not provided.')

    @tag('user_patch_unauthorized_user')
    def test_user_patch_unauthorized_user(self):
        # Login
        headers = _login_user_and_get_token(self)
        response = self.client.patch('/api/user/{0}'.format(self.other_user.id), **headers)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'User does not belong to the user.')

    @tag('user_patch_username')
    def test_user_patch_username(self):
        # Login
        headers = _login_user_and_get_token(self)
        new_username = 'Solomun'
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'username': new_username
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).username, new_username)

        # Username must be unique
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'username': self.other_user.username
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('user_patch_email')
    def test_user_patch_email(self):
        # Login
        headers = _login_user_and_get_token(self)
        new_email = 'new@email.com'
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'email': new_email
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).email, new_email)

        # Email must be unique
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'email': self.other_user.email
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('user_patch_password')
    def test_user_patch_password(self):
        # Login
        headers = _login_user_and_get_token(self)

        # Invalid current password
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'password_current': PASSWORD + PASSWORD,
            'password': PASSWORD,
            'password_confirm': PASSWORD
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # New password must be different than current one
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'password_current': PASSWORD,
            'password': PASSWORD,
            'password_confirm': PASSWORD
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Password min length
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'password_current': PASSWORD,
            'password': 'foo',
            'password_confirm': 'foo'
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Password confirmation match
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'password_current': PASSWORD,
            'password': PASSWORD + PASSWORD,
            'password_confirm': PASSWORD
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Patch password
        response = self.client.patch('/api/user/{0}'.format(self.user.id), {
            'password_current': PASSWORD,
            'password': PASSWORD + PASSWORD,
            'password_confirm': PASSWORD + PASSWORD
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SampleTest(TestCase):
    '''
    Sample model unit testing
    '''
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        self.user = _create_test_user()

        self.test_file = './safm/test/Test_Sample.wav'

    @tag('sample_filename')
    def test_sample_filename(self):
        '''
        Checks that the filename of an uploaded sample is correctly converted.
        '''
        filename = self.user.username
        file = SimpleUploadedFile('test.wav', b'This is the file content.')

        sample = Sample(
            user=self.user,
            name=filename,
            file=file,
            key=Sample.Key.A,
            mode=Sample.Mode.MAJOR
        )
        sample.save()
        
        sample = Sample.objects.get(name=filename)
        expected_filename = 'samples/{0}/{1}.wav'.format(self.user.id, filename)
        self.assertEqual(sample.file, expected_filename)

    @tag('sample_null_user_delete')
    def test_sample_null_user_delete(self):
        '''
        Checks that the user_id field of a sample equals None (SET_NULL) when the
        associated user is deleted.
        '''
        name = 'Test'
        file = SimpleUploadedFile('test.wav', b'This is the file content.')
        sample = Sample(
            user=self.user,
            name=name,
            file=file
        )
        sample.save()

        self.user.delete()
        sample = Sample.objects.get(name=name)
        self.assertTrue(sample.user == None)

    @tag('sample_upload_requires_authentication')
    def test_sample_upload_requires_authentication(self):
        '''
        Checks that a user cannot upload a sample if not logged in.
        '''
        # Cannot upload when not logged in
        with open(self.test_file, 'rb') as f:
            response = self.client.post('/api/sample', {
                'name': 'Test Sample',
                'file': f
            })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('sample_upload')
    def test_sample_upload(self):
        '''
        Checks that a user can upload a sample if logged in and that
        it creates a new Sample model and returns its ID.
        '''
        # Login
        headers = _login_user_and_get_token(self)
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'Test Sample',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Checks that the response contains the newly created Sample model ID
        json_response = json.loads(response.content)
        self.assertIn('id', json_response)

    @tag('sample_upload_properties')
    def test_sample_upload_properties(self):
        '''
        Checks that the sample information entered by the user is
        correctly uploaded and that the automatically deducted properties
        are also correct.
        '''
        # Login
        headers = _login_user_and_get_token(self)
        # Can upload when logged in
        sample_id = -1
        sample_name = 'Test Sample'
        sample_description = 'Test description'
        sample_tags = 'acid,techno,kick'
        sample_key = 'C'
        sample_mode = 'maj'
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': sample_name,
                'file': f,
                'description': sample_description,
                'key': sample_key,
                'mode': sample_mode,
                'tags': sample_tags
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']

        self.assertTrue(sample_id > 0)
        # Gets the newly created Sample model and checks its properties
        #sample = Sample.objects.get(pk=sample_id)
        sampleJson = self.client.get('/api/sample/{0}'.format(sample_id))
        sample = json.loads(sampleJson.content)
        
        self.assertEqual(sample['user']['username'], USERNAME)
        self.assertEqual(sample['name'], sample_name)
        self.assertEqual(sample['description'], sample_description)
        self.assertEqual(sample['key'], sample_key)
        self.assertEqual(sample['mode'], sample_mode)
        self.assertEqual(sample['number_downloads'], 0)
        self.assertEqual(len(sample['tags']), 3)

        # Automatically deducted properties
        self.assertEqual(float(sample['duration']), 7.4)
        self.assertEqual(sample['tempo'], 130)

    @tag('sample_upload_fork')
    def test_sample_upload_fork(self):
        '''
        Checks that the Sample forks property (and its inverse) are correct
        when there is a sample fork from at a Sample upload.
        '''
        # Login
        headers = _login_user_and_get_token(self)
        # First Sample
        sample01_id = -1
        sample_name = 'Test Sample Fork #1'
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': sample_name,
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample01_id = json.loads(response.content)['id']
        self.assertTrue(sample01_id > 0)

        # Second Sample
        sample02_id = -1
        sample_name = 'Test Sample Fork #2'
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': sample_name,
                'file': f,
                'forks_from': sample01_id
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample02_id = json.loads(response.content)['id']
        self.assertTrue(sample02_id > 0)

        # Second Sample is from the first one
        response = self.client.get('/api/forks/from/{0}'.format(sample02_id))
        forks_from = json.loads(response.content)
        self.assertEqual(len(forks_from), 1)
        self.assertEqual(forks_from[0]['id'], sample01_id)
        
        # First Sample is to the second one
        response = self.client.get('/api/forks/to/{0}'.format(sample01_id))
        forks_to = json.loads(response.content)
        self.assertEqual(len(forks_to), 1)
        self.assertEqual(forks_to[0]['id'], sample02_id)

    @tag('patch_sample')
    def test_patch_sample(self):
        '''
        Checks wether a Sampel is correctly patched.
        '''
        # Login
        headers = _login_user_and_get_token(self)

        # Creates a Sample
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'Test Sample',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']

        # Patches the Sample
        new_name = 'Patched Sample'
        new_description = 'Test description'
        new_key = 'C'
        new_mode = 'maj'

        api_client = APIClient()
        response = api_client.patch('/api/sample/{0}'.format(sample_id), {
            'name': new_name,
            'description': new_description,
            'key': new_key,
            'mode': new_mode
        }, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sample = Sample.objects.get(pk=sample_id)
        self.assertEqual(sample.user.username, USERNAME)
        self.assertEqual(sample.name, new_name)
        self.assertEqual(sample.description, new_description)
        self.assertEqual(sample.key, new_key)
        self.assertEqual(sample.mode, new_mode)

    @tag('delete_sample')
    def test_delete_sample(self):
        '''
        Checks wether a Sample is correctly deleted.
        '''
        # Login
        headers = _login_user_and_get_token(self)

        # Creates a Sample
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'Test Sample',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']
        
        # Removes the Sample
        response = self.client.delete('/api/sample/{0}'.format(sample_id), **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Sample does not exist anymore
        response = self.client.get('/api/sample/{0}'.format(sample_id))
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response['detail'], 'Sample not found.')

    @tag('sample_patch_delete_requires_authentication')
    def test_sample_patch_delete_requires_authentication(self):
        # Creates a Sample
        sample_name = 'Sample Test'
        Sample.objects.create(
            name=sample_name,
            file=self.test_file
        )
        sample_id = Sample.objects.get(name=sample_name).id

        # Cannot patch Sample if not authenticated
        response = self.client.patch('/api/sample/{0}'.format(sample_id))
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Authentication credentials were not provided.')

        # Cannot delete Sample if not authenticated
        response = self.client.delete('/api/sample/{0}'.format(sample_id))
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Authentication credentials were not provided.')

    @tag('sample_patch_delete_unauthorized_user')
    def test_sample_patch_delete_unauthorized_user(self):
        # Creates another user
        other_user = User.objects.create(
            username='Unauthorized',
            email='not@authorised.com'
        )

        # Creates a Sample which belongs to the other user
        sample_name = 'Sample Test'
        Sample.objects.create(
            name=sample_name,
            file=self.test_file,
            user=other_user
        )
        sample_id = Sample.objects.get(name=sample_name).id

        # Login
        headers = _login_user_and_get_token(self)   

        # Cannot patch Sample if not from user
        response = self.client.patch('/api/sample/{0}'.format(sample_id), **headers)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Sample does not belong to the user.')

        # Cannot delete Sample if not from user
        response = self.client.delete('/api/sample/{0}'.format(sample_id), **headers)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Sample does not belong to the user.')


class DownloadSampleTest(TestCase):
    '''
    Download Sample unit testing
    '''
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        self.user = _create_test_user()

        self.test_file = './safm/test/Test_Sample.wav'

    @tag('download_sample')
    def test_download_sample(self):
         # Login
        headers = _login_user_and_get_token(self)
        # Creates a Sample
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'Download_Count',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']

        response = self.client.get('/api/sample/file/{0}/1'.format(sample_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('audio', response['content-type'])

    @tag('download_sample_count_property')
    def test_download_sample_count_property(self):
        '''
        Checks that the Sample number_downloads property is correct
        based on the number of times it is downloaded.
        '''
        # Login
        headers = _login_user_and_get_token(self)
        # Creates a Sample
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'Download_Count',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']

        count = 5
        for i in range(0, count):
            # Increments the number_downloads property (manual download by a user)
            self.client.get('/api/sample/file/{0}/1'.format(sample_id))

        sample = Sample.objects.get(pk=sample_id)
        self.assertEqual(sample.number_downloads, count)

        for i in range(0, count):
            # Does not increment the number_downloads property (automatic download for a waveform)
            self.client.get('/api/sample/file/{0}/0'.format(sample_id))

        sample = Sample.objects.get(pk=sample_id)
        # number_downloads property still the same
        self.assertEqual(sample.number_downloads, count)

    @tag('download_sample_user_is_authenticated')
    def test_download_sample_user_is_authenticated(self):
        '''
        Checks that the UserSampleDownload model is correctly created when
        an authenticated user downloads a Sample.
        '''
        # Login
        headers = _login_user_and_get_token(self)
        # Creates a Sample
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/sample', {
                'name': 'User_Sample_Downloads',
                'file': f
            }, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sample_id = json.loads(response.content)['id']

        # Does not create a UserSampleDownload model if the user is not authenticated
        self.client.get('/api/sample/file/{0}/1'.format(sample_id))
        user_downloads = UserSampleDownload.objects.all()
        # There is still no UserSampleDownload model
        self.assertEqual(len(user_downloads), 0)

        # Creates a UserSampleDownload model if the user is authenticated when downloading a sample file
        self.client.get('/api/sample/file/{0}/1'.format(sample_id), **headers)
        user_downloads = UserSampleDownload.objects.all()
        self.assertEqual(len(user_downloads), 1)
        

class UserProfileTest(TestCase):
    '''
    UserProfile model unit testing
    '''
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        self.user = _create_test_user()

    @tag('user_profile_creation')
    def test_user_profile_creation(self):
        '''
        Checks that the filename of an uploaded profile picture is correctly converted.
        '''
        file = SimpleUploadedFile('test.jpg', b'This is the file content.')

        user_profile = UserProfile(
            user=self.user,
            description='This is a random description.',
            profile_picture=file,
            email_public=True
        )
        user_profile.save()

        user_profile = UserProfile.objects.get(user=self.user)
        expected_filename = 'users/{0}/pp.jpg'.format(self.user.id)
        self.assertEqual(user_profile.profile_picture, expected_filename)

    @tag('user_profile_patch')
    def test_user_profile_patch(self):
        # Login
        headers = _login_user_and_get_token(self)
        UserProfile.objects.create(user=self.user)

        # Cannot patch UserProfile if user is not authenticated
        response = self.client.patch('/api/user/profile/{0}'.format(self.user.id))
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Authentication credentials were not provided.')

        # Cannot patch UserProfile if not from user
        other_user = User.objects.create(
            username='Unauthorized',
            email='not@authorised.com'
        )
        UserProfile.objects.create(user=other_user)
        response = self.client.patch('/api/user/profile/{0}'.format(other_user.id), **headers)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_response['detail'], 'Profile does not belong to the user.')

        # UserProfile patch
        new_description = 'This is a new profile description.'
        client = APIClient()
        response = client.patch('/api/user/profile/{0}'.format(self.user.id), {
            'description': new_description,
            'email_public': False
        }, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patched_profile = UserProfile.objects.get(pk=self.user.id)
        self.assertEqual(patched_profile.description, new_description)
        self.assertEqual(patched_profile.email_public, False)


class UserSamplesTest(TestCase):
    '''
    User Samples unit testing
    '''
    fixtures = ['users.json', 'samples.json', 'tags.json']

    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        # Reads the users fixture file
        with open('./safm/fixtures/users.json') as json_users:
            self.users = json.load(json_users)

        # Reads the samples fixture file
        with open('./safm/fixtures/samples.json') as json_samples:
            self.samples = json.load(json_samples)

    @tag('user_samples')
    def test_user_samples(self):
        '''
        Checks wether the user/samples route returns the user samples.
        '''
        for user in self.users:
            user_id = user['pk']
            response = self.client.get('/api/user/samples/{0}'.format(user_id))
            user_samples = json.loads(response.content)

            user_samples_names = []
            for user_sample in user_samples:
                user_samples_names.append(user_sample['name'])
            
            for sample in self.samples:
                sample_name = sample['fields']['name']
                self.assertIn(sample_name, user_samples_names)

    @tag('user_samples_count')
    def test_user_samples_count(self):
        '''
        Checks wether the user/samples/count route returns the correct
        number of samples based on the user.
        '''
        for user in self.users:
            user_id = user['pk']
            count = 0

            for sample in self.samples:
                if sample['fields']['user'] == user_id:
                    count += 1

            response = self.client.get('/api/user/samples/count/{0}'.format(user_id))
            samples_count = json.loads(response.content)['count']
            self.assertEqual(samples_count, count)
            

class UserEmailTest(TestCase):
    '''
    User get email unit testing
    '''
    
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        self.user = _create_test_user()

        self.profile = UserProfile.objects.create(user=self.user)

    @tag('get_user_email')
    def test_get_user_email(self):
        # By default, email_public is False
        user_id = self.user.id
        response = self.client.get('/api/user/email/{0}'.format(user_id))
        self.assertEqual(type(response), HttpResponseNotFound)

        # Sets email_public to True
        self.profile.email_public = True
        self.profile.save()
        response = self.client.get('/api/user/email/{0}'.format(user_id))
        json_response = json.loads(response.content)
        self.assertEqual(json_response['email'], self.user.email)

    @tag('get_authenticated_user_email')
    def test_get_authenticated_user_email(self):
        # Login
        headers = _login_user_and_get_token(self)
        response = self.client.get('/api/user/email/{0}'.format(self.user.id), **headers)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['email'], self.user.email)


class QuickSearchTest(TestCase):
    '''
    Quick Search unit testing
    '''
    fixtures = ['users.json', 'samples.json', 'tags.json']

    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        self.client = Client()

        # Reads the users fixture file
        with open('./safm/fixtures/users.json') as json_users:
            self.users = json.load(json_users)

        # Reads the samples fixture file
        with open('./safm/fixtures/samples.json') as json_samples:
            self.samples = json.load(json_samples)

        # Reads the tags fixture file
        with open('./safm/fixtures/tags.json') as json_tags:
            self.tags = json.load(json_tags)

    @tag('quick_search_returns_correct_results_length')
    def test_quick_search_returns_correct_results_length(self):

        def results_len_from_fixtures(search_query):
            '''
            Returns the theorical number of quick search results based
            on the given search_query and the data from the fixtures.
            '''
            count = 0
            # For each sample from the samples fixture
            for sample in self.samples:
                # Gets the username associated to the sample
                for user in self.users:
                    if user['pk'] == sample['fields']['user']:
                        username = user['fields']['username']
                        break
                    
                # Checks wether the search_query is contained in the sample properties
                # Continue avoids duplicated content
                if search_query in username:
                    count += 1
                    continue
                if search_query in sample['fields']['name']:
                    count += 1
                    continue
                if search_query in str(sample['fields']['duration']):
                    count += 1
                    continue
                if search_query in str(sample['fields']['tempo']):
                    count += 1
                    continue
                if search_query in sample['fields']['key']:
                    count += 1
                    continue
                if search_query in sample['fields']['mode']:
                    count += 1
                    continue
                # search_query in the sample tags
                for tag in self.tags:
                    if search_query in tag['fields']['name']:
                        count += 1
                        break

            return count

        for search_query in [USERNAME, '130', 'techno']:
            response = self.client.get('/api/quick?search=' + search_query)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), results_len_from_fixtures(search_query))

    @tag('quick_search_no_results')
    def test_quick_search_no_results(self):
        '''
        Checks that the quick search returns nothing if the given
        search query matches no sample.
        '''
        response = self.client.get('/api/quick?search=whoistheafterking')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 0)


class AdvancedSearchTest(TestCase):
    '''
    Advanced Search unit testing
    '''
    fixtures = ['users.json', 'samples.json', 'tags.json']

    def setUp(self):
        self.client = Client()

        # Reads the users fixture file
        with open('./safm/fixtures/users.json') as json_users:
            self.users = json.load(json_users)

        # Reads the samples fixture file
        with open('./safm/fixtures/samples.json') as json_samples:
            self.samples = json.load(json_samples)

        # Reads the tags fixture file
        with open('./safm/fixtures/tags.json') as json_tags:
            self.tags = json.load(json_tags)

    @tag('advanced_search_name')
    def test_advanced_search_name(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the name property.
        '''
        for n in ['', 'techno', 'acid', 'kick', 'vocal', 'bass']:
            count = 0
            for sample in self.samples:
                name = sample['fields']['name']
                if re.search(n, name, re.IGNORECASE):
                    count += 1
            
            url = '/api/ad_search?name__icontains={0}'.format(n)
            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), count)

    @tag('advanced_search_username')
    def test_advanced_search_username(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the user__username property.
        '''
        for user in self.users:
            username = user['fields']['username']
            count = 0
            for sample in self.samples:
                user__username = User.objects.get(pk=sample['fields']['user']).username
                if user__username == username:
                    count += 1

            url = '/api/ad_search?user__username__icontains={0}'.format(username)
            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), count)

    @tag('advanced_search_duration')
    def test_advanced_search_duration(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the duration property.
        '''
        duration__gte = 3.0
        duration__lte = 5.0

        count = 0
        for sample in self.samples:
            duration = sample['fields']['duration']
            if duration >= duration__gte and duration <= duration__lte:
                count += 1
        
        url = '/api/ad_search?duration__lte={0}&duration__gte={1}'.format(duration__lte, duration__gte)
        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), count)

    @tag('advanced_search_tempo')
    def test_advanced_search_tempo(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the tempo property.
        '''
        tempo__gte = 125
        tempo__lte = 135

        count = 0
        for sample in self.samples:
            tempo = sample['fields']['tempo']
            if tempo >= tempo__gte and tempo <= tempo__lte:
                count += 1
        
        url = '/api/ad_search?tempo__lte={0}&tempo__gte={1}'.format(tempo__lte, tempo__gte)
        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), count)

    @tag('advanced_search_key')
    def test_advanced_search_key(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the key property.
        '''
        keys = [e.value for e in Sample.Key]
        for k in keys:
            count = 0
            for sample in self.samples:
                key = sample['fields']['key']
                if key == k:
                    count += 1

            url = '/api/ad_search?key={0}'.format(k)
            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), count)

    @tag('advanced_search_mode')
    def test_advanced_search_mode(self):
        '''
        Checks that the Advanced Search returns the correct number
        of samples based on the mode property.
        '''
        for m in ['', 'min', 'maj']:
            count = 0
            for sample in self.samples:
                mode = sample['fields']['mode']
                # When no specific mode is selected, the advanced search
                # should return both minor and major samples
                if m == '' or m == mode:
                    count += 1

            url = '/api/ad_search?mode={0}'.format(m)
            response = self.client.get(url)
            json_response = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), count)
        

    # TODO: tags advanced search test ; depends on AND or OR condition
    