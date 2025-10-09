# NCT-TSO-ChallengeDocker
This folder contains the sample docker setup for challenges hosted by the TSO group of the NCT Dresden.
It allows to run python code and pytorch models in a docker container.

Participants can use this docker image to test their code and models before submitting them to the challenge.

The challenge hosts will build a docker image based on the submitted files and evaluate it on the test data.

## Requirements

## Usage
```bash
docker build -t challenge_name:team_name .
```
```bash
docker run \
--rm \
--gpus=all \
--net=none \
-v $(pwd)/src/:/app/code:ro \
-v $(pwd)/data/input/:/app/input:ro \
-v $(pwd)/data/output/:/app/output \
challenge_name:team_name
```

## Submission
Please check the challenge website, as the submission process may differ from challenge to challenge.

In general, you will have to submit a zip file containing this folder.
The minimum required files are:
- the Dockerfile
- the src folder, containing your code