<div align="center">
<h1>V2Kit: A Lightweight Toolkit for V2Ray Config Manipulation</h1>
<br/>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3"></a>
<a href="https://github.com/sepandhaghighi/v2kit"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/sepandhaghighi/v2kit"></a>
<a href="https://badge.fury.io/py/v2kit"><img src="https://badge.fury.io/py/v2kit.svg" alt="PyPI version"></a>
<a href="https://codecov.io/gh/sepandhaghighi/v2kit"><img src="https://codecov.io/gh/sepandhaghighi/v2kit/graph/badge.svg?token=ytuuYF0NmT"></a>
</div>			
				
## Overview	

<p align="justify">	
V2Kit is a lightweight and extensible Python toolkit for working with V2Ray proxy configurations and subscriptions. It provides a clean API for common operations such as protocol detection, configuration validation, config relabeling, and subscription encoding/decoding. The project is designed with simplicity, predictability, and composability in mind, making it suitable for automation scripts, proxy pipelines, networking tools, and future extensions around V2Ray ecosystem utilities.
</p>

<table>
	<tr>
		<td align="center">PyPI Counter</td>
		<td align="center"><a href="http://pepy.tech/project/v2kit"><img src="http://pepy.tech/badge/v2kit"></a></td>
	</tr>
	<tr>
		<td align="center">Github Stars</td>
		<td align="center"><a href="https://github.com/sepandhaghighi/v2kit"><img src="https://img.shields.io/github/stars/sepandhaghighi/v2kit.svg?style=social&label=Stars"></a></td>
	</tr>
</table>



<table>
	<tr> 
		<td align="center">Branch</td>
		<td align="center">main</td>	
		<td align="center">dev</td>	
	</tr>
	<tr>
		<td align="center">CI</td>
		<td align="center"><img src="https://github.com/sepandhaghighi/v2kit/actions/workflows/test.yml/badge.svg?branch=main"></td>
		<td align="center"><img src="https://github.com/sepandhaghighi/v2kit/actions/workflows/test.yml/badge.svg?branch=dev"></td>
	</tr>
</table>

<table>
    <tr> 
        <td align="center">Code Quality</td>
        <td align="center"><a href="https://app.codacy.com/gh/sepandhaghighi/v2kit/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade"><img src="https://app.codacy.com/project/badge/Grade/c0b30b55e04740b2894fe1aa4eef6589"></a></td>
        <td align="center"><a href="https://www.codefactor.io/repository/github/sepandhaghighi/v2kit"><img src="https://www.codefactor.io/repository/github/sepandhaghighi/v2kit/badge" alt="CodeFactor"></a></td>
    </tr>
</table>

## Installation		

### Source Code
- Download [Version 0.1](https://github.com/sepandhaghighi/v2kit/archive/v0.1.zip) or [Latest Source](https://github.com/sepandhaghighi/v2kit/archive/dev.zip)
- `pip install .`				

### PyPI

- Check [Python Packaging User Guide](https://packaging.python.org/installing/)     
- `pip install v2kit==0.1`						

## Supported Protocols

V2Kit currently supports the following protocols:

| Protocol    | Detection  | Parsing  | Relabeling  | Config Model |
| ----------- | ---------  | -------  | ----------  | ------------ |
| VMESS       | ✅         | ✅       | ✅          | ✅           |
| VLESS       | ✅         | ✅       | ✅          | ✅           |
| Trojan      | ✅         | ✅       | ✅          | ✅           |
| Shadowsocks | ✅         | ✅       | ✅          | ✅           |


## Usage

### URI Utilities

```python
from v2kit import (
    decode_subscription,
    encode_subscription,
    is_vmess,
    parse,
    relabel,
)

uri = "vmess://eyJhZGQiOiIxMjcuMC4wLjEiLCJwcyI6Im9sZCJ9"

new_uri = relabel(uri, "Germany-1")

if is_vmess(new_uri):
    print("VMESS config detected")

config = parse(new_uri)

config.update_label("Germany-2")

subscription = encode_subscription([config])

uris = decode_subscription(subscription)
```

### Configs

```python
from v2kit import VMESSConfig

config = VMESSConfig(
    uuid="550e8400-e29b-41d4-a716-446655440000",
    address="example.com",
    port=443,
    label="Germany-1",
)

uri = config.to_uri()
```

## Issues & Bug Reports			

Just fill an issue and describe it. We'll check it ASAP!

- Please complete the issue template

## Show Your Support
								
<h3>Star This Repo</h3>					

Give a ⭐️ if this project helped you!

<h3>Donate to Our Project</h3>	

<h4>Bitcoin</h4>
1KtNLEEeUbTEK9PdN6Ya3ZAKXaqoKUuxCy
<h4>Ethereum</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Litecoin</h4>
Ldnz5gMcEeV8BAdsyf8FstWDC6uyYR6pgZ
<h4>Doge</h4>
DDUnKpFQbBqLpFVZ9DfuVysBdr249HxVDh
<h4>Tron</h4>
TCZxzPZLcJHr2qR3uPUB1tXB6L3FDSSAx7
<h4>Ripple</h4>
rN7ZuRG7HDGHR5nof8nu5LrsbmSB61V1qq
<h4>Binance Coin</h4>
bnb1zglwcf0ac3d0s2f6ck5kgwvcru4tlctt4p5qef
<h4>Tether</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Dash</h4>
Xd3Yn2qZJ7VE8nbKw2fS98aLxR5M6WUU3s
<h4>Stellar</h4>		
GALPOLPISRHIYHLQER2TLJRGUSZH52RYDK6C3HIU4PSMNAV65Q36EGNL
<h4>Zilliqa</h4>
zil1knmz8zj88cf0exr2ry7nav9elehxfcgqu3c5e5
<h4>Coffeete</h4>
<a href="http://www.coffeete.ir/opensource">
<img src="http://www.coffeete.ir/images/buttons/lemonchiffon.png" style="width:260px;" />
</a>

