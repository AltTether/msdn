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
For example, if you want to use web api of endpoint "/v1/api/accounts/verify_credentials" in mstdn.jp instance,  
you need to prepare access_token in the instance, and using this code.  

``` {.sourceCode .python}
>>> from msdn import Msdn
>>> base_uri = 'https://mstdn.jp'
>>> token = 'MASTODON_YOUR_ACCESS_TOKEN'
>>> msdn = Msdn(base_uri, token)
>>> response = msdn.accounts.verify_credentials()
>>> response.text
{"id":"YOUR_ID","username":"YOUR_USERNAME","acct":"YOUR_ACCT","display_name":"YOUR_DISPLAY_NAME",...}
```  

## License
msdn is licensed under the [MIT](https://github.com/AltTether/msdn/blob/master/LICENSE) license.  
Copyright (c) 2018 AltT
