import  * as BABYLON from  "@babylonjs/core";
var TestRender ={
  testTexture(scene){
  //another texture test
  var mat = new BABYLON.StandardMaterial("dog", scene);
  mat.diffuseTexture = new BABYLON.Texture("https://upload.wikimedia.org/wikipedia/commons/8/87/Alaskan_Malamute%2BBlank.png", scene);
  mat.diffuseTexture.hasAlpha = true;
  mat.backFaceCulling = false;
  var box = BABYLON.MeshBuilder.CreateBox("box", {}, scene);
  box.material = mat;
   },
//=======================================================
//Sky box test
//=======================================================
testSkyBox(scene){
	var skybox = BABYLON.MeshBuilder.CreateBox("skyBox", {size:1000.0}, scene);
	var skyboxMaterial = new BABYLON.StandardMaterial("skyBox", scene);
	skyboxMaterial.backFaceCulling = false;
	skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture("https://upload.wikimedia.org/wikipedia/commons/8/87/Alaskan_Malamute%2BBlank.png", scene);
	skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
	skyboxMaterial.diffuseColor = new BABYLON.Color3(0, 0, 0);
	skyboxMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
	skybox.material = skyboxMaterial;
}	
}

export default TestRender

