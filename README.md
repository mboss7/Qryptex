# Qryptex
Qryptex – Securely encrypt your recovery codes and text into encrypted QR codes.


# CLI APP

```shell 
# Clone repos: 
git clone https://github.com/mboss7/Qryptex.git

# Install dependencies:
pip install -r .\Qryptex\requirements.txt

# Test app: 
cd .\Qryptex\
pytest

# run CLI APP:
python .\Qryptex\src\qryptex\main.py
```

# Python module 

## Installation 
```shell
pip install qryptex
```

## Import and object creation 
```python 
import qryptex 

qtx = qryptex.Qryptex()
```
## Functions 
```python
# Write encrypted QR : 
qtx.write_qr(<your_secret>, <your_password>)  

# Read encrypted QR : 
qtx.read_qr(<your_password>, <your_qr_path>)
```
