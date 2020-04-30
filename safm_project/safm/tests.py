import os
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
    fixtures = ['users.json', 'samples.json']

    def setUp(self):
        import json

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
                tone=Sample.Tone.A,
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
            