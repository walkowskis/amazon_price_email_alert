
# Amazon.pl price alert

The script allows to email notify when the price of the specified item on amazon.pl drops below the set price.
By using GitHub actions, the script can be executed recursively.

## Installation

Install third party packages from `requirements.txt`.



## Usage

In order to execute the script, you need to fulfill the variables:

```bash
  URL
  threshold_price
  sender_email
  receiver_email
  password
  SMTP_server
  port
```
    
## Acknowledgements

 - [patrickloeber](https://github.com/patrickloeber/python-github-action-template)