<template>
  <div class="app-container">
    <el-card style="margin-top: 10px">
      <el-steps :active="active" simple>
        <el-step title="设置关键词" icon="shezhi1"/>
        <el-step title="提交pdf" icon="el-icon-upload"/>
        <el-step title="OCR识别" icon="el-icon-picture"/>
      </el-steps>
      <el-button style="margin-top: 10px;" @click="next">下一步</el-button>
    </el-card>
    <el-card v-show="active === 0" style="margin-top: 10px">
      <el-form ref="form" :model="form">
        <el-form-item label="设置关键词">
          <tag-form/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="keywordSubmit">提交</el-button>
          <el-button @click="onCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card v-show="active === 1" class="box">
      <upload/>
    </el-card>
    <el-card v-show="active === 2" style="margin-top: 10px">
      <p>展示OCR进度</p>
      <el-progress :text-inside="true" :stroke-width="26" :percentage="70"/>
      <el-progress :text-inside="true" :stroke-width="24" :percentage="100" status="success"/>
      <el-progress :text-inside="true" :stroke-width="22" :percentage="80" status="warning"/>
      <el-progress :text-inside="true" :stroke-width="20" :percentage="50" status="exception"/>
    </el-card>
    <el-card v-show="active === 3" style="margin-top: 10px">
      <span>1. 结果展示</span>
      <el-divider/>
      <span>2. 评分</span>
      <el-divider/>
      <span>3. 关键词出现次数</span>
      <el-divider/>
      <el-form ref="form" :model="form">
        <el-form-item>
          <el-button type="primary" @click="onDownload">获取识别结果</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import TagForm from '@/views/ocr/components/tag'
import Upload from '@/views/ocr/components/upload'
import axios from 'axios'

export default {
  components: {
    TagForm,
    Upload
  },
  data() {
    return {
      active: 0,
      value: 3.7,
      form: {
        keyword: [],
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      keyword: ['we', 'think', 'MIT']
    }
  },
  methods: {
    /**
     * 提交关键词
     */
    keywordSubmit() {
      this.$message('submit!')
      const that = this
      const data = {
        keyword: this.keyword
      }
      axios({
        headers: {
          'Content-Type': 'application/json'
        },
        url: '/api/keyword/',
        method: 'post',
        withCredentials: true,
        data: data
      }).then(function(response) {
        console.log(response)
        if (response['status'] === 200) {
          that.$Modal.success({
            title: '成功',
            content: '添加模组成功！'
          })
        } else {
          that.$Modal.error({
            title: '失败',
            content: '服务器端出错，请检查！'
          })
        }
      })
    },

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
</style>

