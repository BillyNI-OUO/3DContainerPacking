<template>
  <div>
    <canvas id="renderCanvas" ref="ref_renderCanvas"></canvas>
    <ul id="hover">
      <li
        id="camera"
        class="camera"
        title="Free Camera [S]"
        onclick="toolSelector('camera', false)"
        v-on:pointerdown="dragElement($event)"
      >
        <i class="material-icons">control_camera</i>
      </li>
      <li class="add" title="Add [W]" onclick="toolSelector('add', true)">
        <i class="material-icons">create</i>
      </li>
      <li
        class="remove"
        title="Remove [D]"
        onclick="toolSelector('remove', true)"
      >
        <i class="material-icons">clear</i>
      </li>
      <li
        class="transform"
        title="Transform [A]"
        onclick="toolSelector('transform', true)"
      >
        <i class="material-icons">border_inner</i>
      </li>
      <li
        class="symmetry"
        title="Symmetry for Add, Remove, Transform, Paint Color"
      >
        <select id="inputsymmetry">
          <option style="color: #444" value="" selected="selected">
            &nbsp;S
          </option>
          <option style="color: #c83c43" value="x">&nbsp;X</option>
          <option style="color: #47c64b" value="y">&nbsp;Y</option>
          <option style="color: #6493d2" value="z">&nbsp;Z</option>
        </select>
      </li>
    </ul>

    <!-- dynamic -->
    <div v-if="render_loading_status" class="overlay">
      <loading-page></loading-page>
    </div>
  </div>
</template>


<script>
import LoadingPage from "./LoadingPage.vue";
import * as BABYLON from "@babylonjs/core";
//import { AdvancedDynamicTexture } from "@babylonjs/gui";
//import { Button } from "@babylonjs/gui";
//import Swal from "sweetalert2";
import { GridMaterial } from "@babylonjs/materials/grid";
import "babylonjs-materials";
// Required side effects to populate the Create methods on the mesh class. Without this, the bundle would be smaller but the createXXX methods from mesh would not be accessible.
import "@babylonjs/core/Meshes/meshBuilder";
import { mapState } from "vuex";
//====================================================
//import my render javascript functions.
//====================================================
import showAxis from "@/Render_functions/ShowAxis";
import actions from "@/Render_functions/RegisterActions";
import rotationWithType from "@/Render_functions/RotationWithType";
//import customLoadSreen from "@/Render_functions/RotationWithType"
//import hover_tool from "@/toolkit_functions/hover_tool";

import "material-icons/iconfont/material-icons.css";
import Swal from "sweetalert2";

