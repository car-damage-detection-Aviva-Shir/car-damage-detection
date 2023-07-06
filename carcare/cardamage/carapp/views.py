from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from carapp.models import PicUpload
from carapp.forms import ImageForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def list(request):
    image_path = ''
    image_path1 = ''

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            newdoc = PicUpload(imagefile = request.FILES['imagefile'])
            newdoc.save()

            return HttpResponseRedirect(reverse('list'))

    else:
        form = ImageForm()

    documents = PicUpload.objects.all()
    for document in documents:
        image_path = document.imagefile.name
        image_path1 = '/'+image_path

        document.delete()

    request.session['image_path'] = image_path
    return render(request, 'list.html',
        {'documents':documents, 'image_path1':image_path1, 'form':form}
    )


#***************************** Car Damage Detection ***************************
#******************************************************************************
#*********************************** Start ************************************

#******************************* Import essentials ****************************
import os
import json

import h5py
import numpy as np
import pickle as pk
from PIL import Image


# keras imports
from keras.models import  load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from keras.models import Model
from keras import backend as K
import tensorflow as tf

#************************* Prepare Image for processing ***********************

def prepare_img_224(img_path):
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


# Loading  valid categories for identifying cars using VGG16
with open('static/cat_counter.pk', 'rb') as f:
    cat_counter = pk.load(f)

# shortlisting top 27 Categories that VGG16 stores for cars (Can be altered for less or more)
cat_list  = [k for k, v in cat_counter.most_common()[:27]]

global graph
graph = tf.get_default_graph()
#******************************************************************************

#******************************************************************************
#~~~~~~~~~~~~~~~ Prapare the flat image~~~~~~~~~~~~~
#******************************************************************************
def prepare_flat(img_224):
    base_model = load_model('static/vgg16.h5')
    model = Model(input=base_model.input, output=base_model.get_layer('fc1').output)
    feature = model.predict(img_224)
    flat = feature.flatten()
    flat = np.expand_dims(flat, axis=0)
    return flat

#******************* Loading Models, Weights and Categories Done **************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~ FIRST Check- CAR OR NOT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

CLASS_INDEX_PATH = 'static/imagenet_class_index.json'

def get_predictions(preds, top=5):

    global CLASS_INDEX
    CLASS_INDEX = json.load(open(CLASS_INDEX_PATH))

    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results

def car_categories_check(img_224):
    first_check = load_model('static/vgg16.h5')
    print ("Validating that this is a picture of your car...")
    out = first_check.predict(img_224)
    top = get_predictions(out, top=5)
    for j in top[0]:
        if j[0:2] in cat_list:
            print ("Car Check Passed!!!")
            print ("\n")
            return True
    return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FIRST check ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~ SECOND CHECK - DAMAGED OR NOT~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

def car_damage_check(img_flat):
    second_check = pk.load(open('static/second_check.pickle', 'rb')) #damaged vs whole - trained model
    print ("Validating that damage exists...")
    train_labels = ['00-damage', '01-whole']
    preds = second_check.predict(img_flat)
    prediction = train_labels[preds[0]]

    if train_labels[preds[0]] == '00-damage':
        print ("Validation complete - proceeding to location and severity determination")
        print ("\n")
        return True
    else:
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SECOND CHECK ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#*******************************************************************************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~ THIRD CHECK - Location and Severity Assesment~~~~~~~~~~~~~
#******************************************************************************

def location_assessment(img_flat):
    print ("Validating the damage area - Front, Rear or Side")
    third_check = pk.load(open("static/third_check.pickle", 'rb'))
    train_labels = ['Front', 'Rear', 'Side']
    preds = third_check.predict(img_flat)
    prediction = train_labels[preds[0]]
    print ("Your Car is damaged at - " + train_labels[preds[0]])
    print ("Location assesment complete")
    print("\n")
    return prediction

def severity_assessment(img_flat):
    print ("Validating the Severity...")
    fourth_check = pk.load(open("static/fourth_check.pickle", 'rb'))
    train_labels = ['Minor', 'Moderate', 'Severe']
    preds = fourth_check.predict(img_flat)
    prediction = train_labels[preds[0]]
    print ("Your Car damage impact is - " + train_labels[preds[0]])
    print ("Severity assesment complete")
    print ("\n")

    return prediction

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ THIRD CHECK ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ENGINE  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

# load models

def engine(request):

    MyCar=request.session['image_path']
    img_path = MyCar

    request.session.pop('image_path', None)
    request.session.modified = True
    with graph.as_default():

        img_224 = prepare_img_224(img_path)
        img_flat = prepare_flat(img_224)
        g1 = car_categories_check(img_224)
        g2 = car_damage_check(img_flat)

        while True:
            try:

                if g1 is False:
                    g1_pic = "Are you sure its a car?Make sure you click a clear picture of your car and resubmit"
                    g2_pic = 'N/A'
                    g3='N/A'
                    g4='N/A'

                    break
                else:
                    g1_pic = "It's a Car"

                if g2 is False:
                    g2_pic = "Car not Damaged"
                    g3='N/A'
                    g4='N/A'

                    break
                else:
                    g2_pic = "Car Damaged."

                    g3 ="The damage was detected on the "+location_assessment(img_flat)+" of the car"
                    g4="The severity of the damage was detected as "+severity_assessment(img_flat)
                    break

            except:
                break



    K.clear_session()

    context={'g1_pic':g1_pic,'g2_pic':g2_pic, 'loc':g3, 'sev':g4}

    results = json.dumps(context)
    return HttpResponse(results, content_type ='application/json')





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ENGINE ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************
