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
You __should not use this middleware in untrusted environments__, as it requires transmission of secret keys and stores
the decrypted contents of Crypt4GH files on disk. This middleware is meant to be used with a [Trusted Execution 
Environment (TEE)][TEE], which allows for the secure transmission and storage of data. Integration with TEEs is a work
in progress.

## Installation
```bash
 pip install poetry
 poetry install
```

## Testing
### Requirements
Tests require a running TES instance and an S3 bucket containing the input files. An instance of [Funnel][funnel] 
and [MinIO][minio] were used in development. `TES_URL` in `tests/tasks/test_tasks.py` can be altered depending on the
TES instance being used.

### Run Tests
Run tests using pytest.
```bash
poetry run pytest tests
```

## Contributing
This project is a community effort and lives off your contributions, be it in the form of bug reports, feature requests,
discussions, ideas, fixes, or other code changes. Please read these [guidelines][guidelines] if you want to contribute. 
And please mind the [code of conduct][code-of-conduct] for all interactions with the community.

## License
This project is distributed under the [Apache License 2.0][badge-license], a
copy of which is also available in [`LICENSE`][license].

## Contact
The project is maintained by [ELIXIR Cloud & AAI][elixir-cloud-aai], a Driver
Project of the [Global Alliance for Genomics and Health (GA4GH)][ga4gh], under
the umbrella of the [ELIXIR][elixir] [Compute Platform][elixir-compute].

- For filing bug reports, feature requests or other code-related issues, please
  make use of the project's [issue tracker](https://github.com/elixir-cloud-aai/protes-middleware-crypt4gh/issues).

[![GA4GH logo](images/logo-ga4gh.png)](https://www.ga4gh.org/)
[![ELIXIR logo](images/logo-elixir.png)](https://www.elixir-europe.org/)
[![ELIXIR Cloud & AAI logo](images/logo-elixir-cloud.png)](https://elixir-europe.github.io/cloud/)

[badge-license]: https://img.shields.io/badge/license-Apache%202.0-blue.svg
[badge-chat]: https://img.shields.io/static/v1?label=chat&message=Slack&color=ff6994
[badge-url-license]: <http://www.apache.org/licenses/LICENSE-2.0>
[badge-url-chat]: https://elixir-cloud.slack.com/archives/C04RLFJNF7U
[code-of-conduct]: https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CODE_OF_CONDUCT.md
[crypt4gh]: https://www.ga4gh.org/news_item/crypt4gh-a-secure-method-for-sharing-human-genetic-data/
[decrypt]: https://github.com/elixir-cloud-aai/protes-middleware-crypt4gh/blob/main/README.md
[elixir]: https://elixir-europe.org/
[elixir-cloud-aai]: https://elixir-cloud.dcc.sib.swiss/
[elixir-compute]: https://elixir-europe.org/platforms/compute
[funnel]: https://ohsu-comp-bio.github.io/funnel/
[ga4gh]: https://ga4gh.org/
[guidelines]: https://elixir-cloud-aai.github.io/guides/guide-contributor/
[license]: LICENSE
[minio]: https://min.io/
[request]: <images/request.png>
[tes]: https://github.com/ga4gh/task-execution-schemas
[tesk]: https://github.com/elixir-cloud-aai/TESK
[TEE]: https://f1000research.com/posters/13-194
[workflow]: <images/workflow.png>
