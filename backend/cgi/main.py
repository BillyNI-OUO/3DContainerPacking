from flask import Flask
from flask import request
from flask_cors import CORS
from py3dbp import Packer, Bin, Item
import json



#===========================================================
#Gobal variable
#===========================================================
#RESULT_JSON_INFOS=[]


#============================================================
#Gobal config
#============================================================
app=Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

#=============================================================
#Function Name: Processsing3DBP
#Description: convert box_info and container info 
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

    #processing box_info
    for box_info in box_infos:
        #if the sameType of box only is one, do nothing and pass it to algorithm
        if (box_info['Numbers'] ==1):
            packer.add_item(Item(box_info['ID'], box_info['TypeName'], box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight']))

        #else create copy and pass it into algorithm
        else:
            for number_index in range(int(box_info['Numbers'])):
                name_with_index=box_info['TypeName']+"_"+str(+number_index)
                packer.add_item(Item(box_info['ID'], name_with_index, box_info['X'], box_info['Y'], box_info['Z'], box_info['Weight']))
    
    #processing container_info
    for container_info in container_infos:
        #if the sameType of container number only is one, do nothing and pass it to algorithm
        if (container_info['Numbers'] ==1):
            packer.add_bin(Bin(container_info['ID'], container_info['TypeName'], container_info['X'], container_info['Y'], container_info['Z'], container_info['Weight']))

        #else create copy and pass it into algorithm
        else:
            for number_index in container_info['Numbers']:
                name_with_index=container_info['TypeName']+"_"+number_index
                packer.add_bin(Bin(container_info['ID'], name_with_index, container_info['X'], container_info['Y'], container_info['Z'], container_info['Weight_limmit']))     
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
    final_info_dictionary={"status":statusNumber, "containers":containers_array}
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
        
    


#==============================================================
#Function Name:Index Page
#Description: used in connnection test
#==============================================================
@app.route('/api/',methods=['GET'])
def IndexPage():
    return "hello"



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

    jsonData=Processing3DBP(container_infos, box_infos)
    return jsonData

app.run()