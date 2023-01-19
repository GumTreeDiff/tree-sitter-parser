# Testing

## Install test dependencies

This project uses `pytest` and `pytest-snapshot` to define and run tests.

You can install these dependencies by running:

```sh
pip install -r tests/requirements.txt
```

Then, make sure `pytest` is installed and in your `$PATH` by running:

```sh
pytest --version
```

Ensure that the command returns some version greater than 7.

## Run the tests

You can execute all tests in the `tests` directory by running:

```sh
pytest tests
```

To execute a specific test file, you can run:

```sh
pytest <file>
```

Further, to execute a specific test function within a particular test file, you can run ...

```
pytest <file>::test_<function_name>
```

## Update the snapshots

We use snapshot testing to ensure the ASTs do not suffer from regressions. When needed, you can regenerate the snapshots using:

```sh
pytest --snapshot-update
```

Ensure that the resulting snapshots make sense before commiting them.
