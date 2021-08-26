<template>
<div  class="w-100 p-3">
  <canvas id="renderCanvas"></canvas>
</div>
</template>


<script>
import * as BABYLON from "@babylonjs/core";
//import { AdvancedDynamicTexture } from "@babylonjs/gui";
//import { Button } from "@babylonjs/gui";
//import Swal from "sweetalert2";
import { GridMaterial } from "@babylonjs/materials/grid";
import "babylonjs-materials";
// Required side effects to populate the Create methods on the mesh class. Without this, the bundle would be smaller but the createXXX methods from mesh would not be accessible.
import "@babylonjs/core/Meshes/meshBuilder";
import { mapState } from "vuex";

//import my render javascript functions.
//import TestRender from "@/Render_functions/TestRender";



export default {
  name: "Render",
  components: {},
  //========================================
  //Computed:
  //Description: Initialize the variable
  //========================================
  computed: mapState({
    container_infos: (state) => state.container_infos,
    box_infos: (state) => state.box_infos,
    render_infos:(state)=>state.render_infos
  }),

  mounted() {

    var canvas = document.getElementById("renderCanvas"); // 得到canvas对象的引用
    var engine = new BABYLON.Engine(canvas, true); // 初始化 BABYLON 3D engine
    /******* Add the create scene function ******/
    var createScene = function (render_infos) {
      //create scene
      var scene = new BABYLON.Scene(engine);
      //=========uncomment the following line to set debug mode=======*/
      //scene.debugLayer.show();

      //======================starting create elements=======================
      
      
      
      //global variable
      var ground_size=500;
      var total_container_number=render_infos['containers'].length
      //var container_margin=10




      console.log("render_infos['containers'].lenght:"+total_container_number)

    //draw containers
    //random color function color(0~1)
      function getRandomColor(min, max) {
        let r=1;
        let g=1;
        let b=1;
          r=Math.random() * (max - min) + min;
          g=Math.random() * (max - min) + min;
          b=Math.random() * (max - min) + min;
          return new BABYLON.Color3(r,g,b);
      }
      
      

    //===================================================== 
    //create material array for containers
    //=====================================================
      var container_mat_array=[];
      for(let i=0; i<render_infos['total_container_types'];i++){
        let container_mat_name=render_infos['containers'][i]['TypeName']+"mat"
        let mat=  new BABYLON.StandardMaterial(container_mat_name, scene)
        mat.diffuseColor =getRandomColor(0.6,1)
        mat.alpha = 0.5;
        container_mat_array.push(mat)
      }
    //=======================================================
    //create container array
    //=======================================================
     var containers_mesh_array=[];
     for(let i=0; i<render_infos['containers'].length;i++){
       console.log(render_infos['containers'][i]['ID'])
      let container_mesh_name=render_infos['containers'][i]['ID']
      let cont=( BABYLON.MeshBuilder.CreateBox(container_mesh_name, {
        height: render_infos['containers'][i]['X'],
        width: render_infos['containers'][i]['Y'],
        depth: render_infos['containers'][i]['Z'],
      }));

      cont.material=container_mat_array[render_infos['containers'][i]['TypeIndex']]
      containers_mesh_array.push(cont);
     }
      console.log(containers_mesh_array)
      
    //move the position for each container

    
    //=========================================================
    //Move the first container to 0,0,0 and set its position as reference
    //=========================================================
     //move the container to the ground
    containers_mesh_array[0].position.y+=(render_infos['containers'][0]['Y'])/2;
    //move the container[0] align to 0,0,0
    containers_mesh_array[0].position.z+=(render_infos['containers'][0]['Z'])/2;
    containers_mesh_array[0].position.x+=(render_infos['containers'][0]['X'])/2;

    //move other containers if exsist
    for(let i=1; i<total_container_number;i++){
      //move the container to the ground
        containers_mesh_array[i].position.y+=(render_infos['containers'][i]['Y'])/2;
        //move the container[0] align to 0,0,0
        containers_mesh_array[i].position.z+=(render_infos['containers'][i]['Z'])/2;
        containers_mesh_array[i].position.x+=containers_mesh_array[i-1].position.x+30+render_infos['containers'][i]['X']/2+render_infos['containers'][i-1]['X']/2
    }


      //========================================================================
      //Calculate the upper left corner position on x-z plane for each container
      //========================================================================
      var left_top_positions_array=[]
      for(let i=0; i<=render_infos['total_container_number'];i++){
      var origin_coordinate_x = containers_mesh_array[i].position.x - render_infos['containers'][i]['X'] / 2;
      var origin_coordinate_y=containers_mesh_array[i].position.y;
      var origin_coordinate_z =containers_mesh_array[i].position.z;
      left_top_positions_array.push({"X":origin_coordinate_x,"Y":origin_coordinate_y, "Z":origin_coordinate_z})
      console.log("left_top")
      console.log(left_top_positions_array)
      }
    //===================================================== 
    //create material array for boxes
    //=====================================================
      var box_mat_array=[];
      for(let i=0; i<render_infos['total_box_types'];i++){
        let box_mat_name="boxmat"+i
        let mat=  new BABYLON.StandardMaterial(box_mat_name, scene)
        mat.diffuseColor =getRandomColor(0.3,1)
        mat.alpha = 0.5;
        box_mat_array.push(mat)
      }

      //=========================================================================
      //create the fitted boxes for each container      
      //=========================================================================
      var box_mesh_array=[] 
      for(const [index_of_container, container] of render_infos["containers"].entries()){
        console.log(container['Fitted_items'].length)
        for(let i=0; i<container['Fitted_items'].length;i++){
          let box_x=container["Fitted_items"][i]["X"]
          let box_y=container["Fitted_items"][i]["Y"]
          let box_z=container["Fitted_items"][i]["Z"]
          let box_mesh_name=container["Fitted_items"][i]['ID']
          let box_instance=( BABYLON.MeshBuilder.CreateBox(box_mesh_name, {
              height: box_x,
              width: box_y,
              depth: box_z,
        }));
            box_instance.material=box_mat_array[container["Fitted_items"][i]["TypeIndex"]]
            console.log(left_top_positions_array)
            box_instance.position.x=(left_top_positions_array[index_of_container])['X']+container['Fitted_items']['position_x']
            box_instance.position.y=(left_top_positions_array[index_of_container])['Y']+container['Fitted_items']['position_y']
            box_instance.position.z=(left_top_positions_array[index_of_container])['Z']+container['Fitted_items']['position_z']
            box_mesh_array.push(box_instance)
       }//end inner for
     }//end outter for








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
        new BABYLON.Vector3(0, 150, 0),
        scene
      );
      // eslint-disable-next-line no-unused-vars
      var light2 = new BABYLON.PointLight(
        "light2",
        new BABYLON.Vector3(2, 150, -1),
        scene
      );
      
      // Create my custom ground
      var ground = BABYLON.MeshBuilder.CreateGround("ground1", {
        height: ground_size,
        width: ground_size,
        subdivisions: 4,
      });

      //Attach grid material to the ground
      var ground_material = new GridMaterial("grid", scene);
      ground_material.diffuseColor = BABYLON.Color3.Blue();
      ground_material.majorUnitFrequency = 20;
      ground_material.minorUnitVisibility = 0;
      ground.material = ground_material;


      //uncomment the following line to make eviroment rotate.
  /* 
	engine.runRenderLoop(function () {
		camera.alpha += 0.004;
	});
  */
      return scene;
    };
    /******* End of the create scene function ******/
    var scene = createScene(this.render_infos); //Call the createScene function
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
