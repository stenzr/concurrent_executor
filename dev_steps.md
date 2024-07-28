# Dev Steps

## Use bumpversion:

### To bump the patch version:
```bash
bumpversion patch
```

### To bump the minor version:

```bash
bumpversion minor
```

### To bump the major version:

```bash
bumpversion major
```

## Manual release process

### Bump version 
    - patch
    - minor
    - major

### git push
    - target: origin
    - branch: main

### execute shell scripts

#### upload the release to pypi

```bash
./upload_to_pypi.sh
```

#### manage release on github

```bash
./github_release_manager.sh
```


## Local Configs

```bash
~/.pypirc


[distutils]
index-servers =
    pypi

[pypi]
  username = __token__
  password = <token>

```



