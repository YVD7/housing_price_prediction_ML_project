### machine-learning-class-project
machine first project


creating conda environment
```
conda create -p venv python==3.7 -y

```

activate conda envinronment

```
conda activate venv/
```

or 

```
conda activate venv
```

installing requirements
```
pip install -r requirements.txt
```

To add file to git
```
git add .
```

> Note: To ignore file or folder from git  we can write name of file/folder in .gitignore file

To check the git status

```
git status
```
To check all version maintained by git
```
git log
```
To create version/commit all changes by git 
```
git commit -m "message"
```
To send version/changes to github
```
git push origin main
```
To check remote url
```
git remote -v
```
To Set CI/CD pipeline in heroku we need 3 information

1.HEROKU_EMAIL = 
2.HEROKU_APP_KEY = 
3.HEROKU_APP_NAME = 

BUILD DOCKER IMAGE

```
docker build -t <image_name> : <tagname> .
``

> Note : Image name for docker must be lowercase

To list docker image
```
docker images  
```
Run Docker Image
```
docker run -p 5000:5000 -e PORT=5000 <container_id>
```
To check running contianer in docker 
```
docker ps
```
To stop docker container
```
docker stop<container_id>
```

