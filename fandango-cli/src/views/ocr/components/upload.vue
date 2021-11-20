<template>
  <el-upload
    class="upload-demo"
    drag
    action=""
    multiple
    show-file-list
    :http-request="upload"
  >
    <i class="el-icon-upload" />
    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    <div slot="tip" class="el-upload__tip">只能上传pdf文件，且不超过2M</div>
  </el-upload>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Upload',
  data() {
    return {
      fileList: [{
        name: 'food.jpeg',
        url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
      }, {
        name: 'food2.jpeg',
        url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
      }]
    }
  },
  methods: {
    addPipeline() {
      const that = this
      const data = {
        // 必选参数
        PipelineName: this.modalValue.PipelineName,
        PipelineNamespace: this.modalValue.PipelineNamespace,
        // 可选参数
        PipelineDescription: this.modalValue.PipelineDescription,
        PipelineGlobalParams: this.modalValue.PipelineGlobalParams
      }
      if (this.checkPipelineModalData() === true) {
        axios({
          headers: {
            'Content-Type': 'application/json'
          },
          url: this.GLOBAL.dataUrl + `pipelines`,
          method: 'post',
          withCredentials: true,
          data: data
        }).then(function (response) {
          console.log(response)
          if (response['status'] === 200) {
            that.addPipelineModal = false
            that.$Modal.success({
              title: '成功',
              content: '添加流水线成功！'
            })
            // 重新加载数据源
            that.getPipeline()
          } else {
            that.$Modal.error({
              title: '失败',
              content: '服务器端出错，请检查！'
            })
          }
        })
        this.modalValue.add = false
      }
    },

    upload(param) {
      const that = this
      const formData = new FormData()
      formData.append('file', param.file)
      axios({
        headers: {
          'Content-Type': 'application/json'
        },
        url: '/api/file_upload/',
        method: 'post',
        withCredentials: true,
        data: formData
      }).then(function(response) {
        console.log(response)
        if (response['status'] === 200) {
          that.addPipelineModal = false
          that.$Modal.success({
            title: '成功',
            content: '添加流水线成功！'
          })
        } else {
          that.$Modal.error({
            title: '失败',
            content: '服务器端出错，请检查！'
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
