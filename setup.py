#!/usr/bin/env python
version = "1.0.0"

install_requires = ["pandas", "numpy", "scipy", "statsmodels"] 

zip_safe = False
scripts = ['scripts/chipseq-greylist.py']

write_version_py()
setup(name="chipseq-greylist",
      version=version,
      author="Rory Kirchner",
      author_email="roryk@alum.mit.edu",
      description="Best-practice pipelines for fully automated high throughput sequencing analysis",
      license="MIT",
      url="https://github.com/roryk/chipesq-greylist",
      zip_safe=zip_safe,
      scripts=scripts,
      install_requires=install_requires,
      include_package_data=True)
