# Toy Depends
Manage thrid-party libs

### depends.yaml
```yaml
source: source    # source will be downloaded in this directory
build: build      # cmake build directory
install: install  # install directory, include this directory with your cmake

cmake_args:       # common cmake args
  - -DCMAKE_BUILD_TYPE=Release

depends:
  ninja: # ninja is necessary, for build other libs
    git: https://github.com/ninja-build/ninja
    tag: v1.9.0
  json:
    git: https://github.com/swm8023/JsonParser
    cmake_args:
      - -DBOOST_ROOT=F:/Source/boost_1_68_0
      - -DJSON_USE_PARSER_SPIRIT=1
```

### install pyyaml
```sh
pip install pyyaml
```

### build
```sh
python depends.py
```

### clean
```sh
python depends.py clean
```



