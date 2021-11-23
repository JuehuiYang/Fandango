<template>
  <div class="app-container">
    <!--    <el-card style="margin-top: 10px">-->
    <!--      <el-steps :active="active" simple>-->
    <!--        <el-step title="提交pdf" icon="el-icon-upload"/>-->
    <!--        <el-step title="设置关键词" icon="el-icon-upload"/>-->
    <!--        <el-step title="OCR识别" icon="el-icon-picture"/>-->
    <!--      </el-steps>-->
    <!--    </el-card>-->
    <el-card v-show="active === 0" style="margin-top: 10px;">
      <div style="display: flex;justify-content:center;align-items: center;">
        <upload />
      </div>
      <el-button style="margin-top: 10px;" @click="next">下一步</el-button>
    </el-card>
    <el-card v-show="active === 1" style="margin-top: 10px">

      <el-form ref="form" :model="form">
        <el-form-item label="设置关键词">
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
          <el-button type="primary" @click="tagSubmit">提交</el-button>
        </el-form-item>
      </el-form>
      <el-button style="margin-top: 10px;" @click="next">下一步</el-button>
      <el-button style="margin-top: 10px;" @click="active = 0">上一步</el-button>
    </el-card>
    <el-card v-show="active === 2" style="margin-top: 10px">
      <span>1. 结果展示</span>
      <el-divider />
      <span>2. 评分</span>
      <el-divider />
      <span>3. 关键词出现次数</span>
      <div>
        <el-table
          :data="tableData"
          style="width: 100%"
        >
          <el-table-column
            prop="key"
            label="关键词"
            width="180"
          />
          <el-table-column
            prop="count"
            label="出现次数"
            width="180"
          />
        </el-table>
      </div>
      <el-divider />
      <el-form ref="form" :model="form">
        <el-form-item>
          <el-button type="primary" @click="onDownload">获取识别结果</el-button>
        </el-form-item>
      </el-form>
      <el-button style="margin-top: 10px;" @click="active = 1">上一步</el-button>
      <el-button style="margin-top: 10px;" @click="active = 0">返回初始页面</el-button>
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

    onSubmit() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },

    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },

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

