from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="gamest-discord-notification-service",
    description="Send notifications to a discord webhook.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sopoforic/gamest_discord_notification_service',
    author="Tracy Poff",
    author_email="tracy.poff@gmail.com",
    packages=['gamest_plugins.discord_notification_service'],
    install_requires=['gamest', 'requests'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
)
