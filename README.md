# AML - Service

21.co service to sell calls to an API that connects to a MongoDB database with the information from the [Consolidated list of targets](https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets/consolidated-list-of-targets) from the UK Government

## Config

The aml service needs a config file named config.py with the following settings:
```sh
mongo = dict(
    connection = 'mongodb://[user]:[password]@[host]:[port]/[database]',
)
payment = dict(
    fee = 1000
)
```
## History

March 2016: Initial version

## Credits

Javi Romero

## License

MIT



