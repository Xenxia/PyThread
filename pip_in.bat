@echo off


python setup.py bdist_wheel
cd dist
pip install PyThreadUp-1.0.0-py3-none-any.whl --force-reinstall
cd ..