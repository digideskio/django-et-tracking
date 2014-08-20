TEST_CMD = flake8 --exclude=migrations . && ./runtests.py
test:
	$(TEST_CMD)

tdd:
	watchmedo shell-command --recursive --command='clear; $(TEST_CMD)' --drop
