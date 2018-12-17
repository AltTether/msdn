# msdn
msdn is Mastodon api for python.  
This api is implemented by refering to sixohsix's api "[Twitter](https://github.com/sixohsix/twitter)"  

# Requirements
- Python 3.6

## Installation
1. Cloning this repository
``` {.sourceCode .bash}
$ git clone https://github.com/AltTether/msdn.git
```  

2. Installing by python
``` {.sourceCode .bash}
$ python3 setup.py install
```  

Now, It has only this way to install.  
I would provide other way.  

## Example
``` {.sourceCode .python}
>>> from msdn import Msdn
>>> BASE_URI = 'https://hogetodon.com'
>>> TOKEN = 'MASTODON_ACCESS_TOKEN'
>>> msdn = Msdn(BASE_URI, TOKEN)
>>> response = msdn.accounts.verify_credentials()
>>> response.status_code
200
```
