from setuptools import setup, find_packages

cv_deps = ["opencv-python-headless", "numpy", "pillow", "scikit-image"]
utils_deps = []
test_deps = ["pytest", "pytest-cov", "pytest-mock"]
all_deps = cv_deps + utils_deps

setup(
    name="nlxpy",
    version="0.0.1",
    description="Library Neoluxi",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Neolux Lee",
    author_email="neolux_lee@outlook.com",
    url="https://github.com/neoluxis/nlxpy",
    packages=find_packages(),
    python_requires=">=3.9",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={
        "cv": cv_deps,
        "utils": utils_deps,
        "all": all_deps,
    },
    include_package_data=True,
)