export default {
  name: "Render",
  components: {
    LoadingPage,
  },
  //========================================
  //Computed:
  //Description: Initialize the variable
  //========================================
  computed: mapState({
    container_infos: (state) => state.container_infos,
    box_infos: (state) => state.box_infos,
    render_infos: (state) => state.render_infos,
    pallet_infos:(state)=>state.pallet_infos,
    render_loading_status: (state) => state.render_loading_status,
    pallet_mode:(state)=>state.pallet_mode
  }), //end compute
  data() {
    return {
      engine: "",
      canvas: "",
      xOffset: 0,
      yOffset: 0,
    };
  },
  methods: {
    dragStart(e) {
      if (e.type === "touchstart") {
        this.initialX = e.touches[0].clientX - this.xOffset;
        this.initialY = e.touches[0].clientY - this.yOffset;
      } else {
        this.initialX = e.clientX - this.xOffset;
        this.initialY = e.clientY - this.yOffset;
      }
      if (e.target === this.elem.target) this.active = true;
    },
    dragElement(elem) {
      this.elem = elem;
      this.active = false;
      //let currentX, currentY, initialX, initialY;

      // prevent fast-dragging problem with background elements
      document.body.addEventListener("pointerdown", this.dragStart, false);
      document.body.addEventListener("pointerup", this.dragEnd, false);
      document.body.addEventListener("pointermove", this.drag, false);
      document.body.addEventListener("touchstart", this.dragStart, false);
      document.body.addEventListener("touchend", this.dragEnd, false);
      document.body.addEventListener("touchmove", this.drag, false);
    },
    dragEnd() {
      this.initialX = this.currentX;
      this.initialY = this.currentY;
      this.active = false;
      document.body.removeEventListener("pointerdown", this.dragStart, false);
      document.body.removeEventListener("pointerup", this.dragEnd, false);
      document.body.removeEventListener("pointermove", this.drag, false);
      document.body.removeEventListener("touchstart", this.dragStart, false);
      document.body.removeEventListener("touchend", this.dragEnd, false);
      document.body.removeEventListener("touchmove", this.drag, false);
    },
    drag(e) {
      if (this.active) {
        if (e.type === "touchmove") {
          this.currentX = e.touches[0].clientX - this.initialX;
          this.currentY = e.touches[0].clientY - this.initialY;
        } else {
          this.currentX = e.clientX - this.initialX;
          this.currentY = e.clientY - this.initialY;
        }
        this.xOffset = this.currentX;
        this.yOffset = this.currentY;
        this.setTranslate(this.currentX, this.currentY);
      }
    },
    setTranslate(xPos, yPos) {
      this.elem.target.parentElement.style.transform =
        "translate3d(" + xPos + "px, " + yPos + "px, 0)";
    },
    handleRenderLoop() {
      this.scene.render();
    },
    handleChangeWindowSize() {
      this.engine.resize();
    }, //end change size

    createSceneWithPallet(){
           this.canvas = document.getElementById("renderCanvas"); // 得到canvas对象的引用
      //this.engine= new BABYLON.Engine(this.canvas, true) // 初始化 BABYLON 3D engine

      this.engine = new BABYLON.Engine(this.canvas, true, null, false);
      this.engine.disablePerformanceMonitorInBackground = true;
      this.engine.enableOfflineSupport = false;
      this.engine.doNotHandleContextLost = true;
      this.engine.useHighPrecisionFloats = false;

      console.log("canvas" + this.canvas);
      console.log("engine" + this.engine);

      var render_infos = this.render_infos;
      //create scene
      var scene = new BABYLON.Scene(this.engine);
      this.scene=scene
      //==========================================================================
      //Enable physical engine
      //==========================================================================
      //this.scene.enablePhysics(new BABYLON.Vector3(0,-10,0), new BABYLON.AmmoJSPlugin());




      this.scene = scene;
      //=========================================================================
      //global variables
      //=========================================================================
      var controlBoxes_originate_cordinate_z = 100;
      var max_box_width=0
      var controlBoxes_originate_cordinate_x = 0-max_box_width/2 -200;
      var controlBoxes_margin = 20;
      //array that store the mesh of the box inside the containers
      var box_mesh_array = [];
      //also create additional box for show the box information
      var control_box_mesh_arrary = [];

      //control box setting
      const total_box_types = render_infos["total_box_types"];
      var sameTypeHaveBeenDraw = new Array(total_box_types);
      for (let i = 0; i < total_box_types; i++) {
        sameTypeHaveBeenDraw[i] = false;
      }

      //=====================================================================
      //uncomment the following line to set debug mode
      //=====================================================================
      //this.scene.debugLayer.show();

      //======================starting create elements=======================

      //global variable
      var ground_size = 500;
      var total_container_number = render_infos["containers"].length;
      //var container_margin=10
      showAxis(50, scene);

      console.log(
        "render_infos['containers'].lenght:" + total_container_number
      );

      //draw containers
      //random color function color(0~1)
      function getRandomColor(min, max) {
        let r = 1;
        let g = 1;
        let b = 1;
        r = Math.random() * (max - min) + min;
        g = Math.random() * (max - min) + min;
        b = Math.random() * (max - min) + min;
        return new BABYLON.Color3(r, g, b);
      }
      //=====================================================
      //Create Skybox
      // Not working for bbjs interal render reason
      //=====================================================
      var skybox = BABYLON.Mesh.CreateBox("skyBox_", { size: 1.0 }, this.scene);
      var skyboxMaterial = new BABYLON.StandardMaterial(
        "skyBox_material",
        this.scene
      );
      skyboxMaterial.backFaceCulling = false;
      skyboxMaterial.disableLighting = true;
      skyboxMaterial.diffuseColor = new BABYLON.Color3(0, 0, 0);
      skyboxMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
      skyboxMaterial.backFaceCulling = false;
      skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture(
        "http://127.0.0.1:5000/get_resource/image/skybox",
        this.scene
      );
      skyboxMaterial.reflectionTexture.coordinatesMode =
        BABYLON.Texture.SKYBOX_MODE;
      skyboxMaterial.disableLighting = true;
      skybox.material = skyboxMaterial;

      //=====================================================
      //create material array for containers
      //=====================================================
      var container_mat_array = [];
      for (let i = 0; i < render_infos["total_container_types"]; i++) {
        let container_mat_name =
          render_infos["containers"][i]["TypeName"] + "mat";
        let mat = new BABYLON.StandardMaterial(container_mat_name, scene);
        mat.diffuseColor = getRandomColor(0.6, 1);
        mat.alpha = 0.5;
        container_mat_array.push(mat);
      }
      //=======================================================
      //create container array
      //=======================================================
      var containers_mesh_array = [];
      for (let i = 0; i < render_infos["containers"].length; i++) {
        console.log(render_infos["containers"][i]["ID"]);
        let container_mesh_name = render_infos["containers"][i]["ID"];
        let cont = BABYLON.MeshBuilder.CreateBox(container_mesh_name, {
          width: render_infos["containers"][i]["X"],
          height: render_infos["containers"][i]["Y"],
          depth: render_infos["containers"][i]["Z"],
        });
        //attach material
        cont.material =
          container_mat_array[render_infos["containers"][i]["TypeIndex"]];
        //registre actions
        //cont.actionManager = new BABYLON.ActionManager(scene);
        //makeOverOut(cont);
        //=========================================================
        //Move the first container to 0,0,0 and set its position as reference
        //=========================================================
        if (i == 0) {
          //move the container to the ground
          cont.position.y = render_infos["containers"][0]["Y"] / 2;
          //move the container[0] align to 0,0,0
          cont.position.z = render_infos["containers"][0]["Z"] / 2;
          cont.position.x = render_infos["containers"][0]["X"] / 2;
          containers_mesh_array.push(cont);
        } else {
          for (let i = 1; i < total_container_number; i++) {
            //move the container to the ground
            cont.position.y = render_infos["containers"][i]["Y"] / 2;
            //move the container[0] align to 0,0,0
            cont.position.z += render_infos["containers"][i]["Z"] / 2;
            cont.position.x =
              containers_mesh_array[i - 1].position.x +
              30 +
              render_infos["containers"][i]["X"] / 2 +
              render_infos["containers"][i - 1]["X"] / 2;
            containers_mesh_array.push(cont);

            console.log(containers_mesh_array);
          }
        }
      } //end create container array for

      //move the position for each container

      //=========================================================
      //Move the first container to 0,0,0 and set its position as reference
      //=========================================================
      //move the container to the ground
      containers_mesh_array[0].position.y =
        render_infos["containers"][0]["Y"] / 2;
      //move the container[0] align to 0,0,0
      containers_mesh_array[0].position.z =
        render_infos["containers"][0]["Z"] / 2;
      containers_mesh_array[0].position.x =
        render_infos["containers"][0]["X"] / 2;

      //move other containers if exsist

      //========================================================================
      //Calculate the upper left corner position on x-z plane for each container
      //========================================================================
      //y should depend on box its own height
      let left_top_positions_array = [];
      let origin_coordinate_x = 0;
      let origin_coordinate_z = 0;
      left_top_positions_array.push({
        X: origin_coordinate_x,
        Z: origin_coordinate_z,
      });
      for (let i = 1; i < total_container_number; i++) {
        let origin_coordinate_x =
          containers_mesh_array[i].position.x -
          render_infos["containers"][i]["X"] / 2;
        let origin_coordinate_z = 0;
        /*
          containers_mesh_array[i].position.z +
          render_infos["containers"][i]["Z"] / 2;
          */
        left_top_positions_array.push({
          X: origin_coordinate_x,
          Z: origin_coordinate_z,
        });
      }

      //=====================================================
      //create material array for pallet
      //=====================================================
      var pallet_mat_array=[];
      for(let i=0; i<render_infos["total_pallet_types"]; i++){
          let pallet_mat_name="palletmat"+i
          let mat=new BABYLON.StandardMaterial(pallet_mat_name, scene);
          mat.diffuseColor = getRandomColor(0.5, 1);
          mat.alpha = 0.5;
        //mat.diffuseTexture = new BABYLON.Texture("http://127.0.0.1:5000/get_resource/image", scene);
        pallet_mat_array.push(mat);
      }

      //=====================================================
      //create material array for boxes
      //=====================================================
      var box_mat_array = [];
      for (let i = 0; i < render_infos["total_box_types"]; i++) {
        let box_mat_name = "boxmat" + i;
        let mat = new BABYLON.StandardMaterial(box_mat_name, scene);
        mat.diffuseColor = getRandomColor(0.5, 1);
        mat.alpha = 0.5;
        //mat.diffuseTexture = new BABYLON.Texture("http://127.0.0.1:5000/get_resource/image", scene);
        box_mat_array.push(mat);
      }

      //=========================================================================
      //create the fitted boxes for each container
      //=========================================================================

      for (const [index_of_container, container] of render_infos[
        "containers"
      ].entries()) {

        //For loop for pallet
        for(const  pallet of container['Fitted_items']){

          //====================================================================
          //rotate the every pallets first, so that we are able to get the ofset
          //====================================================================

          let origin_xyz_array_of_current_pallet = [
            pallet["X"],
            pallet["Y"],
            pallet["Z"],
          ];
         let new_xyz_array_of_current_pallet = rotationWithType(origin_xyz_array_of_current_pallet, pallet["RotationType"]);
          let pallet_x = new_xyz_array_of_current_pallet[0];
          let pallet_y = new_xyz_array_of_current_pallet[1];
          let pallet_z = new_xyz_array_of_current_pallet[2];

          let pallet_mesh_name = pallet["ID"];
          let pallet_instance = BABYLON.MeshBuilder.CreateBox(pallet_mesh_name, {
            width: pallet_x,
            height: pallet_y,
            depth: pallet_z,
          });

          pallet_instance.position.x =
            left_top_positions_array[index_of_container]["X"] +
            pallet["position_x"] +
            pallet_x / 2;
          pallet_instance.position.y =
            pallet_y / 2 + pallet["position_y"];
          pallet_instance.position.z =
            //left_top_positions_array[index_of_container]["Z"] +
          pallet["position_z"] + pallet_z / 2;


        //console.log(container["Fitted_items"].length);


        //=======================================================================
        //For loop to create the boxes
        //=======================================================================
        for (let i = 0; i < pallet["Fitted_items"].length; i++) {
          //==========================================================
          //Rotate the boxes based on differend conditions
          //==========================================================
          let rotateType = pallet["Fitted_items"][i]["RotationType"];
          console.log("rotateType" + rotateType);
          //rotate the box
          let origin_xyz_array = [
            pallet["Fitted_items"][i]["X"],
            pallet["Fitted_items"][i]["Y"],
            pallet["Fitted_items"][i]["Z"],
          ];
          let xyz_array = rotationWithType(origin_xyz_array, rotateType);

          //if the pallet is rotated, the box load on this pallet also have to be rotated
          //  not something like this=>  xyz_array=rotationWithType(xyz_array,  pallet["RotationType"])
          
          let box_x = xyz_array[0];
          let box_y = xyz_array[1];
          let box_z = xyz_array[2];



          //==================================================
          //update the max_box_width if found one
          //this is nothing to do with create box, just make sure the
          //distance between drawing box and control boxes.
          //==================================================
          if (box_x> max_box_width){
            max_box_width=box_x
          }


          let box_mesh_name = pallet["Fitted_items"][i]["ID"];
          let box_instance = BABYLON.MeshBuilder.CreateBox(box_mesh_name, {
            width: box_x,
            height: box_y,
            depth: box_z,
          });
          //======================================================
          //Set the box material
          //======================================================
          box_instance.material =
            box_mat_array[pallet["Fitted_items"][i]["TypeIndex"]];

          box_instance.receiveShadows = true;
          box_instance.doNotSyncBoundingInfo = true;
          box_instance.cullingStrategy =
            BABYLON.AbstractMesh.CULLINGSTRATEGY_BOUNDINGSPHERE_ONLY;
          //scene.lights[1].getShadowGenerator().addShadowCaster(box_instance);

          console.log(box_instance);

          //======================================================
          //Set the box position
          //======================================================

          //if pallet have been rotated, exchange x, z position
          if(pallet["RotationType"]!=0){

            console.log("rotated!!!!!!!!!!!!!")
            box_instance.position.x =left_top_positions_array[index_of_container]["X"] +
            pallet["Fitted_items"][i]["position_z"] +
            box_x / 2 +     //+pallet offset
            pallet["position_x"];
            
          box_instance.position.y =
            box_y / 2 + 
            pallet["Fitted_items"][i]["position_y"]+
            pallet["Y"] //+pallet height
            ;
          box_instance.position.z =
          //left_top_positions_array[index_of_container]["Z"] +
            pallet["Fitted_items"][i]["position_x"] + 
            box_z / 2+
            pallet["position_z"]
            ;
          }else{
          box_instance.position.x =left_top_positions_array[index_of_container]["X"] +
            pallet["Fitted_items"][i]["position_x"] +
            box_x / 2 +     //+pallet offset
            pallet["position_x"];
            
          box_instance.position.y =
            box_y / 2 + 
            pallet["Fitted_items"][i]["position_y"]+
            pallet["Y"] //+pallet height
            ;
          box_instance.position.z =//left_top_positions_array[index_of_container]["Z"] +
            pallet["Fitted_items"][i]["position_z"] + 
            box_z / 2+
            pallet["position_z"]
            ;
          }
          //===========================================================
          //Create control box
          //===========================================================
          //console.log("control box");
          console.log(
            sameTypeHaveBeenDraw[pallet["Fitted_items"][i]["TypeIndex"]]
          );
          if (
            sameTypeHaveBeenDraw[pallet["Fitted_items"][i]["TypeIndex"]] ==
            false
          ) {
            let control_box = box_instance.clone("abox");
            control_box.position.z = controlBoxes_originate_cordinate_z;
            control_box.position.x = controlBoxes_originate_cordinate_x;
            control_box.position.y = box_y / 2;
            controlBoxes_originate_cordinate_z =
              controlBoxes_originate_cordinate_z - box_z - controlBoxes_margin;
            sameTypeHaveBeenDraw[
              pallet["Fitted_items"][i]["TypeIndex"]
            ] = true;

            //======================================================
            //Register actions for control box and boxes
            //======================================================
            control_box.actionManager = new BABYLON.ActionManager(scene);
            actions.makeOverOut(control_box);
            actions.makeOnClickShowInfo(
              control_box,
              pallet["Fitted_items"][i]
            );
            control_box_mesh_arrary.push(control_box);
          } //end create control box

          box_instance.actionManager = new BABYLON.ActionManager(scene);
          console.log("test");
          console.log(pallet["Fitted_items"][i]);
          actions.makeOverOut(
            box_instance,
            pallet["Fitted_items"][i]["TypeName"],
            pallet["Fitted_items"][i]["X"],
            pallet["Fitted_items"][i]["Y"],
            pallet["Fitted_items"][i]["Z"],
            pallet["Fitted_items"][i]["Weight"]
          );

          box_mesh_array.push(box_instance);
        } //end inner for
        }//end for (pallet)
      } //end outter for (container)

      const camera = new BABYLON.ArcRotateCamera(
        "camera",
        -Math.PI / 2,
        Math.PI / 2.5,
        3,
        new BABYLON.Vector3(0, 4, 0),
        scene
      );

      function setLightPositionByAngle(light, angle, distance, height) {
        const x = Math.cos((angle * Math.PI) / 180) * distance;
        const y = height;
        const z = Math.sin((angle * Math.PI) / 180) * distance;
        const pos = new BABYLON.Vector3(x, y, z);
        light.position = pos; // our primary shadow light
        light.setDirectionToTarget(BABYLON.Vector3.Zero());
      }

      camera.attachControl(this.canvas, true);
      const ambient = new BABYLON.HemisphericLight(
        "ambient",
        new BABYLON.Vector3(0, 1, 0),
        scene
      );
      ambient.diffuse = new BABYLON.Color3(0.5, 0.5, 0.5);
      ambient.specular = new BABYLON.Color3(0, 0, 0);
      ambient.groundColor = new BABYLON.Color3(0.4, 0.4, 0.4);
      ambient.intensity = 0.3;

      const light = new BABYLON.DirectionalLight(
        "light",
        new BABYLON.Vector3(0, -1, 0),
        scene
      );
      setLightPositionByAngle(light, 120, 50, 100);
      light.autoUpdateExtends = true;
      light.diffuse = new BABYLON.Color3(1, 1, 1);
      light.intensity = 1;

      const shadowGen = new BABYLON.ShadowGenerator(512, light); // shadows updated manually on SPS.mesh changes,
      shadowGen.getShadowMap().refreshRate =
        BABYLON.RenderTargetTexture.REFRESHRATE_RENDER_ONCE; // to save performance
      shadowGen.filteringQuality = BABYLON.ShadowGenerator.QUALITY_LOW;
      shadowGen.useExponentialShadowMap = false;
      shadowGen.usePercentageCloserFiltering = true;
      shadowGen.setDarkness(0.6);

      // Create my custom ground
      var ground = BABYLON.MeshBuilder.CreateGround("ground1", {
        height: ground_size,
        width: ground_size,
        subdivisions: 4,
      });
      //========================================================
      //Create ground Material
      //Attach grid material to the ground
      //===========================================================

      var ground_material = new GridMaterial("grid", this.scene);
      ground_material.backFaceCulling = false;
      ground_material.gridRatio = 1;
      ground_material.mainColor = new BABYLON.Color3.White();
      ground_material.lineColor = new BABYLON.Color3(0.7, 0.7, 0.7);
      ground_material.opacity = 0.3;
      //ground_material.freeze();
      //ground_material.isPickable = false;
      //ground_material.doNotSyncBoundingInfo = true;

      ground_material.diffuseColor = BABYLON.Color3.Blue();
      ground_material.majorUnitFrequency = 20;
      //ground_material.minorUnitFrequency = 5;
      ground_material.minorUnitVisibility = 0;
      ground.material = ground_material;

      //const gridTexture = createGridTexture();
      //const defaultMaterial = createMaterial(gridTexture);
      //ground.material = defaultMaterial;

      //uncomment the following line to make eviroment rotate.
      /* 
	engine.runRenderLoop(function () {
		camera.alpha += 0.004;
	});
  */
      return scene;


    },
    createScene() {
      this.canvas = document.getElementById("renderCanvas"); // 得到canvas对象的引用
      //this.engine= new BABYLON.Engine(this.canvas, true) // 初始化 BABYLON 3D engine

      this.engine = new BABYLON.Engine(this.canvas, true, null, false);
      this.engine.disablePerformanceMonitorInBackground = true;
      this.engine.enableOfflineSupport = false;
      this.engine.doNotHandleContextLost = true;
      this.engine.useHighPrecisionFloats = false;

      console.log("canvas" + this.canvas);
      console.log("engine" + this.engine);

      var render_infos = this.render_infos;
      //create scene
      var scene = new BABYLON.Scene(this.engine);
      this.scene = scene;
      //=========================================================================
      //global variables
      //=========================================================================
      var controlBoxes_originate_cordinate_z = 100;
      var max_box_width=0
      var controlBoxes_originate_cordinate_x = 0-max_box_width/2 -200;
      var controlBoxes_margin = 20;
      //array that store the mesh of the box inside the containers
      var box_mesh_array = [];
      //also create additional box for show the box information
      var control_box_mesh_arrary = [];

      //control box setting
      const total_box_types = render_infos["total_box_types"];
      var sameTypeHaveBeenDraw = new Array(total_box_types);
      for (let i = 0; i < total_box_types; i++) {
        sameTypeHaveBeenDraw[i] = false;
      }

      //=====================================================================
      //uncomment the following line to set debug mode
      //=====================================================================
      //this.scene.debugLayer.show();

      //======================starting create elements=======================

      //global variable
      var ground_size = 500;
      var total_container_number = render_infos["containers"].length;
      //var container_margin=10
      showAxis(50, scene);

      console.log(
        "render_infos['containers'].lenght:" + total_container_number
      );

      //draw containers
      //random color function color(0~1)
      function getRandomColor(min, max) {
        let r = 1;
        let g = 1;
        let b = 1;
        r = Math.random() * (max - min) + min;
        g = Math.random() * (max - min) + min;
        b = Math.random() * (max - min) + min;
        return new BABYLON.Color3(r, g, b);
      }
      //=====================================================
      //Create Skybox
      // Not working for bbjs interal render reason
      //=====================================================
      var skybox = BABYLON.Mesh.CreateBox("skyBox_", { size: 1.0 }, this.scene);
      var skyboxMaterial = new BABYLON.StandardMaterial(
        "skyBox_material",
        this.scene
      );
      skyboxMaterial.backFaceCulling = false;
      skyboxMaterial.disableLighting = true;
      skyboxMaterial.diffuseColor = new BABYLON.Color3(0, 0, 0);
      skyboxMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
      skyboxMaterial.backFaceCulling = false;
      skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture(
        "http://127.0.0.1:5000/get_resource/image/skybox",
        this.scene
      );
      skyboxMaterial.reflectionTexture.coordinatesMode =
        BABYLON.Texture.SKYBOX_MODE;
      skyboxMaterial.disableLighting = true;
      skybox.material = skyboxMaterial;

      //=====================================================
      //create material array for containers
      //=====================================================
      var container_mat_array = [];
      for (let i = 0; i < render_infos["total_container_types"]; i++) {
        let container_mat_name =
          render_infos["containers"][i]["TypeName"] + "mat";
        let mat = new BABYLON.StandardMaterial(container_mat_name, scene);
        mat.diffuseColor = getRandomColor(0.6, 1);
        mat.alpha = 0.5;
        container_mat_array.push(mat);
      }
      //=======================================================
      //create container array
      //=======================================================
      var containers_mesh_array = [];
      for (let i = 0; i < render_infos["containers"].length; i++) {
        console.log(render_infos["containers"][i]["ID"]);
        let container_mesh_name = render_infos["containers"][i]["ID"];
        let cont = BABYLON.MeshBuilder.CreateBox(container_mesh_name, {
          width: render_infos["containers"][i]["X"],
          height: render_infos["containers"][i]["Y"],
          depth: render_infos["containers"][i]["Z"],
        });
        //attach material
        cont.material =
          container_mat_array[render_infos["containers"][i]["TypeIndex"]];
        //registre actions
        //cont.actionManager = new BABYLON.ActionManager(scene);
        //makeOverOut(cont);
        //=========================================================
        //Move the first container to 0,0,0 and set its position as reference
        //=========================================================
        if (i == 0) {
          //move the container to the ground
          cont.position.y = render_infos["containers"][0]["Y"] / 2;
          //move the container[0] align to 0,0,0
          cont.position.z = render_infos["containers"][0]["Z"] / 2;
          cont.position.x = render_infos["containers"][0]["X"] / 2;
          containers_mesh_array.push(cont);
        } else {
          for (let i = 1; i < total_container_number; i++) {
            //move the container to the ground
            cont.position.y = render_infos["containers"][i]["Y"] / 2;
            //move the container[0] align to 0,0,0
            cont.position.z += render_infos["containers"][i]["Z"] / 2;
            cont.position.x =
              containers_mesh_array[i - 1].position.x +
              30 +
              render_infos["containers"][i]["X"] / 2 +
              render_infos["containers"][i - 1]["X"] / 2;
            containers_mesh_array.push(cont);

            console.log(containers_mesh_array);
          }
        }
      } //end create container array for

      //move the position for each container

      //=========================================================
      //Move the first container to 0,0,0 and set its position as reference
      //=========================================================
      //move the container to the ground
      containers_mesh_array[0].position.y =
        render_infos["containers"][0]["Y"] / 2;
      //move the container[0] align to 0,0,0
      containers_mesh_array[0].position.z =
        render_infos["containers"][0]["Z"] / 2;
      containers_mesh_array[0].position.x =
        render_infos["containers"][0]["X"] / 2;

      //move other containers if exsist

      //========================================================================
      //Calculate the upper left corner position on x-z plane for each container
      //========================================================================
      //y should depend on box its own height
      let left_top_positions_array = [];
      let origin_coordinate_x = 0;
      let origin_coordinate_z = 0;
      left_top_positions_array.push({
        X: origin_coordinate_x,
        Z: origin_coordinate_z,
      });
      for (let i = 1; i < total_container_number; i++) {
        let origin_coordinate_x =
          containers_mesh_array[i].position.x -
          render_infos["containers"][i]["X"] / 2;
        let origin_coordinate_z = 0;
        /*
          containers_mesh_array[i].position.z +
          render_infos["containers"][i]["Z"] / 2;
          */
        left_top_positions_array.push({
          X: origin_coordinate_x,
          Z: origin_coordinate_z,
        });
      }
      //=====================================================
      //create material array for boxes
      //=====================================================
      var box_mat_array = [];
      for (let i = 0; i < render_infos["total_box_types"]; i++) {
        let box_mat_name = "boxmat" + i;
        let mat = new BABYLON.StandardMaterial(box_mat_name, scene);
        mat.diffuseColor = getRandomColor(0.3, 1);
        mat.alpha = 0.5;
        //mat.diffuseTexture = new BABYLON.Texture("http://127.0.0.1:5000/get_resource/image", scene);
        box_mat_array.push(mat);
      }

      //=========================================================================
      //create the fitted boxes for each container
      //=========================================================================

      for (const [index_of_container, container] of render_infos[
        "containers"
      ].entries()) {


        
        console.log(container["Fitted_items"].length);
        for (let i = 0; i < container["Fitted_items"].length; i++) {
          //==========================================================
          //Rotate the boxes based on differend conditions
          //==========================================================
          let rotateType = container["Fitted_items"][i]["RotationType"];
          console.log("rotateType" + rotateType);
          //rotate the box
          let origin_xyz_array = [
            container["Fitted_items"][i]["X"],
            container["Fitted_items"][i]["Y"],
            container["Fitted_items"][i]["Z"],
          ];
          let xyz_array = rotationWithType(origin_xyz_array, rotateType);

          let box_x = xyz_array[0];
          let box_y = xyz_array[1];
          let box_z = xyz_array[2];

          //update the max_box_width if found one
          if (box_x> max_box_width){
            max_box_width=box_x
          }


          let box_mesh_name = container["Fitted_items"][i]["ID"];
          let box_instance = BABYLON.MeshBuilder.CreateBox(box_mesh_name, {
            width: box_x,
            height: box_y,
            depth: box_z,
          });
          //======================================================
          //Set the box material
          //======================================================
          box_instance.material =
            box_mat_array[container["Fitted_items"][i]["TypeIndex"]];

          box_instance.receiveShadows = true;
          box_instance.doNotSyncBoundingInfo = true;
          box_instance.cullingStrategy =
            BABYLON.AbstractMesh.CULLINGSTRATEGY_BOUNDINGSPHERE_ONLY;
          //scene.lights[1].getShadowGenerator().addShadowCaster(box_instance);

          console.log(box_instance);

          //======================================================
          //Set the box position
          //======================================================
          box_instance.position.x =
            left_top_positions_array[index_of_container]["X"] +
            container["Fitted_items"][i]["position_x"] +
            box_x / 2;
          box_instance.position.y =
            box_y / 2 + container["Fitted_items"][i]["position_y"];
          box_instance.position.z =
            //left_top_positions_array[index_of_container]["Z"] +
            container["Fitted_items"][i]["position_z"] + box_z / 2;
          //===========================================================
          //Create control box
          //===========================================================
          //console.log("control box");
          console.log(
            sameTypeHaveBeenDraw[container["Fitted_items"][i]["TypeIndex"]]
          );
          if (
            sameTypeHaveBeenDraw[container["Fitted_items"][i]["TypeIndex"]] ==
            false
          ) {
            let control_box = box_instance.clone("abox");
            control_box.position.z = controlBoxes_originate_cordinate_z;
            control_box.position.x = controlBoxes_originate_cordinate_x;
            control_box.position.y = box_y / 2;
            controlBoxes_originate_cordinate_z =
              controlBoxes_originate_cordinate_z - box_z - controlBoxes_margin;
            sameTypeHaveBeenDraw[
              container["Fitted_items"][i]["TypeIndex"]
            ] = true;

            //======================================================
            //Register actions for control box and boxes
            //======================================================
            control_box.actionManager = new BABYLON.ActionManager(scene);
            actions.makeOverOut(control_box);
            actions.makeOnClickShowInfo(
              control_box,
              container["Fitted_items"][i]
            );
            control_box_mesh_arrary.push(control_box);
          } //end create control box

          box_instance.actionManager = new BABYLON.ActionManager(scene);
          console.log("test");
          console.log(container["Fitted_items"][i]);
          actions.makeOverOut(
            box_instance,
            container["Fitted_items"][i]["TypeName"],
            container["Fitted_items"][i]["X"],
            container["Fitted_items"][i]["Y"],
            container["Fitted_items"][i]["Z"],
            container["Fitted_items"][i]["Weight"]
          );

          box_mesh_array.push(box_instance);
        } //end inner for
      } //end outter for

      const camera = new BABYLON.ArcRotateCamera(
        "camera",
        -Math.PI / 2,
        Math.PI / 2.5,
        3,
        new BABYLON.Vector3(0, 4, 0),
        scene
      );

      function setLightPositionByAngle(light, angle, distance, height) {
        const x = Math.cos((angle * Math.PI) / 180) * distance;
        const y = height;
        const z = Math.sin((angle * Math.PI) / 180) * distance;
        const pos = new BABYLON.Vector3(x, y, z);
        light.position = pos; // our primary shadow light
        light.setDirectionToTarget(BABYLON.Vector3.Zero());
      }

      camera.attachControl(this.canvas, true);
      const ambient = new BABYLON.HemisphericLight(
        "ambient",
        new BABYLON.Vector3(0, 1, 0),
        scene
      );
      ambient.diffuse = new BABYLON.Color3(0.5, 0.5, 0.5);
      ambient.specular = new BABYLON.Color3(0, 0, 0);
      ambient.groundColor = new BABYLON.Color3(0.4, 0.4, 0.4);
      ambient.intensity = 0.3;

      const light = new BABYLON.DirectionalLight(
        "light",
        new BABYLON.Vector3(0, -1, 0),
        scene
      );
      setLightPositionByAngle(light, 120, 50, 100);
      light.autoUpdateExtends = true;
      light.diffuse = new BABYLON.Color3(1, 1, 1);
      light.intensity = 1;

      const shadowGen = new BABYLON.ShadowGenerator(512, light); // shadows updated manually on SPS.mesh changes,
      shadowGen.getShadowMap().refreshRate =
        BABYLON.RenderTargetTexture.REFRESHRATE_RENDER_ONCE; // to save performance
      shadowGen.filteringQuality = BABYLON.ShadowGenerator.QUALITY_LOW;
      shadowGen.useExponentialShadowMap = false;
      shadowGen.usePercentageCloserFiltering = true;
      shadowGen.setDarkness(0.6);

      // Create my custom ground
      var ground = BABYLON.MeshBuilder.CreateGround("ground1", {
        height: ground_size,
        width: ground_size,
        subdivisions: 4,
      });
      //========================================================
      //Create ground Material
      //Attach grid material to the ground
      //===========================================================

      var ground_material = new GridMaterial("grid", this.scene);
      ground_material.backFaceCulling = false;
      ground_material.gridRatio = 1;
      ground_material.mainColor = new BABYLON.Color3.White();
      ground_material.lineColor = new BABYLON.Color3(0.7, 0.7, 0.7);
      ground_material.opacity = 0.3;
      //ground_material.freeze();
      //ground_material.isPickable = false;
      //ground_material.doNotSyncBoundingInfo = true;

      ground_material.diffuseColor = BABYLON.Color3.Blue();
      ground_material.majorUnitFrequency = 20;
      //ground_material.minorUnitFrequency = 5;
      ground_material.minorUnitVisibility = 0;
      ground.material = ground_material;

      //const gridTexture = createGridTexture();
      //const defaultMaterial = createMaterial(gridTexture);
      //ground.material = defaultMaterial;

      //uncomment the following line to make eviroment rotate.
      /* 
	engine.runRenderLoop(function () {
		camera.alpha += 0.004;
	});
  */
      return scene;
    }, //end create scence
  }, //end method.s
  mounted() {
    console.log("render mounted");
    //=========================================================================
    //set loading screen before create scene
    //=========================================================================
    //engine.displayLoadingUI();

    /******* Add the create scene function ******/

    /******* End of the create scene function ******/

    //try to create scence, and if error show alert
    try {
      if(this.pallet_mode){
        console.log("pallet_mode")
        this.scene=this.createSceneWithPallet();
      }else{
      this.scene = this.createScene(); //Call the createScene function
      //console.log("scene" + this.scene);
      }
    } catch (e) {
      console.log(e);
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Something went wrong! wiil jump to formsend page in 5sec",
        footer: "<p>Do you create the box and container information first?</p>",
      });
      setTimeout(() => {
        this.$router.push("../formsend");
      }, 5000);
    }
    this.$store.dispatch("setRenderLoadingStatus", false);
    // 最后一步调用engine的runRenderLoop方案，执行scene.render()，让我们的3d场景渲染起来
    this.engine.runRenderLoop(this.handleRenderLoop);
    // 监听浏览器改变大小的事件，通过调用engine.resize()来自适应窗口大小
    window.addEventListener("resize", this.handleChangeWindowSize);
  }, //end monted
};
</script>

