#.PHONY: cleanup lintproject unittests serve

cleanup:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete

lintproject:
	pylint app/

unittests:
	pytest --cov=app/
	coverage html -d tests_coverage_report --title="Flask-Rest-Api unit test coverage"

serve:
	gunicorn -c gunicorn.py "wsgi:create_app()"