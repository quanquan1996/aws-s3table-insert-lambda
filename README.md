# S3 Tables Insert lambda image use pyiceberg
you only need to change region in code,then you can use it.

git clone https://github.com/quanquan1996/aws-s3table-insert-lambda.git

cd aws-s3table-insert-lambda

aws ecr get-login-password --region {yourRegion} | docker login --username AWS --password-stdin {yourAccountID}.dkr.ecr.{yourRegion}.amazonaws.com

sudo docker buildx build --platform linux/amd64 --provenance=false -t docker-image:{yourImageName} .

sudo docker tag docker-image:{yourImageName} {yourAccountID}.dkr.ecr.{yourRegion}.amazonaws.com/{yourEcrRepoName}:latest

sudo docker push {yourAccountID}.dkr.ecr.{yourRegion}.amazonaws.com/{yourEcrRepoName}:latest   