# CDB - CSV to DB
This is a project is all about turning a big CSV file to a [postgres](https://www.postgresql.org/) table, it automatically detects the type and generates a schema and create the table for you, all you need to do is ensure there are no duplicate column names and that the column names don't go over the postgres limit of size (31 as I know).

# Environment variables
This code cannot work without having your environment variables setup correctly
```env
POSTGRES_USER=...
POSTGRES_PASSWORD=...
TABLE_NAME=...
```

# Database
If you don't have postgres installed, you can use [docker](https://www.docker.com/)
```bash
docker compose up
```

# Cloning
Since I've used one submodule [plog](https://github.com/Ilyass-Bougati/plog) you'll have to clone this repo recursively
```bash
git clone --recursive git@github.com:Ilyass-Bougati/CDB.git
```

# Usage
running the program after setting things up, is as easy as it could get
```bash
python cdb.py filepath
```