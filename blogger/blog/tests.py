"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from django.contrib.auth.models import User

from models import Post


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='u1')
        self.date = timezone.now()
        self.p = Post.objects.create(author=self.user, date=self.date, 
                    title='Test', content='Sample content!')
    
    def test_post_object(self):
        "Post object should set values correctly"
        self.assertEqual(self.p.author, self.user)
        self.assertEqual(self.p.date, self.date)
        self.assertEqual(self.p.title, 'Test')
        self.assertEqual(self.p.content, 'Sample content!')

    def test_post_unicode(self):
        "Unicode representation should follow correct format"
        self.assertEqual(unicode(self.p), 
            u'"{}", by {}, published on {}'.format(self.p.title, self.p.author, self.p.date.date()))



class TestUrls(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        self.user.post_set.create(title='First Test Post', 
                        date=timezone.now(), content='First test.')
        self.user.post_set.create(title='Second Test Post', 
                        date=timezone.now(), content='Second test.')

    def test_signup_url_logged_in(self):
        "Should redirect to /welcome if the user is logged in"
        response = self.client.get('/signup')
        self.assertRedirects(response, '/welcome')

    def test_signup_url_not_logged_in(self):
        "Should redirect to /welcome if the user is logged in"
        self.client.logout()
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_url_logged_in(self):
        "Should redirect to the welcome page if the user is logged in"
        response = self.client.get('/')
        self.assertRedirects(response, '/welcome')

    def test_login_url_not_logged_in(self):
        "Should return the login page if the user is not logged in"
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        "Should redirect to the login page"
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')

    def test_welcome_url_logged_in(self):
        "Should return the welcome page if the user is logged in"
        response = self.client.get('/welcome')
        self.assertEqual(response.status_code, 200)

    def test_welcome_url_not_logged_in(self):
        "Should redirect to the login page if the user is not logged in"
        self.client.logout()
        response = self.client.get('/welcome')
        self.assertRedirects(response, '/')

    def test_add_new_post_url_logged_in(self):
        "Should return the new post page if the user is logged in"
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)

    def test_add_new_post_url_not_logged_in(self):
        "Should redirect to the login page if the user is not logged in"
        self.client.logout()
        response = self.client.get('/new')
        self.assertRedirects(response, '/')

    def test_view_users_recent_posts_url(self):
        "Should return a users' 10 more recent posts"
        response = self.client.get('/view/recent/10')
        self.assertEqual(response.status_code, 200)


