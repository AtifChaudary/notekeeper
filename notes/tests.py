from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note


class NoteCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.initial_note_count = Note.objects.count()

    def test_note_creation(self):
        self.client.login(username='testuser', password='testpassword')

        # Positive scenario: Create a new note
        new_note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        response = self.client.post(reverse('notes', kwargs={'functionality': 'add'}), data=new_note_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the note was created successfully

        # Check if the new note exists in the database
        created_note = Note.objects.filter(title='Test Note', content='This is a test note.').first()
        self.assertIsNotNone(created_note)  # Ensure the note was created

        # Negative scenario: Create a note without a title
        invalid_note_data = {
            'title': '',
            'content': 'This is an invalid note.',
        }
        response = self.client.post(reverse('notes', kwargs={'functionality': 'add'}), data=invalid_note_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the form is not valid

        # Clean up the created notes if they exist
        created_notes = Note.objects.filter(title='Test Note', content='This is a test note.').values_list('id',
                                                                                                          flat=True)
        Note.objects.filter(id__in=created_notes).delete()


class NoteEditingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.note = Note.objects.create(title='Existing Note', content='This is an existing note.', user=self.user)

    def test_note_editing(self):
        self.client.login(username='testuser', password='testpassword')

        # Positive scenario: Edit an existing note
        updated_note_data = {
            'edit_title': 'Updated Note',
            'edit_content': 'This note has been updated.',
        }
        response = self.client.post(reverse('notes', kwargs={'functionality': 'edit-' + str(self.note.id)}),
                                    data=updated_note_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the note was updated successfully
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')  # Ensure the title was updated
        self.assertEqual(self.note.content, 'This note has been updated.')  # Ensure the content was updated

        # Negative scenario: Edit a note with invalid data
        invalid_note_data = {
            'edit_title': '',
            'edit_content': 'This is an invalid note.',
        }
        response = self.client.post(reverse('notes', kwargs={'functionality': 'edit-' + str(self.note.id)}),
                                    data=invalid_note_data, follow=True)
        self.assertEqual(response.status_code, 200)  #
