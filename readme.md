#1. Install Python
install python 3.5 or 3.6 64 bit version & Dependancies
https://pip.pypa.io/en/stable/installing/
https://virtualenv.pypa.io/en/stable/installation/

#2. Install Tensorflow
https://www.tensorflow.org/install/pip
In Windows you may have to install: pip install virtualenvwrapper-win

#3. Install Keras

#4. To train a language, you can open the luo.txt file and feed in the english phrases and the language
you want to translate to separated by a tab space.

#5. Run the python files as named in the steps. i.e. 1st step, 2nd step, 3rd step. and the other steps

#6. Train and Export the Model in step 3.

#7. Host/serve the model using Tensorflow-model server, you can follow steps below for Ubuntu
apt-get update
apt-get install tensorflow-model-server
tensorflow_model_server --version



#8. Run the tensorflow model server:
a). save the variables and saved_model.pb in Version 1 folder.
i.e. your folder structure can be exported_luo_model/1/.... This is done to ensure that the tensorflow
model server is able to host and serve the model
tensorflow_model_server --model_base_path=/home/ubuntu/exported_luo_model/ --rest_api_port=9000 --model_name=LanguageClassifier

#9 Install Python Flask and Flask rest
pip install flask
pip install flask-restful

Startup the flask Server:
python api.py

Send POST requests to the api with preferred transations
http://127.0.0.1:5000
data: 'phrase to translate'