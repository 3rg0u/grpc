<img src='https://www.koyeb.com/static/images/blog/what-is-grpc/what-is-grpc.jpg'></img>

### Setting up environment

There are 2 options for you guys to setup project's environment, using `Anaconda` or `Python virtual environment`.

#### Anaconda

If you did not install `Conda` on your device, visit [its official website](https://anaconda.org/anaconda/conda) and follow the instruction to install.

Now, you have `Conda` installed on your device, create a new environment. In this project, we're using `python` version `3.10.16`.

```shell
conda create --name grpc python=3.10.16

#activate new env
conda activate grpc
```

Install project's dependency packages:

```shell
#clone repository
git clone https://github.com/3rg0u/grpc.git
cd grpc

#install dependencies
pip install -r requirements.txt
```

All done!

#### Python virtual environment

Instead of using `Anaconda`, you can also use `python venv`, it's available from Python `3.3`.  
Here is the instruction to create a `venv` in Python:

```shell
python -m venv grpc
```

Now, activate new env.

- If you're using Windows, run this command in Command Prompt to activate venv (**assert your current working directory is our repo**, which is **/path/to/grpc**).

```shell
gprc\Scripts\activate
```

- If you're using Linux, run this command (**also assert your cwd is our repo**).

```shell
source grpc/bin/activate
```

Finally, install project's dependency packages.

```shell
pip install -r requirements.txt
```

### Implementation

At this moment, you have installed all the dependencies, let's implement our project.  
Step 1: Server hosting.

- In this project, we simulated a mini system, which just had 3 nodes running on 3 different ports (i.e `[6677, 7766, 6767]`).
- You need to open 3 terminal windows corresponding to each server, and run the following command in all 3 windows:

```shell
python3 crud_server.py
```

In each window, enter the corresponding port: `[6677, 7766, 6767]`, respectively.

Step 2: Client serving.

- To experiment the CRUD functions, run the client's application with this command:

```shell
python3 crud_client.py
```