<style scoped>
#renderCanvas {
  width: 100%;
  height: 100%;
  touch-action: none;
}
.overlay {
  opacity: 0.8;
  background-color: #ccc;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0px;
  left: 0px;
  z-index: 1000;
}

a {
  color: slategray;
  text-decoration: none;
}
a:hover {
  color: orange;
  text-decoration: none;
}
/*canvas { z-index: 0; position: absolute; width: 100%; height: 100%; outline: none; background: radial-gradient(circle, rgb(81, 90, 109) 0%, rgb(49, 53, 68) 100%); }*/
ul {
  background: #5f62702f;
  position: absolute;
  list-style-type: none;
}
ul li {
  background: #242b35;
  border: 1px solid #161a2096;
  border-radius: 5px;
  padding: 3px;
  text-align: center;
}
ul li:hover,
ul li.select,
ul li.toggle {
  background: orange;
  color: #222;
  cursor: pointer;
}
ul li.separator {
  background: none;
  height: 3px;
  padding: 0;
  cursor: default;
  border: none;
}
ul li.spacer {
  background: none;
  height: 3px;
  padding: 0;
  cursor: default;
  border: none;
}
input[type="color"] {
  width: 22px;
  height: 18px;
  border: none;
  background: #2e35414d;
  outline: none;
  border: none;
  border-radius: 50%;
  vertical-align: text-bottom;
}
input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}
input[type="color"]::-webkit-color-swatch {
  border: none;
  border-radius: 20%;
}
input[type="color"]:hover {
  background: white;
  cursor: pointer;
}
input[type="number"] {
  width: 50px;
  margin-bottom: 1px;
  background: #2a313db7;
  color: #808fa3;
  padding: 2px;
  font-size: 11px;
  text-indent: 5px;
  border: solid 1px #343c49;
  border-radius: 3px;
  text-align: left;
  outline: none;
}
input[type="number"]:hover {
  color: orange;
  border: solid 1px #43495a;
}
input[type="checkbox"] {
  display: none;
}
input[type="checkbox"] + .material-icons::after {
  content: "check_box_outline_blank";
  color: #475364;
}
input[type="checkbox"]:checked + .material-icons::after {
  content: "check_box";
  color: orange;
}
select {
  appearance: none;
  width: 18px;
  background-color: #2a313db7;
  color: #bbb;
  font-size: 14px;
  font-weight: bold;
  padding: 0;
  border: none;
  outline: none;
}
select:hover {
  color: orange;
  cursor: pointer;
}
option {
  font-size: 14px;
  font-weight: bold;
  color: #bbb;
  background-color: #252931;
}
button {
  width: 115px;
  background-color: #353f4d;
  color: #bbb;
  box-shadow: inset 1px 1px 1px #3f4a58, inset -1px -1px 1px #2f3742;
  border-radius: 4px;
  padding: 3px;
  font-size: 10px;
  border: 1px solid #161a20bd;
  outline: none;
}
button:hover {
  background-color: orange;
  color: #222;
  cursor: pointer;
}
label {
  color: #5c6c81;
  margin-right: 5px;
}
#menuH_L {
  background: none;
  left: 10px;
  top: 10px;
}
#menuH_L li {
  display: inline-block;
  width: 30px;
  padding: 1px;
  box-shadow: inset 1px 1px 1px #323b47, inset -1px -1px 1px #29303a;
}
#menuH_R {
  background: none;
  right: 10px;
  top: 10px;
  z-index: 999;
}
#menuH_R li {
  display: inline-block;
  width: 30px;
  padding: 1px;
  box-shadow: inset 1px 1px 1px #323b47, inset -1px -1px 1px #29303a;
}
#menuV {
  z-index: 1000;
  position: fixed;
  top: 0;
  right: 0;
  background: #222731f8;
  padding: 10px;
  width: 120px;
  height: 100%;
  transform: translate(200px, 0);
  transition: -webkit-transform 0.2s ease;
  overflow-y: scroll;
}
#menuV li {
  background: none;
  text-align: left;
  border: none;
  padding: 0;
  color: #67778d;
}
#menuV li:hover {
  background: none;
  color: orange;
}
#menuV .category {
  color: #464c5e;
  background: #1e222b;
  border: solid 1px #181c22;
  font-size: 10px;
  font-weight: bold;
  text-align: center;
  margin: 6px 4px 6px 0;
  padding: 2px;
}
#menuV .category:hover {
  color: #43495a;
  background: #1e222b;
  cursor: default;
}
#toolbar_R {
  width: 30px;
  right: 10px;
  top: 80px;
  padding: 3px;
  border-radius: 5px;
}
#toolbar_R li {
  margin-bottom: 2px;
  box-shadow: inset 1px 1px 1px #323b47, inset -1px -1px 1px #29303a;
}
#toolbar_R li.separator {
  box-shadow: none;
}
#toolbar_L {
  width: 30px;
  left: 10px;
  top: 80px;
  padding: 3px;
  border-radius: 5px;
}
#toolbar_L li {
  margin-bottom: 2px;
  box-shadow: inset 1px 1px 1px #323b47, inset -1px -1px 1px #29303a;
}
#toolbar_L li.separator {
  box-shadow: none;
}
#color_palette {
  left: 10px;
  top: 210px;
  padding: 3px;
  border-radius: 5px;
}
#color_palette li {
  width: 22px;
  height: 5px;
  margin-bottom: 1px;
}
#color_palette li:hover {
  border: solid 1px orange;
}
#hover {
  z-index: 1;
  background: none;
  left: 60%;
  top: 120px;
}
#hover li {
  box-shadow: inset 1px 1px 1px #37414e, inset -1px -1px 1px #2f3742;
}
#hover li:nth-child(1) {
  cursor: move;
  position: absolute;
  top: 0%;
  left: 0px;
}
#hover li:nth-child(2) {
  position: absolute;
  top: -33px;
  left: 0%;
}
#hover li:nth-child(3) {
  position: absolute;
  top: 0%;
  left: 30px;
}
#hover li:nth-child(4) {
  position: absolute;
  top: 0%;
  left: -30px;
}
#hover li:nth-child(5) {
  position: absolute;
  top: 33px;
  left: 0%;
}
#axisview {
  background: #161a203f;
  bottom: 5px;
  right: 6px;
  width: 68px;
  height: 68px;
  border: 1px solid #161a2096;
  border-radius: 50%;
  box-shadow: inset 1px 1px 1px #38404d, inset -1px -1px 1px #38404d;
}
#axisview li {
  border-radius: 50%;
  padding: 3px;
  color: #495363;
  border: 1px solid #161a2096;
}
#axisview li:nth-child(1) {
  position: absolute;
  top: -28%;
  right: 0%;
}
#axisview li:nth-child(2) {
  position: absolute;
  top: -36%;
  right: 44%;
}
#axisview li:nth-child(3) {
  position: absolute;
  top: -18%;
  right: 83%;
}
#axisview li:nth-child(4) {
  position: absolute;
  top: 22%;
  right: 103%;
}
#axisview li:nth-child(5) {
  position: absolute;
  top: 65%;
  right: 97%;
}
#loadingscreen {
  display: none;
  z-index: 1001;
  position: absolute;
  width: 100%;
  height: 100%;
  background: #000000bb;
}
#loadingscreen .spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -50px;
  margin-top: -50px;
  border-radius: 50%;
  background: #252e38;
  border: 2px solid #344558;
  animation: spin 3s infinite linear;
}
#notifier {
  opacity: 0;
  transition: opacity 0.5s;
  position: absolute;
  left: 50%;
  top: 50%;
  margin-left: -50px;
  margin-top: -20px;
  padding: 3px 5px 3px 5px;
  background: orange;
  color: #111;
  border: dashed 1px #d18800;
  font-size: 10px;
  font-weight: bold;
  border-radius: 5px;
}
#notifier.fade {
  opacity: 1;
}
#status {
  color: #ffffff30;
  position: absolute;
  bottom: 4px;
  left: 5px;
  font-size: 10px;
  font-weight: bold;
  opacity: 0.8;
}
#status span {
  color: #eee;
  padding: 0 1px 0 1px;
}
#status i {
  color: #aaa;
}
::-webkit-scrollbar {
  display: none;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.material-icons {
  font-size: 18px;
  pointer-events: none;
  vertical-align: middle;
  text-align: center;
}
</style>
