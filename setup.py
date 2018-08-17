from setuptools import setup

setup(name='elyabot',
      version='0.5',
      description='Telegram bot for ELYA community',
      url='https://github.com/streamtv85/elyabot',
      author='streamtv85',
      author_email='streamtv85@gmail.com',
      license='MIT',
      packages=['elyabot'],
      install_requires=[
          'emoji',
          'requests',
          'python-telegram-bot',
          'numpy',
          'ccxt'
      ],
      zip_safe=False)