class TestSignupView(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pw1')

    def test_signup_success_if_user_does_not_exist(self):
        "New username exists in the database"
        response = self.client.post('/signup', {'username': 'user2', 'password': 'pw2'})
        self.assertTrue(User.objects.get(username='user2'))

    def test_signup_failure_if_user_already_exists(self):
        "Original user's information should not change"
        response = self.client.post('/signup', {'username': 'user1', 'password': 'pw2'})
        user1 = User.objects.get(username='user1')
        self.assertTrue(user1.password, 'pw1')       

    def test_error_message_on_signup_failure(self):
        "An error message should appear on the page if a user already exists"
        response = self.client.post('/signup', {'username': 'user1', 'password': 'pw2'})
        error = 'That username is already taken.'
        self.assertContains(response, error, status_code=200)     

    def test_redirect_on_signup_success(self):
        "On successful signup, a user should be redirected to the welcome page"
        response = self.client.post('/signup', {'username': 'user2', 'password': 'pw2'})
        self.assertRedirects(response, '/welcome')

    def test_user_is_logged_in_after_signup_success(self):
        "User should be logged in after a successful signup"
        response = self.client.post('/signup', {'username': 'user2', 'password': 'pw2'})
        user_id = User.objects.get(username='user2').pk
        self.assertEqual(self.client.session['_auth_user_id'], user_id)

class TestLoginView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.good_cred = {'username': 'user', 'password': 'password'}
        self.bad_cred = {'username': 'user', 'password': 'badpassword'}

    def test_login_and_signup_buttons_appear(self):
        "Login page contains a button for login and signup"
        response = self.client.get('/')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Signup')

    def test_user_is_logged_in_after_successful_attempt(self):
        "User's id should appear in the session after a successful login"
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post('/', self.good_cred)
        self.assertEqual(self.client.session['_auth_user_id'], self.user.pk)

    def test_redirect_to_welcome_page_after_successful_attempt(self):
        "Successful login should redirect to welcome page"
        response = self.client.post('/', self.good_cred)
        self.assertRedirects(response, '/welcome')

    def test_user_is_not_logged_in_with_bad_credentials(self):
        "User id should not appear in the session id after a bad login"
        response = self.client.post('/', self.bad_cred)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_error_message_appears_with_bad_login_attempt(self):
        "An error message should appear after a bad login attempt"
        error = 'That username or password does not exist'
        response = self.client.post('/', self.bad_cred)
        self.assertContains(response, error)

class TestLogoutView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_user_info_should_not_appear_in_session_after_logout(self):
        response = self.client.get('/logout')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_redirect_to_login_page_after_logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')

class TestWelcomeView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_welcome_message(self):
        "Page should contain a 'Welcome, <username>' message"
        response = self.client.get('/welcome')
        self.assertContains(response, 'Welcome, user!')

    def test_buttons_appear(self):
        "Page should display 'Add a new post', 'View recent posts', and 'Logout' buttons"
        response = self.client.get('/welcome')
        buttons = ['Add a new post', 'View recent posts', 'Logout']
        for button in buttons:
            self.assertContains(response, button)

class TestAddNewPostView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        self.post1 = {'title':'First Test Post', 'content':'First test.'}
        self.error_post = {'title':'I have no content'}

    def test_blank_form_on_get_request(self):
        "A get request should display the two form fields with no errors"
        response = self.client.get('/new')
        self.assertContains(response, 'title')
        self.assertContains(response, 'content')
        self.assertNotContains(response, 'This field is required')

    def test_new_post_created_on_successful_entry(self):
        "A new post should exist in the database after a successful submission"
        response = self.client.post('/new', self.post1)
        self.assertTrue(Post.objects.get(author=self.user.pk))

    def test_redirect_on_successful_post(self):
        "Page should redirect to show the user's post recent posts"
        response = self.client.post('/new', self.post1)
        self.assertRedirects(response, '/view/recent/10')

    def test_error_message_if_field_left_blank(self):
        "An error message should appear if title or content fields are left blank"
        response = self.client.post('/new', self.error_post)
        self.assertContains(response, 'This field is required')


class TestViewRecentPostsView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        for i in range(1, 26):
            title = 'Post {}'.format(i)
            date = timezone.now()
            self.user.post_set.create(title=title, date=date, content='Content')

    def test_request_10_should_show_ten_most_recent_posts(self):
        "Asking for 10 results should show the ten most recent posts"
        response = self.client.get('/view/recent/10')
        for i in range(25, 15, -1):
            self.assertContains(response, 'Post {}'.format(i))

    def test_request_20_should_show_twenty_most_recent_posts(self):
        "Asking for 20 results should show the twenty most recent posts"
        response = self.client.get('/view/recent/20')
        for i in range(25, 5, -1):
            self.assertContains(response, 'Post {}'.format(i))

    def test_request_30_should_show_twenty_five_posts(self):
        "Asking for 30 results should show all twenty-five posts"
        response = self.client.get('/view/recent/30')
        for i in range(25, 0, -1):
            self.assertContains(response, 'Post {}'.format(i))

    def test_more_button_appears_when_posts_less_than_20(self):
        "'View more' button should appear when all posts have not been requested"
        response1 = self.client.get('/view/recent/10')
        self.assertContains(response1, 'View more')
        response2 = self.client.get('/view/recent/20')
        self.assertContains(response2, 'View more')

    def test_more_button_does_not_appear_when_posts_greater_than_20(self):
        "'View more' button should not appear when all posts have been requested"
        response3 = self.client.get('/view/recent/30')
        self.assertNotContains(response3, 'View more')

    def test_posts_ordered_by_date(self):
        "Posts should be reverse-ordered by date"
        response3 = self.client.get('/view/recent/30')
        for i in range(24):
            self.assertTrue(response3.context['posts'][i].date > response3.context['posts'][i + 1].date)


class TestViewOnePostView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        self.post1 = self.user.post_set.create(title='First Test Post', 
                        date=timezone.now(), content='First test.')
        self.post2 = self.user.post_set.create(title='Second Test Post', 
                        date=timezone.now(), content='Second test.')
        self.post3 = self.user.post_set.create(title='Third Test Post', 
                        date=timezone.now(), content='Third test.')

    def test_view_existing_post(self):
        "Page should return the post information"
        response = self.client.get('/view/{}'.format(self.post1.pk))
        self.assertContains(response, 'First Test Post')

    def test_view_post_not_in_existence(self):
        "Attempting to view a post that doesn't exist should return a 404 page"
        response = self.client.get('/view/{}'.format(self.post3.pk + 1))
        self.assertTrue(response.status_code, 404)

    def test_view_sidebar_on_first_post(self):
        "The sidebar should contain a 'next' link but not a 'prev' link"
        response = self.client.get('/view/{}'.format(self.post1.pk))
        self.assertContains(response, 'Next')
        self.assertNotContains(response, 'Prev')

    def test_view_sidebar_on_second_post(self):
        "The sidebar should contain a 'next' and 'prev' link"
        response = self.client.get('/view/{}'.format(self.post2.pk))
        self.assertContains(response, 'Next')
        self.assertContains(response, 'Prev')

    def test_view_sidebar_on_third_post(self):
        "The sidebar should contain a 'prev' link but not a 'next' link"
        response = self.client.get('/view/{}'.format(self.post3.pk))
        self.assertContains(response, 'Prev')
        self.assertNotContains(response, 'Next')