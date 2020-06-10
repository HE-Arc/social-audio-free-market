import os
import re
import json
from rest_framework import status
from django.test import TestCase
from django.test import Client
from django.test import tag
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from .models import *

# Create your tests here.

class AuthTest(TestCase):
    '''
    Authentication unit testing
    '''
    def setUp(self):
        self.client = Client()

        self.username = 'test'
        self.email = 'test@safmarket.com'
        self.password = 'foo'

        self.user = User.objects.create(
            username=self.username,
            email=self.email,
        )
        self.user.set_password(self.password)
        self.user.save()

    @tag('login')
    def test_login(self):
        response = self.client.post('/api/login', { 'username': self.username, 'password': self.password })
        self.assertEqual(200, response.status_code)
        
        # Successful login returns an authentication token
        jsonResponse = json.loads(response.content)
        self.assertIn('token', jsonResponse)

        # Wrong credentials
        response = self.client.post('/api/login', { 'username': self.username, 'password': 'password' })
        self.assertEqual(400, response.status_code)

    @tag('logout')
    def test_logout(self):
        response = self.client.post('/api/login', { 'username': self.username, 'password': self.password })
        token = json.loads(response.content)['token']
        
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + token
        }
        response = self.client.post('/api/logout', **headers)
        self.assertEqual(200, response.status_code)

    @tag('registration')
    def test_registration(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': 'foobar@safmarket.com',
            'password': 'bar',
            'password_confirm': 'bar'
        })
        self.assertEqual(201, response.status_code)

        # Successful registration returns an authentication token
        jsonResponse = json.loads(response.content)
        self.assertIn('token', jsonResponse)

    @tag('registration_unique_username')
    def test_registration_unique_username(self):
        response = self.client.post('/api/register', {
            'username': self.username,
            'email': 'foobar@safmarket.com',
            'password': self.password,
            'password_confirm': self.password
        })
        self.assertEqual(400, response.status_code)

    @tag('registration_unique_email')
    def test_registration_unique_email(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': self.email,
            'password': self.password,
            'password_confirm': self.password
        })
        self.assertEqual(400, response.status_code)

    @tag('registration_confirm_password')
    def test_registration_confirm_password(self):
        response = self.client.post('/api/register', {
            'username': 'foo',
            'email': 'foobar@safmarket.com',
            'password': self.password,
            'password_confirm': self.password + self.password
        })
        self.assertEqual(400, response.status_code)


class SampleTest(TestCase):
    '''
    Sample model unit testing
    '''
    fixtures = ['users.json', 'samples.json', 'tags.json']

    def setUp(self):
        # Reads the users fixture file
        with open('./safm/fixtures/users.json') as json_users:
            self.users = json.load(json_users)

        # Reads the samples fixture file
        with open('./safm/fixtures/samples.json') as json_samples:
            self.samples = json.load(json_samples)

    @tag('data_len')
    def test_data_len(self):
        '''
        Makes sure that the fixtures format is correct.
        '''
        users = User.objects.all()
        self.assertEqual(len(users), len(self.users))

        samples = Sample.objects.all()
        self.assertEqual(len(samples), len(self.samples))

    @tag('samples_per_user')
    def test_samples_per_user(self):
        '''
        Checks that the number of samples per user is correct.
        '''
        for user in self.users:
            user_id = user['pk']
            user_samples = Sample.objects.filter(user = user_id)
            
            count = 0
            for sample in self.samples:
                if sample['fields']['user'] == user_id:
                    count += 1

            self.assertEqual(count, len(user_samples))

    @tag('sample_filename')
    def test_sample_filename(self):
        '''
        Checks that the filename of an uploaded sample is correctly converted.
        '''

        for user in User.objects.all():
            # Could generate a random string here
            filename = user.username
            file = SimpleUploadedFile('test.wav', b'This is the file content.')

            sample = Sample(
                user=user,
                name=filename,
                file=file,
                key=Sample.Key.A,
                mode=Sample.Mode.MAJOR
            )
            sample.save()
            
            sample = Sample.objects.get(name=filename)
            expected_filename = 'samples/{0}/{1}.wav'.format(user.username, filename)
            self.assertEqual(sample.file, expected_filename)
            
            # Removes the test file in order to avoid future errors
            file_path = os.path.join(settings.MEDIA_ROOT, expected_filename)
            os.remove(file_path)

    @tag('sample_null_user_delete')
    def test_sample_null_user_delete(self):
        '''
        Checks that the user_id field of a sample equals None (SET_NULL) when the
        associated user is deleted.
        '''
        for user in User.objects.all():
            user.delete()

        for sample in Sample.objects.all():
            self.assertTrue(sample.user == None)


