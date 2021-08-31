Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@N0nent1ty 
N0nent1ty
/
3D-Binpacking-GUI
1
00
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
3D-Binpacking-GUI/frontend/src/views/LoadingPage.vue
@littletrojan
littletrojan add loading page, fix frontend UI
Latest commit 0f63ae8 3 days ago
 History
 1 contributor
425 lines (369 sloc)  7.29 KB
  
<template>
<div class="root">
<div class="mycontainer">

<!-- GRADIENT SPINNER 
<div class="spinner-box">
  <div class="circle-border">
    <div class="circle-core"></div>
  </div>  
</div>
-->

<!-- SPINNER ORBITS 
<div class="spinner-box">
  <div class="blue-orbit leo">
  </div>
  <div class="green-orbit leo">
  </div>
  
  <div class="red-orbit leo">
  </div>
  
  <div class="white-orbit w1 leo">
  </div><div class="white-orbit w2 leo">
  </div><div class="white-orbit w3 leo">
  </div>
</div>
-->
<!-- GRADIENT CIRCLE PLANES 
<div class="spinner-box">
  <div class="leo-border-1">
    <div class="leo-core-1"></div>
  </div> 
  <div class="leo-border-2">
    <div class="leo-core-2"></div>
  </div> 
</div>
-->
<!-- SPINNING SQUARES 
<div class="spinner-box">
  <div class="configure-border-1">  
    <div class="configure-core"></div>
  </div>  
  <div class="configure-border-2">
    <div class="configure-core"></div>
  </div> 
</div>
-->
<!-- LOADING DOTS... -->
<div class="spinner-box">
  <div class="pulse-container">  
    <div class="pulse-bubble pulse-bubble-1"></div>
    <div class="pulse-bubble pulse-bubble-2"></div>
    <div class="pulse-bubble pulse-bubble-3"></div>
  </div>
</div>


<!-- SOLAR SYSTEM 
<div class="spinner-box">
  <div class="solar-system">
    <div class="earth-orbit orbit">
      <div class="planet earth"></div>
      <div class="venus-orbit orbit">
        <div class="planet venus"></div>
        <div class="mercury-orbit orbit">
          <div class="planet mercury"></div>
          <div class="sun"></div>
        </div>
      </div>
    </div>
  </div>
</div>
-->

<!-- Three Quarter Spinner 
<div class="spinner-box">
  <div class="three-quarter-spinner"></div>
</div>
--><div>
	<p class="p3">Your browser is rendering your request, please be patient.</p>
    </div>
</div>

</div>
</template>





<style>
.p3 {
  font-family: "Lucida Console", "Courier New", monospace ;
  margin-top:10%;
}

@keyframes pulse {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: .25;
    transform: scale(.75);
  }
}
/* GRID STYLING */
* {
  box-sizing: border-box;
}
.root{
    height:100%;
    width:100%;
}
.mycontainer {
  min-height: 100vh;
  background-image: linear-gradient(100deg, #d2dff1 0%, #80acf3 40%  70%);;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* PULSE BUBBLES */
.pulse-container {
  width: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pulse-bubble {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #2c073d;
}
.pulse-bubble-1 {
    animation: pulse .4s ease 0s infinite alternate;
}
.pulse-bubble-2 {
    animation: pulse .4s ease .2s infinite alternate;
}
.pulse-bubble-3 {
    animation: pulse .4s ease .4s infinite alternate;
}

</style>
