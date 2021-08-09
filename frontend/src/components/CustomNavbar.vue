  <template>
  <nav
    class="
      navbar navbar-expand-lg navbar-dark
      bg-dark
      d-flex
      justify-content-between
    "
  >
    <router-link class="navbar-brand" to="/">3D-Bin Packing</router-link> |
    <router-link class="navbar-brand" to="/">Home</router-link> |
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="navbar-brand" to="/render">Render</router-link>
        </li>
        <li class="nav-item">
          <router-link class="navbar-brand" to="/formsend">FormSend</router-link>
        </li>

        <li class="nav-item">
          <router-link class="navbar-brand" to="/about">About</router-link>
        </li>
      </ul>
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
    </div>
  </nav>
</template>
<script>

export default {
  name: 'CustomNavbar',
  components: {
  }
}
</script>
