from setuptools import setup

setup(name='elyabot',
      version='0.5',
      description='Telegram bot for crypto analytics',
      url='https://github.com/streamtv85/CoinSneaker',
      author='streamtv85',
      author_email='streamtv85@gmail.com',
      license='MIT',
      packages=['elyabot'],
      install_requires=[
          'emoji',
          'requests',
          'python-telegram-bot',
          'matplotlib',
          'numpy',
          'ccxt',
          'btfxwss', 'arrow', 'bitmex', 'pandas'
      ],
      zip_safe=False)
