  <template>
  <nav
    class="
      navbar navbar-expand-lg navbar-dark
      bg-dark
      d-flex
      justify-content-between
      sticky-top
      p-3
      fixed-top
    "
  >
    <router-link class="navbar-brand" to="/">3D-Bin Packing</router-link> |
    <router-link class="navbar-brand" to="/">Home</router-link> |
    <router-link class="navbar-brand" to="/formsend">FormSend</router-link>
    <router-link class="navbar-brand" to="/render">Render</router-link>
    <router-link class="navbar-brand" to="/about">About</router-link>
   
      <form class="form-inline my-2 my-lg-0 d-flex">
        <input
          class="form-control mr-sm-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
        />
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
          Search
        </button>
      </form>
  </nav>
</template>
<script>

export default {
  name: 'CustomNavbar',
  components: {
  }
}
</script>
<style>
</style>