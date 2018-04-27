# scheduler
---
## Dependency
- Redis
- Google Pubsub
## Features
The dFunc Schedualer is currently scheduling job in a greedy fashion by treading each job and each worker independent and identical. Scheduller publish a job function to a worker via Google Pubsub.
## Usage
This is a iterative function constantly schedual jobs when a job is avaliable. It should be running on server along with mediator component. To run this component please see [setup](https://github.com/dfunc-serverless/setup)
## Future Work
The schedualler is currently using a creedy algorithm scheduling first job to the first worker node it sees. 