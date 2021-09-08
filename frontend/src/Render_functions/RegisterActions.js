
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
      makeOnClickShowInfo(mesh, box_infos){
        this.box_infos=box_infos;
        mesh.actionManager.registerAction(
          new BABYLON.ExecuteCodeAction(
              BABYLON.ActionManager.OnPickTrigger,
              () => {
                Swal.fire({
                  icon: 'info',
                  title: this.box_infos["TypeName"],
                  text: 'X:'+this.box_infos['X']+'\n'+'Y:'+this.box_infos['Y']+'\n'+'Z:'+this.box_infos['Z']+'\n'+"Weight:"+this.box_infos['Weight'],
                  //footer: '<a href="">Why do I have this issue?</a>'
                })
            }
          )
        )
      }//end makeOnClickShowInfo
    }//end actions

      export default actions;
      