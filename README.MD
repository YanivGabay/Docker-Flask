# Experience of Learning Docker and Flask

We have 4 Dockers in our setup:

1. **Docker as a router**
2. **Docker as a Python executer**
3. **Docker as a Java executer**
4. **Docker as a Dart executer**

Each Docker has a Flask server to handle POST and GET requests.

## Flow of the Setup

1. The **router** has an `upload` method that receives a code file.
2. You can keep uploading files.
3. When you execute a **GET** method, the router will send the temporary files saved to the **Python**, **Java**, and **Dart executers** based on the file extension.
4. The **executer** will execute the code and return the output to the router using another **POST** request.
5. Finally, the **router** will return the output to the user.

## How to Run

we have a `docker-compose.yml` file that will run all the Dockers at once.

```bash
docker-compose up --build // if you want detached mode, add -d
```
than you can open another terminal and make a basic test via two curls commands:

```bash
curl -F "file=@TestProgram.java" http://localhost:5000/upload
curl -X GET http://localhost:5000/execute
```

make sure your at the directory of the test file you want to upload.

small warning, the dart image with the python and flask installed is a bit heavy, so it will take some time to build. 
id be happy to hear solutions to improve the build time.

Feel free to ask if you have any further questions!
