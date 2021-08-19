<template>
  <canvas id="renderCanvas"></canvas>
</template>


<script>
import * as BABYLON from "@babylonjs/core";
import {AdvancedDynamicTexture} from "@babylonjs/gui";
import {Button} from "@babylonjs/gui";
import Swal from 'sweetalert2'
import { GridMaterial } from "@babylonjs/materials/grid";
import "babylonjs-materials";
// Required side effects to populate the Create methods on the mesh class. Without this, the bundle would be smaller but the createXXX methods from mesh would not be accessible.
import "@babylonjs/core/Meshes/meshBuilder";
import { mapState } from "vuex";

//import my render javascript functions.
import TestRender from "@/Render_functions/TestRender";

export default {
  name: "Render",
  components: {},
  //container_info structure:
  //            ID:'',
  //            X:'',
  //            Y:'',
  //            Z:'',
  //            Weight_limmit:'',
  //            Numbers:''

  //========================================
  //Computed:
  //Description: Initialize the variable
  //========================================
  computed: mapState({
    container_infos: (state) => state.container_infos,
    box_infos: (state) => state.box_infos,
  }),

  mounted() {
    //*You have to initialize the value before create scene

    //container setting
    console.log("container_infos:x" + this.container_infos[0].X);
    var container_infos = this.container_infos;

    //box setting
    console.log("box_infos:x" + this.box_infos[0].X);
    console.log("box_infos:ID" + this.box_infos[0].TypeName);
    var box_infos = this.box_infos;

    var canvas = document.getElementById("renderCanvas"); // 得到canvas对象的引用
    var engine = new BABYLON.Engine(canvas, true); // 初始化 BABYLON 3D engine

    /*========================WARNNING======================================= */
    //you can not asccess 'this.xxx' property after create the scene

    /******* Add the create scene function ******/
    var createScene = function () {
      //create scene
      var scene = new BABYLON.Scene(engine);
      //=========uncomment the following line to set debug mode=======*/
      //scene.debugLayer.show();

      const camera = new BABYLON.ArcRotateCamera(
        "camera",
        -Math.PI / 2,
        Math.PI / 2.5,
        3,
        new BABYLON.Vector3(0, 4, 0),
        scene
      );
      camera.attachControl(canvas, true);
      // 添加一组灯光到场景
      // eslint-disable-next-line no-unused-vars
      var light1 = new BABYLON.HemisphericLight(
        "light1",
        new BABYLON.Vector3(1, 1, 0),
        scene
      );
      // eslint-disable-next-line no-unused-vars
      var light2 = new BABYLON.PointLight(
        "light2",
        new BABYLON.Vector3(0, 1, -1),
        scene
      );
      //my code
      //================================================
      // Create Container
      //================================================
      var container_width = container_infos[0].X;

      var container_height = container_infos[0].Y;
      var container_deepth = container_infos[0].Z;
      const container = BABYLON.MeshBuilder.CreateBox("container", {
        height: container_height,
        width: container_width,
        depth: container_deepth,
      });
      //Create the container material
      var mat_for_container = new BABYLON.StandardMaterial("mat", scene);
      mat_for_container.diffuseColor = BABYLON.Color3.White();
      mat_for_container.alpha = 0.3;
      //Attach material to the container
      container.material = mat_for_container;

      //set the position y of container so that it can stand on the "ground"
      container.position.y += container_height / 2;

      //===================================================
      //Calculate the upper left corner position on x-z plane
      //===================================================
      var origin_coordinate_x = 0 - container_infos[0].X / 2;
      //var origin_coordinate_y; y base on box its own height
      var origin_coordinate_z = container_infos[0].Z / 2;

      //===================================================
      //Create the box
      //===================================================
      var boxes_array = [];

      //Create the box1 material
      var mat_for_boxes0 = new BABYLON.StandardMaterial("matboxes0", scene);
      mat_for_boxes0.diffuseColor = BABYLON.Color3.Blue();
      mat_for_boxes0.alpha = 0.5;


      //define box hover actions
          // Over/Out
    var makeOverOut = function (mesh) {
        mesh.actionManager.registerAction(new BABYLON.SetValueAction(BABYLON.ActionManager.OnPointerOutTrigger, mesh.material, "emissiveColor", mesh.material.emissiveColor));
        mesh.actionManager.registerAction(new BABYLON.SetValueAction(BABYLON.ActionManager.OnPointerOverTrigger, mesh.material, "emissiveColor", BABYLON.Color3.White()));
        //uncomment the following line to make the box size chage while clicked.
        //mesh.actionManager.registerAction(new BABYLON.InterpolateValueAction(BABYLON.ActionManager.OnPointerOutTrigger, mesh, "scaling", new BABYLON.Vector3(1, 1, 1), 150));
        //mesh.actionManager.registerAction(new BABYLON.InterpolateValueAction(BABYLON.ActionManager.OnPointerOverTrigger, mesh, "scaling", new BABYLON.Vector3(1.1, 1.1, 1.1), 150));
    }



      //for loop create box
      for (var iter = 0; iter != box_infos[0].Numbers; iter++) {
        let box_name = "box_" + iter; //box_0, box_1, box_2 ...
        console.log("create boxes, box_name:" + box_name);
        boxes_array.push(
          BABYLON.MeshBuilder.CreateBox(box_name, {
            height: box_infos[0].X,
            width: box_infos[0].Y,
            depth: box_infos[0].Z,
          })
        );
        //attach material
        boxes_array[iter].material = mat_for_boxes0;

        boxes_array[iter].position.x =
          box_infos[0].X * (iter + 1) +
          origin_coordinate_x -
          box_infos[0].X / 2;
        boxes_array[iter].position.y += box_infos[0].Y / 2;
        boxes_array[iter].position.z = origin_coordinate_z - box_infos[0].Z / 2;

        //register the action that,if box is clicked, alert the box ID
        boxes_array[iter].actionManager=new BABYLON.ActionManager(scene);

      } //end for loop
      console.log(boxes_array)
    
  



      //register action for all of the boxes
      makeOverOut(boxes_array[0]);


      //container.material=skyboxMaterial;
      TestRender.testTexture(scene);

      // Create my custom ground
      var ground = BABYLON.MeshBuilder.CreateGround("ground1", {
        height: 500,
        width: 500,
        subdivisions: 4,
      });

      //Attach grid material to the ground
      var ground_material = new GridMaterial("grid", scene);
      ground_material.majorUnitFrequency = 20;
      ground_material.minorUnitVisibility = 0;
      ground.material = ground_material;
        
        
        // GUI
    var advancedTexture =AdvancedDynamicTexture.CreateFullscreenUI("UI");

    var button1 = Button.CreateSimpleButton("but1", "Click Me");
    button1.width = "150px"
    button1.height = "40px";
    button1.color = "white";
    button1.cornerRadius = 20;
    button1.background = "green";
    button1.onPointerUpObservable.add(function() {
Swal.fire({
  title: 'Error!',
  text: 'Do you want to continue',
  icon: 'error',
  confirmButtonText: 'Cool'
})

    });
    advancedTexture.addControl(button1);    
      //uncomment the following line to make eviroment rotate.
      /* 
	engine.runRenderLoop(function () {
		camera.alpha += 0.004;
	});
  */
      return scene;
    };
    /******* End of the create scene function ******/
    var scene = createScene(); //Call the createScene function
    // 最后一步调用engine的runRenderLoop方案，执行scene.render()，让我们的3d场景渲染起来
    engine.runRenderLoop(function () {
      scene.render();
    });
    // 监听浏览器改变大小的事件，通过调用engine.resize()来自适应窗口大小
    window.addEventListener("resize", function () {
      engine.resize();
    });
  }, //end monted
};
</script>

<style>
#renderCanvas {
  width: 100%;
  height: 100%;
  touch-action: none;
}
</style>
