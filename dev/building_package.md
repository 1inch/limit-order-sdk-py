# Creating Package
```sh
pipenv run python -m build
```
## Upload to PyPi
```sh
pipenv run twine upload dist/*
```

## Upload to TestPyPi

```sh
pipenv run twine upload --repository testpypi dist/*
```
### Installing Package from TestPyPI
```sh
pip install --index-url https://test.pypi.org/simple/ limit-order-sdk
```
