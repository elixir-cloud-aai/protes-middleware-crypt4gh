# Crypt4GH Middleware for proTES
[![license][badge-license]][badge-url-license]
[![chat][badge-chat]][badge-url-chat]

## Synopsis
This middleware enables the use of [Crypt4GH][crypt4gh] files as inputs for tasks that are run in [TES][tes]
implementations (e.g., [funnel][funnel], [TESK][tesk]).
## Description

## Installation

## Testing
### Prerequisites
This middleware requires a running instance of [proTES](https://github.com/elixir-cloud-aai/proTES)
(running on localhost:8090 by default).\
\
Download the required dependencies\
`pip install requirements_dev.txt`
### Run Tests
Run tests using pytest\
`pytest tests`

## Contributing

## Code of Conduct

## Versioning

## License

This project is distributed under the [Apache License 2.0][badge-license], a
copy of which is also available in [`LICENSE`][license].

## Contact

The project is maintained by [ELIXIR Cloud & AAI][elixir-cloud-aai], a Driver
Project of the [Global Alliance for Genomics and Health (GA4GH)][ga4gh], under
the umbrella of the [ELIXIR][elixir] [Compute Platform][elixir-compute].

- For filing bug reports, feature requests or other code-related issues, please
  make use of the project's [issue tracker](https://github.com/elixir-cloud-aai/protes-middleware-crypt4gh/issues).

[badge-license]: https://img.shields.io/badge/license-Apache%202.0-blue.svg
[badge-chat]: https://img.shields.io/static/v1?label=chat&message=Slack&color=ff6994
[badge-url-license]: <http://www.apache.org/licenses/LICENSE-2.0>
[badge-url-chat]: https://elixir-cloud.slack.com/archives/C04RLFJNF7U
[crypt4gh]: https://www.ga4gh.org/news_item/crypt4gh-a-secure-method-for-sharing-human-genetic-data/
[elixir]: https://elixir-europe.org/
[elixir-cloud-aai]: https://elixir-cloud.dcc.sib.swiss/
[elixir-compute]: https://elixir-europe.org/platforms/compute
[funnel]: https://ohsu-comp-bio.github.io/funnel/
[ga4gh]: https://ga4gh.org/
[license]: LICENSE
[tes]: https://github.com/ga4gh/task-execution-schemas
[tesk]: https://github.com/elixir-cloud-aai/TESK
