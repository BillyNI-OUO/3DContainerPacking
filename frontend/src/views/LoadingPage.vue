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
@keyframes spin {
  from {
    transform: rotate(0);
  }
  to{
    transform: rotate(359deg);
  }
}

</style>