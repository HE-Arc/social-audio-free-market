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

    
    
    # TODO: Check automatic deductions



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

        for search_query in ['qtipee', '3.0', '130', 'techno']:
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
        for m in ['', 'm', 'M']:
            count = 0
            for sample in self.samples:
                mode = sample['fields']['mode']
                if m == '' or m == mode:
                    count += 1

            url = '/api/ad_search?mode={0}'.format(m)
            response = self.client.get(url)
            jsonResponse = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(jsonResponse), count)
        

    # TODO: tags advanced search test ; depends on AND or OR condition
    
