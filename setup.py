from setuptools import setup, find_packages

setup(
    name = 'ssh_attacks',
    version = '0.1',
    packages = find_packages(),
    install_requires = [
        "Flask==0.10.1",
        "Flask-Login==0.2.7",
        "Flask-WTF==0.9.3",
        "GitPython==0.1.7",
        "Markdown==2.3.1",
        "WTForms==1.0.5",
        "Werkzeug==0.9.6",
        "requests",
        "pygeoip",
        "dnspython3",
	"ipwhois"
	#"nltk"
        #"lxml"
    ],
    url = 'http://cottagelabs.com/',
    author = 'Steve Eardley',
    author_email = 'steve@cottagelabs.com',
    description = 'View and log failed ssh login / attack attempts on a Linux server',
    license = 'Copyheart',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Copyheart',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
