# Reverse_Backdoor
Building a reverse backdoor and a listener 
## Objective
To connect to a target computer remotely. Performing functions like executing system commands, uploading and downloading files to and from the target computer are possible which includes formats such as .txt, .jpeg, .png etc..
## Working 
* Web sockets are used to establish the connnection
* Json module is used to serialise the data
## Features
* The backdoor runs without showing any command prompt
* The backdoor automatically creates a registry entry which allows it establish connection each time the system restarts
* The files are upoaded and downloaded without the loss of any data
* User can navigate between different directories of the target computer
