from setuptools import setup, find_packages

# Regen requirements.txt:
# python3 -m pip freeze > requirements.txt

# Install dependencies:
# python3 -m pip install -r requirements.txt -t dependencies
setup(
    name='ps5-stock-checker',
    version='1.0',
    description='Checks for PS5 stock availability',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'twilio',
        'python-dotenv'
    ]
)