class UploadSampleTest(TestCase):
    '''
    Upload sample unit testing
    '''
    def setUp(self):
        self.client = Client()

        self.username = 'test'
        self.email = 'test@safmarket.com'
        self.password = 'foo'

        self.user = User.objects.create(
            username=self.username,
            email=self.email,
        )
        self.user.set_password(self.password)
        self.user.save()

        self.test_file = './safm/test/Test_Sample.wav'

    @tag('sample_upload_requires_authentication')
    def test_sample_upload_requires_authentication(self):
        '''
        Checks that a user cannot upload a sample if not logged in.
        '''
        # Cannot upload when not logged in
        with open(self.test_file, 'rb') as f:
            unauthorizedResponse = self.client.post('/api/upload_sample', {
                'name': 'Test Sample',
                'file': f
            })
            self.assertEqual(401, unauthorizedResponse.status_code)

    @tag('sample_upload')
    def test_sample_upload(self):
        '''
        Checks that a user can upload a sample if logged in and that
        it creates a new Sample model and returns its ID.
        '''
         # Login
        loginResponse = self.client.post('/api/login', { 'username': self.username, 'password': self.password })
        self.assertEqual(200, loginResponse.status_code)
        token = json.loads(loginResponse.content)['token']
        
        # Can upload when logged in
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + token
        }
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/upload_sample', {
                'name': 'Test Sample',
                'file': f
            }, **headers)
            self.assertEqual(201, response.status_code)

            # Checks that the response contains the newly created Sample model ID
            jsonResponse = json.loads(response.content)
            self.assertIn('id', jsonResponse)

    @tag('sample_upload_properties')
    def test_sample_upload_properties(self):
        '''
        Checks that the sample information entered by the user is
        correctly uploaded and that the automatically deducted properties
        are also correct.
        '''
         # Login
        loginResponse = self.client.post('/api/login', { 'username': self.username, 'password': self.password })
        self.assertEqual(200, loginResponse.status_code)
        token = json.loads(loginResponse.content)['token']
        
        # Can upload when logged in
        sample_id = -1
        sample_name = 'Test Sample'
        sample_tags = 'acid,techno,kick'
        sample_key = 'C'
        sample_mode = 'maj'
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + token
        }
        with open(self.test_file, 'rb') as f:    
            response = self.client.post('/api/upload_sample', {
                'name': sample_name,
                'file': f,
                'key': sample_key,
                'mode': sample_mode,
                'tags': sample_tags
            }, **headers)
            self.assertEqual(201, response.status_code)
            sample_id = json.loads(response.content)['id']

        self.assertTrue(sample_id > 0)
        # Gets the newly created Sample model and checks its properties
        #sample = Sample.objects.get(pk=sample_id)
        sampleJson = self.client.get('/api/sample/{0}'.format(sample_id))
        sample = json.loads(sampleJson.content)
        
        self.assertEqual(sample['user']['username'], self.username)
        self.assertEqual(sample['name'], sample_name)
        self.assertEqual(sample['key'], sample_key)
        self.assertEqual(sample['mode'], sample_mode)
        self.assertEqual(sample['nb_dl_unauthenticated'], 0)
        self.assertEqual(len(sample['tags']), 3)

        # Automatically deducted properties
        self.assertEqual(float(sample['duration']), 7.4)
        self.assertEqual(sample['tempo'], 130)


class UserProfileTest(TestCase):
    '''
    UserProfile model unit testing
    '''
    fixtures = ['users.json']

    def setUp(self):
        import json

        # Reads the users fixture file
        with open('./safm/fixtures/users.json') as json_users:
            self.users = json.load(json_users)

    @tag('user_profile_creation')
    def test_user_profile_creation(self):
        '''
        Checks that the filename of an uploaded profile picture is correctly converted.
        '''
        for user in User.objects.all():
            file = SimpleUploadedFile('test.jpg', b'This is the file content.')

            user_profile = UserProfile(
                user=user,
                description='This is a random description.',
                profile_picture=file,
                email_public=True
            )
            user_profile.save()

            user_profile = UserProfile.objects.get(user=user)
            expected_filename = 'users/{0}/pp.jpg'.format(user.id)
            self.assertEqual(user_profile.profile_picture, expected_filename)

            # Removes the test file in order to avoid future errors
            file_path = os.path.join(settings.MEDIA_ROOT, expected_filename)
            os.remove(file_path)
            

class QuickSearchTest(TestCase):
    '''
    Quick Search unit testing
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

    @tag('quick_search_returns_correct_results_length')
    def test_quick_search_returns_correct_results_length(self):
        '''
        Checks that the quick search returns the correct number of samples.
        '''

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

        for search_query in ['qtipee', '130', 'techno']:
            response = self.client.get('/api/quick?search=' + search_query)
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), results_len_from_fixtures(search_query))

    @tag('quick_search_no_results')
    def test_quick_search_no_results(self):
        '''
        Checks that the quick search returns nothing if the given
        search query matches no sample.
        '''
        response = self.client.get('/api/quick?search=whoistheafterking')
        jsonResponse = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(jsonResponse), 0)


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
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), count)

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
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), count)

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
        jsonResponse = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(jsonResponse), count)

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
        jsonResponse = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(jsonResponse), count)

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
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), count)

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
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), count)
        

    # TODO: tags advanced search test ; depends on AND or OR condition
    
