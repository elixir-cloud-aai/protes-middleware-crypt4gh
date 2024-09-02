# Crypt4GH Middleware for proTES
[![license][badge-license]][badge-url-license]
[![chat][badge-chat]][badge-url-chat]

## Synopsis
This proof-of-concept middleware enables the use of [Crypt4GH][crypt4gh] files as inputs for tasks that are 
run in [TES][tes] implementations (e.g., [funnel][funnel], [TESK][tesk]).

## Description
Currently, there are no implementations of TES that natively support the use of files encrypted with Crypt4GH.
This middleware supports the use of Crypt4GH files by prepending the list of executors in a TES request with a
decryption executor. This decryption executor decrypts the contents of any Crypt4GH files and places them in a volume
so that subsequent executors can work on the decrypted contents.

## Implementation Details
### Middleware
The middleware alters the initial TES request such that a decryption executor and a new volume (`/vol/crypt/`)are added 
to the request. Since the decryption executor places all input files in `/vol/crypt/` all input paths in subsequent
executors are altered to `/vol/crypt/{filename}`.

![request-overview][request]

### Decryption
The functionality of the decryption executor lies in [`decrypt.py`][decrypt]. This script moves all input files to a
specified output directory (in this case, `/vol/crypt/`). If a Crypt4GH file is detected and the secret key used to
encrypt it is provided, the executor decrypts the contents of the Crypt4GH file and places it in `/vol/crypt`.
Subsequent executors then refer to the files in `/vol/crypt/`, not their original locations.

![workflow-overview][workflow]

## Important Considerations



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
[decrypt]: https://github.com/elixir-cloud-aai/protes-middleware-crypt4gh/blob/main/README.md
[elixir]: https://elixir-europe.org/
[elixir-cloud-aai]: https://elixir-cloud.dcc.sib.swiss/
[elixir-compute]: https://elixir-europe.org/platforms/compute
[funnel]: https://ohsu-comp-bio.github.io/funnel/
[ga4gh]: https://ga4gh.org/
[license]: LICENSE
[request]: <images/request.png>
[tes]: https://github.com/ga4gh/task-execution-schemas
[tesk]: https://github.com/elixir-cloud-aai/TESK
[workflow]: <images/workflow.png>
