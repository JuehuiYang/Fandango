<template>
  <div class="app-container">
    <el-card v-show="active === 0" style="margin-top: 10px;">
      <div style="display: flex;justify-content:center;align-items: center;">
        <upload/>
      </div>
      <el-button style="margin-top: 10px;" @click="next">next step</el-button>
    </el-card>
    <el-card v-show="active === 1" style="margin-top: 10px">

      <el-form ref="form" :model="form">
        <el-form-item label="Set keywords">
          <div class="tag-form">
            <el-tag
              v-for="tag in dynamicTags"
              :key="tag"
              closable
              :disable-transitions="false"
              @close="handleClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="inputVisible"
              ref="saveTagInput"
              v-model="inputValue"
              class="input-new-tag"
              size="small"
              @keyup.enter.native="handleInputConfirm"
              @blur="handleInputConfirm"
            />
            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="tagSubmit">submit</el-button>
        </el-form-item>
      </el-form>
      <el-button style="margin-top: 10px;" @click="active = 0">previous step</el-button>
      <el-button style="margin-top: 10px;" @click="next">next step</el-button>
    </el-card>
    <el-card v-show="active === 2" style="margin-top: 10px">
      <span>score</span>
      <el-rate
        v-model="value"
        disabled
        show-score
        text-color="#ff9900"
        score-template="{value}"
      >
      </el-rate>
      <el-divider/>
      <span>Keyword occurrences</span>
      <div>
        <el-table
          :data="tableData"
          style="width: 100%"
        >
          <el-table-column
            prop="key"
            label="keyword"
            width="180"
          />
          <el-table-column
            prop="count"
            label="count"
            width="180"
          />
        </el-table>
      </div>
      <el-divider/>
      <el-form ref="form" :model="form">
        <el-form-item>
          <el-button type="primary" @click="onDownload">result</el-button>
        </el-form-item>
      </el-form>
      <el-button style="margin-top: 10px;" @click="active = 1">previous step</el-button>
      <el-button style="margin-top: 10px;" @click="active = 0">back</el-button>
    </el-card>
  </div>
</template>

<script>
import Upload from '@/views/ocr/components/upload'
import axios from 'axios'

export default {
  components: {
    Upload
  },
  data() {
    return {
      dynamicTags: ['we', 'think', 'MIT'],
      inputVisible: false,
      inputValue: '',
      active: 0,
      value: 3.7,
      form: {
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      tableData: [{
        key: 'we',
        count: 1
      }]
    }
  },
  methods: {
    onDownload() {
      this.$message('download!')
      axios({
        method: 'GET', // 如果是get方法，则写“GET”
        url: '/api/result/',
        responseType: 'blob'
      }).then(res => {
        const blob = new Blob([res.data], {
          type: 'application/zip'
        })

        const eLink = document.createElement('a')
        eLink.download = 'result.zip'
        eLink.style.display = 'none'
        eLink.href = URL.createObjectURL(blob)
        document.body.appendChild(eLink)
        eLink.click()
        URL.revokeObjectURL(eLink.href)
        document.body.removeChild(eLink)
      })
    },

    next() {
      console.log(this.active)
      if (this.active++ > 2) this.active = 0
      console.log(this.active)
    },

    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },

    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },

    handleInputConfirm() {
      const inputValue = this.inputValue
      if (inputValue) {
        this.dynamicTags.push(inputValue)
      }
      this.inputVisible = false
      this.inputValue = ''
    },

    tagSubmit() {
      const self = this
      const formData = new FormData()
      formData.append('keyword', JSON.stringify(this.dynamicTags))
      axios({
        headers: {
          'Content-Type': 'application/json'
        },
        url: '/api/frequency/',
        method: 'post',
        withCredentials: true,
        data: formData
      }).then(function(response) {
        console.log(response)
        console.log(response.data.items)
        self.tableData = response.data.items
      })
    },

    getScore() {
      console.log('3.7')
    }
  }
}
</script>

<style scoped>
.box {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  margin-top: 10px;
  min-height: 500px;
  min-width: 100%;
}

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>

