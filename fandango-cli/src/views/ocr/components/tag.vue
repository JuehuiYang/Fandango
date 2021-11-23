<template>
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

</template>

<style>
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

<script>
import axios from 'axios'

export default {
  name: 'TagForm',
  data() {
    return {
      dynamicTags: ['mit', 'free'],
      inputVisible: false,
      inputValue: ''
    }
  },
  methods: {
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

    submit: function() {
      const that = this
      this.$message('submit!')
      console.log('子组件')
      // const data = {
      //   'keyword': this.dynamicTags
      // }
      const data = {
        'keyword': ['we', 'free', 'mit']
      }
      console.log(data)
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
