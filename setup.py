from setuptools import setup, find_packages

setup(
    name="diffchecker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "streamlit",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "diffchecker=diffchecker.run:main"
        ]
    },
    description="Side-by-side DataFrame comparison with highlighting, like DiffChecker",
    author="Akash Hake",
    python_requires=">=3.7",
)
