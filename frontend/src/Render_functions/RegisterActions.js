
 import  * as BABYLON from  "@babylonjs/core";
      //define box hover actions
      // Over/Out
      var makeOverOut = function (mesh) {
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
      };

      export default makeOverOut;