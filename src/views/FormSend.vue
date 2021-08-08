<template>
<div><!--root div -->
  <div class="container ">
      <button class="btn btn-success mt-5 mb-5 float-start">
          New Employee
    </button>
  </div>
  <div class="d-flex justify-content-center "><!--card container make element in center-->
  <div class="card">
      <div class="card-body ">
          <span class="float-end" style="cursor:pointer">
              x
          </span>
          <h4 class="card-title">Add employee </h4>
          <div class="employee-form">
              <input type="text" class="form-control mb-2" placeholder="Name">
              <input type="text" class="form-control mb-2" placeholder="Job">
              <textarea cols="30" rows="10"></textarea>
          </div>
      </div><!-- end card body-->
  </div><!-- end card  -->
  </div><!--end card container-->
</div><!--end root element -->
</template>

<script>
  export default {
    data() {
      return {
      }
    }
  }
</script>