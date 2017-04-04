# ECS Tasks

## Usage:

### List available tasks

```
fab --list
```

### List running containers

```
fab -H hostname1,hostname2 list_containers
```

### List installed packages on a container

```
fab -H hostname1,hostname2 list_packages:<container id>
```

### Output installed packages on all containers to files

```
fab -H hostname1,hostname2 query
```

## TODO

* rename `query` task to something more reasonable
* add output path parameter to `query`
