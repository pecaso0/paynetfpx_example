# paynetfpx_example
Example of Paynet FPX integration in Django

## There are things to prepare in order for this to work:
- A company needs to create an account with Paynet via their Developer Portal (https://developer.paynet.my/home/)
- Then it needs to create a project within the developer portal
- Then enable the sandbox within the newly created project
- Then the company needs to fill up all the company details
- Within the form, the company needs to submit a public key of its certificate (refer to https://docs.developer.paynet.my/docs/fpx/key-management on how to generate a self-signed certificate with the corresponding private and public keys)
- From the project, get the appropriate API keys and replace the relevant variables in the Django settings.py file
- Run `python manage.py migrate` within the root project file to create an initial sqlitedb when first working with this project
- Run `python manage.py createsuperuser --username sample_user --email sample_user@example.com` to create a first user record for the testing in the database

