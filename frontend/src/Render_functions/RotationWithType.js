//import  * as BABYLON from  "@babylonjs/core";

var rotateWithType = function (mesh, rotationType) {
    if(rotationType==0){
        return

    }else if(rotationType==1){
        mesh.rotation.z = Math.PI/2;

    }else if(rotationType==2){
        mesh.rotation.y=Math.PI/2;

    }else if(rotationType==3){
        mesh.rotation.x=Math.PI/2;
        mesh.rotation.y=Math.PI/2;

    }else if(rotationType==4){
        mesh.rotation.x=Math.PI/2;

    }else if(rotationType==5){
        mesh.rotation.x=Math.PI/2;
        mesh.rotation.z= Math.PI/2;

    }else{
        console.log("rotation error: unknow type")
    }
}
export default rotateWithType;