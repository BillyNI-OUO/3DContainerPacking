#main.py

from flask import Flask
from flask import request
from flask_cors import CORS
from py3dbp import Packer, Bin, Item
import json
import uuid
import configparser
from flask import send_file
import os
#===========================================================
#Gobal variable
#===========================================================
#RESULT_JSON_INFOS=[]
PALLET_WEIGHT_LIMMIT=450

#============================================================
#Gobal config
#============================================================
app=Flask(__name__)
#cors problem
CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, resources={r"/get_resource/*": {"origins": "*"}})
#upload setting
config=configparser.ConfigParser()
config.read("cgi_config.ini")
app.config['UPLOAD_FOLDER']=config['DEFAULT']['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH']=config['DEFAULT']['MAX_CONTENT_LENGTH']
ALLOWED_EXTENSIONS=set(['xlsx','xls'])
#==================================``===========================
#Function Name: Processsing3DBP
#Description: convert box_info and container info 
#EXAMPLE: HOW STRUCTURE LOOKS LIKE
'''
{
status: 0, 1, 2 //0:success, 1:fail, 2: partial success 3: critical error 
containers:{
	container1:{
	...informations
		fit_box:{	
		}
		unfit_box:{
		}
	},
	container2:{
		fit_box{
			box_infos
		}
		unfit_box:{
		}
	}
}
}
'''
#=============================================================
def Processing3DBP(container_infos, box_infos):
    packer = Packer()
    #0:success, 1:fail, 2:partial sucess 3:critical error

    flag_success=True
    flag_partial_success=False
    

    total_container_types=len(container_infos)
    total_box_types=len(box_infos)


    #pack box_info
    for index, box_info in enumerate(box_infos):
        #if the sameType of box only is one, do nothing and pass it to algorithm
        packer.add_item(Item(box_info['ID'], box_info['name_with_index'], box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight'],box_info['TypeIndex']))
    

    #processing container_info
    for index, container_info in enumerate(container_infos):
        packer.add_bin(Bin(container_info['ID'],
        container_info['name_with_index'],
        container_info['X'],
        container_info['Y'],
        container_info['Z'],
        container_info['Weight_limmit'],
        container_info['TypeIndex']     
             ))
   
    #calculate
    packer.pack()

    containers_array=[]
    statusNumber=-1

    for b in packer.bins:
        #if there if unfitted_item
        if len(b.unfitted_items)!=0:
            flag_success=False
        if len(b.items)!=0:
            flag_partial_success=True
        #result_json_info=json.dumps(b.getResultDictionary(), indent=4)
        containers_array.append(b.getResultDictionary())

    #add statusNumber
    statusNumber=None
    if(flag_success==True):
        #allsuccess
        statusNumber=1
    elif(flag_success==False and flag_partial_success==True):
        #partial success
        statusNumber=3
    else:
        #fail
        statusNumber=2

    #add status of containers
    final_info_dictionary={
        "status":statusNumber,
        "containers":containers_array,
        "total_container_types":total_container_types,
        "total_box_types":total_box_types
        }

    result_json_info=json.dumps(final_info_dictionary, indent=4)
 

        
        #print(b.getResultDictionary())
    print(result_json_info)
    return result_json_info

#============================================================================
#
#
#=============================================================================
def createPackerWithBox(box_infos):
    packer=Packer()
    for index, box_info in enumerate(box_infos):
        #if the sameType of box only is one, do nothing and pass it to algorithm
        if (box_info['Numbers'] ==1):
            packer.add_item(Item(box_info['ID'], box_info['name_with_index'], box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight'], type_index=index))
            return packer
        #else create copy and pass it into algorithm
        else:
            for number_index in range(int(box_info['Numbers'])):
                name_with_index=box_info['TypeName']+"_"+str(+number_index)
                #if the index is 0 new instance keep the original ID
                if (number_index==0):
                    packer.add_item(Item(box_info['ID'], name_with_index, box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight'], type_index=index))
                    return packer
                else:
                    #else it will create new uuidv4 for this instance
                    packer.add_item(Item(str(uuid.uuid4()), name_with_index, box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight'], type_index=index))
                    return packer   


#=============================================================================
#
#
#=============================================================================
def packTheBoxOnPalletAsVirtualContainer(remain_box_infos, pallet_info):
    packer=Packer()
    


#===============================================================================
#FunctinoName: Processing3DBPwithPallet
#Description :Base on Processing3DBP
#==========================================================================
def Processing3DBPWithPallet(container_infos, box_infos, pallet_infos):
    #return the containers with packed information
    containers_array=[]
    pallets_array=[]
    remain_box_infos=[]
    packer = Packer()
    #0~99:success, 100~199:fail, 300~399:partial sucess 200~299:critical error
    #200 can not push all packed pallets into container
    #201 can not push all boxes into pallets
    flag_success=True
    flag_partial_success=False
    

    total_container_types=len(container_infos)
    total_box_types=len(box_infos)
    total_pallet_types=len(pallet_infos)


    #processing box_info
    packer_with_box=createPackerWithBox(box_infos)
    

    #processing container_info

    #Processing pallet info
    #and create a virtual container for packing, virtual container is the space upon on the palleYt
    for container_type_index, container_info in enumerate(container_infos):
        #if the sameType of container number only is one, do nothing and pass it to algorithm
        if (container_info['Numbers'] ==1):
            #if number of pallet is also one 
            if len(pallet_infos)==1:
                pallet_info=pallet_infos[0]
                virtual_container={}
                virtual_container['X']=pallet_info['X']
                virtual_container['Y']=container_info['Y']-pallet_info['Y']
                virtual_container['Z']=pallet_info['Z']
                virtual_container['Weight']=PALLET_WEIGHT_LIMMIT-pallet_info['Weight']
                #eror handling
                if virtual_container['Y']<0 or virtual_container['Weight']<0:
                    print("There is error in container, pallet can't event be packed by contianer.")
                    #set status code as error, and send to broswer
                    final_info_dictionary={"status":200}
                    result_json_info=json.dumps(final_info_dictionary, indent=4)
                    return result_json_info

                packer_with_box.add_bin(Bin(pallet_info['ID'], pallet_info['TypeName'], virtual_container['X'], virtual_container['Y'], virtual_container['Z'], virtual_container['Weight'], type_index=1))
                packer_with_box.pack()
                #pack the one pallet once 
                b=packer_with_box.bins[0]
                pallets_array.append(b.getResultDictionary())
            #one container with multiple pallet
            else:
                for pallet_type_index, pallet_info in enumerate(pallet_infos):
                    virtual_container={}
                    virtual_container['X']=pallet_info['X']
                    virtual_container['Y']=container_info['Y']-pallet_info['Y']
                    virtual_container['Z']=pallet_info['Z']
                    #eror handling
                    if virtual_container['Y']<0 or virtual_container['Weight']<0:
                        print("There is error in container, pallet can't event be packed by contianer.")
                        #set status code as error, and send to broswer
                        final_info_dictionary={"status":200}
                        result_json_info=json.dumps(final_info_dictionary, indent=4)
                        return result_json_info
                    packer_with_box.add_bin(Bin(pallet_info['ID'], pallet_info['TypeName'], virtual_container['X'], virtual_container['Y'], virtual_container['Z'], virtual_container['Weight'], type_index=pallet_type_index))
                    packer_with_box.pack()
                    b=packer_with_box.bins[0]

                    
                

        #else multiple numbers of containers condition, create copy and pass it into algorithm
        else:
            for number_index in  container_info['Numbers']:
                name_with_index=container_info['TypeName']+"_"+number_index
                #if the index is 0 new instance keep the original ID
                if (number_index==0):
                    packer.add_bin(Bin(container_info['ID'], name_with_index, container_info['X'], container_info['Y'], container_info['Z'], container_info['Weight_limmit'], type_index=container_type_index))
                else:
                    #else it will create new uuidv4 for this instance
                    packer.add_bin(Bin(str(uuid.uuid4()), name_with_index, container_info['X'], container_info['Y'], container_info['Z'], container_info['Weight_limmit'], type_index=container_type_index))    
    #calculate
    packer.pack()

    containers_array=[]
    statusNumber=-1

    for b in packer.bins:
        #if there if unfitted_item
        if len(b.unfitted_items)!=0:
            flag_success=False
        if len(b.items)!=0:
            flag_partial_success=True
        #result_json_info=json.dumps(b.getResultDictionary(), indent=4)
        containers_array.append(b.getResultDictionary())

    #add statusNumber
    statusNumber=None
    if(flag_success==True):
        #allsuccess
        statusNumber=1
    elif(flag_success==False and flag_partial_success==True):
        #partial success
        statusNumber=3
    else:
        #fail
        statusNumber=2

    #add status of containers
    final_info_dictionary={
        "status":statusNumber,
        "containers":containers_array,
        "total_container_types":total_container_types,
        "total_box_types":total_box_types
        }

    result_json_info=json.dumps(final_info_dictionary, indent=4)
 

        
        #print(b.getResultDictionary())
    print(result_json_info)
    return result_json_info




#==============================================================
#Function Name: CheckValidJsonData
#Descritpion: Check whether the json file is in the format we want
#Return: if the result is valid return true else false
#==============================================================
# TO DO!
def CheckValidJsonData(infoJsonData):
    FirstLayerKeys={'containers':False,'box':False}
    containers_sec_key={'ID':False,'TypeName':False,'X':False,'Y':False,'Z':False,'Weight_limmit':False,'Numbers':False}
    box_sec_key={'ID':False,'TypeName':False,'X':False, 'Y':False, 'Z':False, 'Weight':False, 'Numbers':False}

    firstkyes=infoJsonData.keys()
    #for key in FirstLayerKeys.keys():
#=============================================================
#
#
#=============================================================
@app.errorhandler(404)
def page_not_found(error):
   return "404 not found"
    
#=============================================================
#Function:testImg
#
#=============================================================
@app.route('/get_resource/image/<filename>', methods=['GET'])
def get_image(filename):
    filepath="./textures/"+filename
    if os.path.isfile(filepath):
        return send_file(filepath, mimetype='image/gif')
    else:
        return "404 not found"


#==============================================================
#Function Name:Index Page
#Description: used in connnection test
#==============================================================
@app.route('/api/',methods=['GET'])
def IndexPage():
    return "hello"


#===============================================================
#Function Name: upLoadFile()
#Description: handle the file that need to be upload
# the relevent config setting written in cgi_config_ini
# ===============================================================
@app.route('/api/uploadExcelSettingFile',methods=['POST'])
def upLoadExcelSettingFile():
    file=request.files['file']




#===============================================================
#Funciton Name: reciveJsonFromClient
#Description: recive the post data which content the box_info and container_info
#return: the return value send back to server side will contenet with
#data that going to be render in 3d.
#===============================================================
@app.route('/api/recv/3dbinpack/info',methods=['POST'])
def reciveJsonFromClient():
    info_jsondata=request.get_json(force=True)
    #print(info_jsondata)
    container_infos=info_jsondata['containers']
    box_infos=info_jsondata['boxes']
    if info_jsondata['pallet_mode']==1:
        print("Pallet mode on")
        pallet_infos=info_jsondata['pallet_infos']
        jsonData=Processing3DBPWithPallet(container_infos, box_infos, pallet_infos)
    else:
        container_infos=preProcessContainerInfos(container_infos)
        box_infos=preProcessBoxInfos(box_infos)
        jsonData=Processing3DBP(container_infos, box_infos)
    return jsonData
#==================================================================
#
#
#==================================================================
def preProcessContainerInfos(container_infos):
    preProcessedInfo=[]
    for container_type_index, container_info in enumerate(container_infos):
        #if the sameType of container number only is one, do nothing and pass it to algorithm
        if (container_info['Numbers'] ==1):
            container_info['TypeIndex']=1
            preProcessedInfo.append(container_info)
        #else multiple numbers condition, create copy and pass it into algorithm
        else:
            for number_index in  container_info['Numbers']:
                name_with_index=container_info['TypeName']+"_"+number_index
                container_info['name_with_index']=name_with_index
                container_info['TypeIndex']=container_type_index
                #if the index is 0 new instance keep the original ID
                if (number_index==0):
                    preProcessedInfo.append(container_info)
                else:
                    newUUID=str(uuid.uuid4())
                    container_info["ID"]=newUUID
                    #else it will create new uuidv4 for this instance
                    preProcessedInfo.append(container_info)
    print(preProcessedInfo)
    return preProcessedInfo
#=====================================================================
#Function name
#Description
#=====================================================================
def preProcessBoxInfos(box_infos):
    return preProcessContainerInfos(box_infos)

if __name__=="__main__":
    app.run()
