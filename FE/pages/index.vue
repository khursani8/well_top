<template>
  <section class="container">
    <el-container>
      <el-main>
        <el-container direction="horizontal" height="30%" id="top">
          <el-container direction="vertical">
            <el-aside width="100%">
              <el-upload
                :on-change="handleChange"
                width="100%"
                ref="upload"
                class="upload-demo"
                action="https://jsonplaceholder.typicode.com/posts/"
                :auto-upload="false"
              >
                <el-button slot="trigger" size="small" type="primary">select file</el-button>
              </el-upload>
            </el-aside>
            <div class="well">
              <el-checkbox-group v-model="checkList" style="overflow-y:scroll">
                <el-container direction="vertical">
                  <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
                </el-container>
              </el-checkbox-group>
              <el-button type="primary">Generate Log</el-button>
            </div>
          </el-container>

          <el-aside width="60%" height="70%">
            <div id="gmap-container" height="400px"/>
          </el-aside>
        </el-container>

        <!-- testadadadsd -->
        <el-container direction="horizontal" style="text-align:center" id="bottom">
          <div width="100px" id="fullscreen">
            <el-checkbox v-model="checked">
              <input :disabled="!checked" placeholder="GR CUTOFF">
            </el-checkbox>
          </div>
          <el-main>Correlation Panel</el-main>
          <input id="button" type="button" value="FULL" @click="full">
        </el-container>
      </el-main>
    </el-container>
  </section>
</template>

<script>
const cityOptions = ['WellA', 'WellB', 'WellC', 'WellD']
export default {
  components: {},
  data() {
    return {
      fileList3: [],
      checked: false,
      checkList: [],
      checkAll: false,
      checkedCities: ['WellA', 'WellC'],
      cities: cityOptions,
      isIndeterminate: true,
      vueGMap: null,
      // Basically, making an anon function so that Vue
      // doesn't try to access google.maps until it's actually required
      globalOptions: () => ({
        zoom: 4,
        center: { lat: -33, lng: 151 },
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
          mapTypeIds: ['roadmap', 'terrain']
        }
      })
    }
  },
  mounted() {
    this.createGoogleMaps().then(
      this.initGoogleMaps,
      this.googleMapsFailedToLoad
    )
  },
  methods: {
    handleChange(file, fileList) {
      debugger
      this.fileList3 = fileList.slice(-3)
    },
    full() {
      const display = document.getElementById('top').style.display
      document.getElementById('top').style.display = display ? '' : 'none'
    },
    submitUpload() {
      this.$refs.upload.submit()
    },
    createGoogleMaps() {
      return new Promise((resolve, reject) => {
        const gmap = document.createElement('script')
        gmap.src =
          'https://maps.googleapis.com/maps/api/js?v=3&key=AIzaSyAKEWs3TBk8EYYsLw0ZcT8o0mqviF--vYw'
        gmap.type = 'text/javascript'
        gmap.onload = resolve
        gmap.onerror = reject
        document.body.appendChild(gmap)
      })
    },
    initGoogleMaps() {
      // You could do this as an easier alternative
      const localOptions = {
        zoom: 4,
        center: { lat: -33, lng: 151 },
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: () => window.google.maps.MapTypeControlStyle.DROPDOWN_MENU,
          mapTypeIds: ['roadmap', 'terrain']
        }
      }
      const gmap = document.getElementById('gmap-container')
      this.vueGMap = new google.maps.Map(gmap, this.globalOptions())
      gmap.style.height = '500px'
      console.log(this.vueGMap)
    },
    googleMapsFailedToLoad() {
      this.vueGMap = 'Error occurred'
    },
    handleCheckAllChange(val) {
      this.checkedCities = val ? cityOptions : []
      this.isIndeterminate = false
    },
    handleCheckedCitiesChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.cities.length
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.cities.length
    }
  }
}
</script>

<style>
#fullscreen {
  position: relative;
  top: 0;
  left: 0;
}
div.el-upload el-upload--text {
  height: 30px !important;
}
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  /* align-items: center; */
  text-align: center;
}
.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

label.el-checkbox {
  height: 40px !important;
}
.well {
  height: 300px !important;
}
</style>
