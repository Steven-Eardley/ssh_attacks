from setuptools import setup, find_packages

setup(
    name = 'ssh_attacks',
    version = '0.2',
    packages = find_packages(),
    install_requires = [
        "Flask",
        "Flask-Login",
        "Flask-WTF",
        "GitPython",
        "Markdown",
        "WTForms",
        "Werkzeug",
        "requests",
        "pygeoip",
        "dnspython3",
	    "ipwhois"
    ],
    url = 'http://cottagelabs.com/',
    author = 'Steve Eardley',
    author_email = 'steve@cottagelabs.com',
    description = 'View and log failed ssh login / attack attempts on a Linux server',
    license = 'MIT License',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
