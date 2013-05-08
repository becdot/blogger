###Blogger!

Blogging platform written with Django.

####Features
- Users can sign-up
- Users can login/logout
- Users can add new posts
- New post input form has validation checks
- Navigation sidebar on single post view that contains links to next and previous posts by the same author
- Recent posts view with custom pagination
- Admin account can add/remove both users and blog posts
- Uses Foundation CSS for styling

####Testing
I used the Django built-in testing framework to test everything, and Django-nose to generate test coverage and ensure that models, views, and urls are all 100% covered.  

To use django-nose:

- `pip install coverage`
- `pip install django-nose`
- `python manage.py test --with-coverage --cover-package=blog`


