# Onboard API documentation

Source for the readthedocs page for the Onboard Python API client documentation

If you're trying to develop locally and want to test changes, use `sphinx-build` at terminal to build the local html files so you can see what your changes look like, like so: 

```shell
	$ # assuming you're in the Onboard_API_wrappers_documentation directory

	$ # sphinx-build [sourcedir] [outputdir]

	$ sphinx-build . _build
```

This builds the latest version of the docs in a new directory called `_build`. Then just open whatever html file from the `_build` dir into your fav browser, e.g. `$ open _build/xxxxx.html`

Read the docs here:

https://onboard-api-wrappers-documentation.readthedocs.io/en/latest/

Changes to this repo will not be reflected in docs until you build manually: see https://readthedocs.org/projects/onboard-api-wrappers-documentation/