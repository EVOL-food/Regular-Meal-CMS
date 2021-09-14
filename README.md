# Regular Meal CMS - create your food subscriptions website without any line of code!
#### Fully-featured content management system for a daily food delivery subscription system and ready-to-use restaurant website.
*The project is under development!*   
Stage: ALPHA VERSION 
## Setup
1. Clone the GitHub repo in a separate folder:
`git clone https://github.com/EVOL-food/Regular-Meals-CMS.git`  
2. Go to the main directory of the project:
`cd Regular-Meals-CMS`
3. Create new superuser:
`python manage.py createsuperuser`
4. Create database migrations for the Django apps:
`python manage.py makemigrations`
NOTE: if 
```
python manage.py makemigrations menu
python manage.py makemigrations delivery
python manage.py makemigrations client
```
## Requirements:
##### Project has been written on Python Django.
1. *Global*:  
  1.1. Django  
  1.2. Django REST Framework  

2. *Admin-panel*:  
  2.1. django-baton  
  2.2. django-admin-numeric-filter  
  2.3. django-filter  

3. *Internationalization and localization*:  
  3.1. modeltranslation  

4. *Django ORM Models*:  
  5.1. model_mommy  
  5.2. django-imagekit  

5. *Social authentication*:  
  5.1. djoser  
  5.2. social-auth-app-django  
  5.3. restframework-simplejwt  

6. *Extra*:  
  6.1. unidecode  
  6.2. markdown  
  6.3. coverage  
  6.4. pillow  

## TODOs:
1. Make buttons for switching the language in the admin panel.
2. Connect image hosting API like Imgur or Cloudinary.
3. Make a celery task for the Order model, which will indicate the order status "Completed" after the subscription expires.
4. Make OAuth 2.0 better.
5. Make JWT Authentication better.
6. Meke REST API search for menus by: menu name (strict), names of dishes in the menu (non-strict, that is, contains).
