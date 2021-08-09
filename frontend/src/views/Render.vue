<template>
  <canvas id="renderCanvas"></canvas>
</template>


<script>
import  * as BABYLON from  "@babylonjs/core";
import {
    GridMaterial
} from "@babylonjs/materials/grid";
import 'babylonjs-materials'
// Required side effects to populate the Create methods on the mesh class. Without this, the bundle would be smaller but the createXXX methods from mesh would not be accessible.
import "@babylonjs/core/Meshes/meshBuilder";




export default {
  name: 'Render',
  components: {
  },
  mounted() {
    var canvas = document.getElementById("renderCanvas"); // 得到canvas对象的引用
    var engine = new BABYLON.Engine(canvas, true); // 初始化 BABYLON 3D engine
    /******* Add the create scene function ******/
    var createScene = function () {
      // 创建一个场景scene
    var scene = new BABYLON.Scene(engine);

          // 添加一个相机，并绑定鼠标事件
const camera = new BABYLON.ArcRotateCamera(
  "camera",
   -Math.PI / 2,
    Math.PI / 2.5, 3,
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
    let container_width=10;
    let container_height=10;
    let container_deepth=20; 
    const container = BABYLON.MeshBuilder.CreateBox("container", 
    {height: container_height,
     width: container_width,
      depth: container_deepth});
    //Create the container material
    var mat_for_container = new BABYLON.StandardMaterial("mat", scene);
    mat_for_container.diffuseColor = BABYLON.Color3.White();
    mat_for_container.alpha = 0.5;
    //Attach material to the container
    container.material=mat_for_container;
    
    //set the position y of container so that it can stand on the "ground"
    container.position.y+=container_height/2;

    //===================================================
    //Create the box
    //===================================================
    let box1_width=2;
    let box1_height=2;
    let box1_deepth=2;

    const box1=BABYLON.MeshBuilder.CreateBox("box1",
    {height: box1_height,
    width: box1_width,
    depth: box1_deepth}
    );

    //Create the box1 material
    var mat_for_box1 = new BABYLON.StandardMaterial("matbox1", scene);
    mat_for_box1.diffuseColor = BABYLON.Color3.Blue();
    mat_for_box1.alpha = 0.5;
    //Attach material to the box1
    box1.material=mat_for_box1;

    //set the position y of container so that it can stand on the "ground"
    box1.position.y+=box1_height/2;
    //move the position x
    box1.position.x+=box1_width;

    //====================================================
    //Create the box1 clone
    //====================================================
    let boxes_array=[];
    let number_of_boxes=5;
    var iter;
    let initial_x_position=2;
    for(iter=0;iter!=number_of_boxes;iter++){
      let box_name="box_"+iter//box_0, box_1, box_2 ...
      console.log("box_name:"+box_name);
      boxes_array.push(BABYLON.MeshBuilder.CreateBox(box_name,
    {height: box1_height,
    width: box1_width,
    depth: box1_deepth}
      ));
      boxes_array[iter].material=mat_for_box1;
      boxes_array[iter].position.y+=box1_height/2;
      boxes_array[iter].position.x+=box1_width*(iter+1)+initial_x_position;
    }//end for loop

    // Create ground
    var ground = BABYLON.MeshBuilder.CreateGround("ground1", {height: 100, width: 100, subdivisions: 4});
    //Attach grid material to the ground
    var material = new GridMaterial("grid", scene);
    ground.material=material;
	
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
}//end monted
}
</script>

<style>
#renderCanvas {
  width: 100%;
  height: 100%;
  touch-action: none;
}
</style>
