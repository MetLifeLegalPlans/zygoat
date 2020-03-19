Deploying a Zygoat Application
==============================

Zygoat leaves the deployment options up to the user, and provides enough flexibility to tolerate most setups built on top of it. The only dependency is that the ``frontend`` application has an environment variable during build time called ``BACKEND_URL`` that points to the backend deployment.


Recommended Deployment Options
------------------------------

We recommend deploying the backend Django application using `Zappa serverless <https://github.com/Miserlou/Zappa>`_, and deploying the frontend NextJS application using `Zeit Now <https://zeit.co/>`_.


Common Setup
------------

The official Zappa documentation recommends using `this guide <https://romandc.com/zappa-django-guide/>`_ to configure your django deployment and attaching a database to it. Make sure that you're allowed to call out to it from the frontend by configuring CORS properly. The Zygoat NextJS configuration will proxy the CSRF token and cookies back and forth between API requests.

Something that is not mentioned in the Zappa documentation is that if you want an outbound internet connection (such as if your Django app consumes a 3rd party API) you have to configure two private subnets in AWS, where the default route points to a NAT Gateway that routes out through one or more public subnets.

A private subnet in AWS is any subnet where the default route in the route table (``0.0.0.0/0``) points to a NAT Gateway, whereas in a public subnet it points to an internet gateway resource. Ensure that the private subnets are the only ones attached to your Lambda function in your Zappa configuration, and that it is in a security group that allows access to the database.
