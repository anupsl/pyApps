import pip

def install(packageList):
    for package in packageList:
        try:
            __import__(package)
        except ImportError:
            print package
            pip.main(['install', package, '--disable-pip-version-check', '--quiet']) 


packageList = ['pytest', 'pytest-html', 'pytest_ordering', 'requests', 'selenium', 'enum', 
				'bson', 'bs4', 'pymongo', 'pyrabbit', 'boto3']


install(packageList)


#	find . -type f -name "*.py" | xargs python -m py_compile