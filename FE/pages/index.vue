<template>
  <section class="container">
    <el-container direction="vertical">
      <div>
        <h4>Automatic Selection Top Formation Module</h4>
        <img src="~/assets/logo2.png" width="150px" height="40px">
      </div>
      <el-main>
        <el-container direction="horizontal" height="29%" id="top">
          <el-container direction="vertical">
            <el-aside width="100%">
              <el-upload
                :on-change="handleChange"
                width="100%"
                ref="upload"
                class="upload-demo"
                action="https://jsonplaceholder.typicode.com/posts/"
                :auto-upload="false"
                multiple
              >
                <el-button slot="trigger" size="small" type="primary">select file</el-button>
              </el-upload>
            </el-aside>
            <div class="well">
              <el-checkbox-group v-model="checkList" style="overflow-y:scroll">
                <el-container direction="vertical">
                  <el-checkbox
                    v-for="city in wellNames"
                    :label="city"
                    :key="triggerReRender+city"
                  >{{city}}</el-checkbox>
                </el-container>
              </el-checkbox-group>
              <el-button type="primary" @click="generate">Generate Log</el-button>
            </div>
          </el-container>

          <el-aside width="80%" height="70%">
            <div id="gmap-container" height="710px"/>
          </el-aside>
        </el-container>

        <!-- testadadadsd -->
        <el-container direction="horizontal" style="text-align:center" id="bottom">
          <div width="100px" id="fullscreen">
            <el-tooltip
              class="item"
              effect="dark"
              content="Gamma Ray Cut off"
              placement="top-start"
            >
              <el-checkbox v-model="checked">
                <el-input-number
                  size="mini"
                  v-model="cutOff"
                  @change="handleChange"
                  :min="0"
                  :max="200"
                ></el-input-number>
                <!-- <input :disabled="!checked" placeholder="GR CUTOFF" v-model="cutOff"> -->
              </el-checkbox>
            </el-tooltip>
          </div>
          <el-main id="correlation">Correlation Panel</el-main>
          <input id="button" type="button" value="FULL" @click="full">
        </el-container>
      </el-main>
    </el-container>
  </section>
</template>

<script>
import Papa from 'papaparse'
export default {
  components: {},
  data() {
    return {
      cutOff: 120,
      triggerReRender: Math.random(),
      files: [],
      wellNames: [],
      fileList3: [],
      checked: false,
      checkList: [],
      checkAll: false,
      checkedCities: [],
      isIndeterminate: true,
      vueGMap: null,
      // Basically, making an anon function so that Vue
      // doesn't try to access google.maps until it's actually required
      globalOptions: () => ({
        zoom: 15,
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
    generate() {
      const payload = {
        files: this.files.filter(el => this.checkList.includes(el.well)),
        GR_CUTOFF: this.GR_CUTOFF
      }
      this.$axios.post('/endpoint', payload)
      debugger
    },
    handleChange(file, fileList) {
      const f = file.raw
      const that = this
      Papa.parse(f, {
        header: true,
        complete: function(results) {
          setTimeout(() => {
            const { lat, lon, well } = results.data[0]
            const myLatlng = { lat: +lat, lng: +lon }
            if (that.wellNames.length === 0) {
              const gmap = document.getElementById('gmap-container')
              const test = that.globalOptions()
              test.center = myLatlng
              that.vueGMap = new google.maps.Map(gmap, test)
              that.wellNames = []
            }
            that.wellNames.push(well)
            // console.log('before', that.triggerReRender)
            // that.triggerReRender = Math.random()
            // console.log('after', that.triggerReRender)
            // console.log('well', that.wellNames)
            console.log(lat, lon, well)
            // const test = new google.maps.Marker({
            //   // position: { lat: -33, lng: 151 },
            //   position: myLatlng,
            //   map: that.vueGMap,
            //   title: 'Hello World!'
            // })
            const marker = new google.maps.Marker({
              position: myLatlng,
              title: well
            })

            // To add the marker to the map, call setMap();
            marker.setMap(that.vueGMap)
            that.files.push({ well, file: results.data })
          }, 0)
        }
      })
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
      const myLatlng = { lat: -33, lng: 151 }
      // const localOptions = {
      //   zoom: 15,
      //   center: myLatlng,
      //   mapTypeControl: true,
      //   mapTypeControlOptions: {
      //     style: () => window.google.maps.MapTypeControlStyle.DROPDOWN_MENU,
      //     mapTypeIds: ['roadmap', 'terrain']
      //   }
      // }
      const gmap = document.getElementById('gmap-container')
      this.vueGMap = new google.maps.Map(gmap, this.globalOptions())
      gmap.style.height = '710px'
      console.log(this.vueGMap)
    },
    googleMapsFailedToLoad() {
      this.vueGMap = 'Error occurred'
    }
  }
}
</script>

<style>
div.el-checkbox-group {
  height: 200px;
}
.el-upload-list.el-upload-list--text {
  height: 200px;
}
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

#bottom {
  background-color: #d1dce6;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

#correlation {
  background-color: #d1dce6;
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
