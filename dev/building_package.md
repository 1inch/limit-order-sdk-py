- Create necessery files
pipenv run python -m build

- Upload to testpypi
pipenv run twine upload --repository testpypi dist/*

- Installing package, uploaded previously
pip install --index-url https://test.pypi.org/simple/ limit-order-sdk
