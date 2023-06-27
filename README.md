# xsdata-pydantic-basemodel

[![GitHub](https://img.shields.io/github/license/tlambert03/xsdata-pydantic-basemodel)](https://github.com/tlambert03/xsdata-pydantic-basemodel/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/xsdata-pydantic-basemodel.svg?color=green)](https://pypi.org/project/xsdata-pydantic-basemodel)
[![Python Version](https://img.shields.io/pypi/pyversions/xsdata-pydantic-basemodel.svg?color=green)](https://python.org)
[![CI](https://github.com/tlambert03/xsdata-pydantic-basemodel/actions/workflows/ci.yml/badge.svg)](https://github.com/tlambert03/xsdata-pydantic-basemodel/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/tlambert03/xsdata-pydantic-basemodel/branch/main/graph/badge.svg)](https://codecov.io/gh/tlambert03/xsdata-pydantic-basemodel)

This is an experimental variant of <https://github.com/tefra/xsdata-pydantic> that uses pydantic's BaseModel instead of dataclasses.

## Installation

this isn't on PyPI, until it is decided whether to merge into xsdata-pydantic or not.

Please install from github

```bash
pip install xsdata-pydantic-basemodel[cli]@git+https://github.com/tlambert03/xsdata-pydantic-basemodel.git
```

## Generate Models

```bash
$ # Generate models
$ xsdata http://rss.cnn.com/rss/edition.rss --output pydantic-basemodel
Parsing document edition.rss
Analyzer input: 9 main and 0 inner classes
Analyzer output: 9 main and 0 inner classes
Generating package: init
Generating package: generated.rss
```

outputs:

```python
# generated/rss.py
from pydantic import Field, BaseModel
from typing import List, Optional

class Rss(BaseModel):
    class Meta:
        name = "rss"

    version: Optional[float] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    channel: Optional[Channel] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
```

## XML Parsing

```python
>>> from xsdata_pydantic_basemodel.bindings import XmlParser
>>> from urllib.request import urlopen
>>> from generated.rss import Rss
>>>
>>> parser = XmlParser()
>>> with urlopen("http://rss.cnn.com/rss/edition.rss") as rq:
...     result = parser.parse(rq, Rss)
...
>>> result.channel.item[2].title
"'A total lack of discipline': Clarissa Ward visits abandoned Russian foxholes"

>>> result.channel.item[2].pub_date
'Fri, 08 Apr 2022 22:56:33 GMT'
>>> result.channel.item[2].link
'https://www.cnn.com/videos/world/2022/04/08/ukraine-chernihiv-visit-ward-pkg-tsr-vpx.cnn'
```
