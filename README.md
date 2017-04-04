# ECS Tasks

## Usage:

### List availabel tasks

```
fab --list
```

### List running containers

```
fab -H hostname1,hostname2 list_packages
```

### List installed packages on a container

```
fab -H hostname1,hostname2 list_packages:<container id>
```

### Output installed packages on all containers to files

```
fab -H hostname1,hostname2 query
```
