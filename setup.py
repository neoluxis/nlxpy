from setuptools import setup, find_packages

deps = []
cv_deps = ["opencv-python-headless", "numpy", "pillow", "scikit-image"]
misc_deps = []
dl_deps = ["torch", "torchvision", "torchaudio", "tqdm", "numpy", "scikit-learn"]
all_deps = cv_deps + misc_deps + dl_deps
all_deps = list(set(all_deps))  # 去重

test_deps = ["pytest"]

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
    install_requires=deps,
    extras_require={
        "cv": cv_deps,
        "misc": misc_deps,
        "dl": dl_deps,
        "test": test_deps,
        "all": all_deps,
    },
    include_package_data=True,
)
