import  * as BABYLON from  "@babylonjs/core";
const CustomLoadingScreen=function(){
    BABYLON.DefaultLoadingScreen.prototype.displayLoadingUI = function () {
        if (document.getElementById("customLoadingScreenDiv")) {
            // Do not add a loading screen if there is already one
            document.getElementById("customLoadingScreenDiv").style.display = "initial";
            return;
        }
        this._loadingDiv = document.createElement("div");
        this._loadingDiv.id = "customLoadingScreenDiv";
        this._loadingDiv.innerHTML = "scene is currently loading";
        var customLoadingScreenCss = document.createElement('style');
        customLoadingScreenCss.type = 'text/css';
        customLoadingScreenCss.innerHTML = `
        #customLoadingScreenDiv{
            background-color: #BB464Bcc;
            color: white;
            font-size:50px;
            text-align:center;
        }
        `;
        document.getElementsByTagName('head')[0].appendChild(customLoadingScreenCss);
        this._resizeLoadingUI();
        window.addEventListener("resize", this._resizeLoadingUI);
        document.body.appendChild(this._loadingDiv);
    };
    
    BABYLON.DefaultLoadingScreen.prototype.hideLoadingUI = function(){
        document.getElementById("customLoadingScreenDiv").style.display = "none";
        console.log("scene is now loaded");
    }
}
export default CustomLoadingScreen;