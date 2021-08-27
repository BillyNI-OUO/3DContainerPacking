
 import  * as BABYLON from  "@babylonjs/core";
 import Swal from "sweetalert2";
      //define box hover actions
      // Over/Out

      const actions={
      makeOverOut(mesh) {
        mesh.actionManager.registerAction(
          new BABYLON.SetValueAction(
            BABYLON.ActionManager.OnPointerOutTrigger,
            mesh.material,
            "emissiveColor",
            mesh.material.emissiveColor
          )
        );
        mesh.actionManager.registerAction(
          new BABYLON.SetValueAction(
            BABYLON.ActionManager.OnPointerOverTrigger,
            mesh.material,
            "emissiveColor",
            BABYLON.Color3.White()
          )
        );
        //uncomment the following line to make the box size chage while clicked.
        //mesh.actionManager.registerAction(new BABYLON.InterpolateValueAction(BABYLON.ActionManager.OnPointerOutTrigger, mesh, "scaling", new BABYLON.Vector3(1, 1, 1), 150));
        //mesh.actionManager.registerAction(new BABYLON.InterpolateValueAction(BABYLON.ActionManager.OnPointerOverTrigger, mesh, "scaling", new BABYLON.Vector3(1.1, 1.1, 1.1), 150));
      },
      makeOnClickShowInfo(mesh, render_infos){
        mesh.actionManager.registerAction(
          new BABYLON.ExecuteCodeAction(
              BABYLON.ActionManager.OnPickTrigger,
              function(evt){
            let titlestr="BoxName:"+render_infos['TypeName']
       Swal.fire({
          title: titlestr,
          text: "Do you want to continue",
          icon: "error",
          confirmButtonText: "Cool",
        });
        console.log("clicked the box"+evt);
              }//end function
          )
        )
      }//end makeOnClickShowInfo
    }//end actions

      export default actions;
      