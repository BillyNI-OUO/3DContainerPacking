//import  * as BABYLON from  "@babylonjs/core";
/*
class RotationType:
    RT_WHD = 0
    RT_HWD = 1
    RT_HDW = 2
    RT_DHW = 3
    RT_DWH = 4
    RT_WDH = 5
*/

var rotateWithType = function (xyz_array, rotationType) {
   //console.log("rotationType"+rotationType)
    if(rotationType==0){
        return xyz_array

    }else if(rotationType==1){
        //yxz
        let temp=[]
        temp.push(xyz_array[1],xyz_array[0],xyz_array[2])
        return temp

    }else if(rotationType==2){
        //yzx
        let temp=[]
        temp.push(xyz_array[1],xyz_array[2],xyz_array[0])
        return temp

    }else if(rotationType==3){
        //zyx
        let temp=[]
        temp.push(xyz_array[2],xyz_array[1],xyz_array[0])
        return temp

    }else if(rotationType==4){
        //zxy
        let temp=[]
        temp.push(xyz_array[2], xyz_array[0], xyz_array[1])        
        return temp

    }else if(rotationType==5){
        //xzy
        let temp=[]
        temp.push(xyz_array[0], xyz_array[2], xyz_array[1])
        return temp
    }else{
        console.log("rotation error: unknow type")
        return xyz_array
    }
}
export default rotateWithType;