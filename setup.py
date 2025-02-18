#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path
import os

# Read requirements
def read_requirements(filename: str) -> list:
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description
def read_long_description() -> str:
    with open('README.md', encoding='utf-8') as f:
        return f.read()

# Package metadata
PACKAGE_NAME = "security-toolkit"
VERSION = "2.7.4"
AUTHOR = "Security Research Team"
AUTHOR_EMAIL = "security@toolkit.org"
DESCRIPTION = "Comprehensive security toolkit for educational purposes"
LONG_DESCRIPTION = read_long_description()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
URL = "https://github.com/your-repo/security-toolkit"
LICENSE = "MIT"

# Package categories
CATEGORIES = [
    "network",
    "web",
    "forensics",
    "crypto",
    "system"
]

# Package data
package_data = {
    'security_toolkit': [
        'config/*.yml',
        'data/*.json',
        'templates/*.j2',
        'static/*',
        'tools/*'
    ]
}

# Entry points
entry_points = {
    'console_scripts': [
        'security-toolkit=security_toolkit.cli:main',
        'toolkit-scan=security_toolkit.tools.scanner:main',
        'toolkit-web=security_toolkit.tools.web:main',
        'toolkit-crypto=security_toolkit.tools.crypto:main',
    ],
}

# Dependencies by category
deps = {
    'core': read_requirements('requirements.txt'),
    'network': read_requirements('requirements/network.txt'),
    'web': read_requirements('requirements/web.txt'),
    'forensics': read_requirements('requirements/forensics.txt'),
    'crypto': read_requirements('requirements/crypto.txt'),
    'dev': read_requirements('requirements/dev.txt'),
}

# Setup configuration
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data=package_data,
    include_package_data=True,
    entry_points=entry_points,
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=deps['core'],
    extras_require={
        'network': deps['network'],
        'web': deps['web'],
        'forensics': deps['forensics'],
        'crypto': deps['crypto'],
        'dev': deps['dev'],
        'all': [dep for cat in deps.values() for dep in cat],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Education",
        "Topic :: System :: Systems Administration",
    ],
    
    # Project URLs
    project_urls={
        "Documentation": "https://security-toolkit.readthedocs.io/",
        "Source": "https://github.com/your-repo/security-toolkit",
        "Tracker": "https://github.com/your-repo/security-toolkit/issues",
        "Changelog": "https://github.com/your-repo/security-toolkit/blob/main/CHANGELOG.md",
    },
    
    # Keywords
    keywords=[
        "security",
        "penetration-testing",
        "network-security",
        "web-security",
        "cryptography",
        "forensics",
        "education",
        "toolkit",
    ],
) 