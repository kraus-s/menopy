# MeNoPy - A Menota Parser for Python

This package provides a utility for parsing Menota XML files. [Menota](https://www.menota.org/forside.xhtml) 
stands for Medieval Nordic Text Archive and is a scholarly resource and ongoing project, hosted at the 
University of Bergen. It has its own standard for digital editions based on TEI XML and described in the 
[Menota Handbook](https://www.menota.org/HB3_index.xml).

Menota XML has a number of elements and attributes not found in TEI XML and purpose built for editing
medieval Scandinavian manuscripts. Parsing these by hand can be cumbersome and time consuming. There 
currently is no module for the ingestion of Menota XML in SpaCy or CLTK, which is why I have developed 
this simple parser for Python. It ingests Menota XML and returns an object with properties for different 
editorial features, easily accessible as properties of the class.

# Installation

...

# Usage

Parse an XML document as follows:

```
from menopy.parser import parse

doc = parse("menota_file.xml")
```

This will the parse() function returns an object of the class MeNoDoc, which is 
used to handle menota Editions. Thats it! You can now access the doc and the tokens 
for further use, i.e. in SpaCy, for embedding, and other fun things!


## Classes

### MeNoDoc

This class has the following properties:

```
name: str
ms: str
tokens: list[MenotaToken]
lemmatized: bool
diplomatic: bool
normalized: bool
facsimile: bool
msa: bool
```

name: Name of the text manuscript, taken from the source description in the Menota XML
cf. [Menota Handbook ch. 14 sec. 3](https://www.menota.org/HB3_ch14.xml#sec14.3)
ms: Signature/shelfmark of the manuscript, taken from the source description, cf. above
tokens: a list of objects of the class MenotaToken (cf. below)
lemmatized, diplomatic, normalized, facsimile, msa: Indicates whether the 
corresponding level of annotation/transcription is preset (msa = morpho-syntactic annotation).
This is mainly for information purposes at this point. The information is taken
from the encoding description of the XML file, cf. [Menota Handbook ch. 14 sec. 4](https://www.menota.org/HB3_ch14.xml#sec14.4)
Allows for easy filtering by these attributes when working with a larger 
number of manuscripts.


### Menota Token

Class used to handle the individual tokens. For the purpose of this script, 
anything that is inside a `<w>`-element is considered a token. For the exact 
definition, refer to [Menota Handbook ch. 3 sec. 6](https://www.menota.org/HB3_ch3.xml#sec3.6)
The MenotaToken class maps all the different properties, attributes and elements
a `<w>`-element can have according to the Menota handbook to properties of the class:

```
normalized: str
diplomatic: str
facsimile: str
lemma: str
msa: str
```

They are the same as above, i.e. the different levels of transcription and annotation.
If present, they will each contain the string value found for the respective
property in the XML file at hand. If not present, they are currently filled with
an "N/A" string value. This is not ideal behaviour and will be adressed in the future.


# Feedback, suggestion, contribution

Feedback and suggestions are always welcome! Feel free to get in touch by mail
or create an issue on GitHub. If you want to contribute, get in touch.
