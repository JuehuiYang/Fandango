<template>
  <div class="app-container">
    <el-card style="margin-top: 10px">
      <el-steps :active="active" simple>
        <el-step title="设置关键词" icon="shezhi1" />
        <el-step title="提交pdf" icon="el-icon-upload" />
        <el-step title="OCR识别" icon="el-icon-picture" />
      </el-steps>
      <el-button style="margin-top: 10px;" @click="next">下一步</el-button>
    </el-card>
    <el-card v-show="active === 0" style="margin-top: 10px">
      <el-form ref="form" :model="form">
        <el-form-item label="设置关键词">
          <tag-form />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交</el-button>
          <el-button @click="onCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card v-show="active === 1" class="box">
      <upload />
    </el-card>
    <el-card v-show="active === 2" style="margin-top: 10px">
      <p>展示OCR进度</p>
      <el-progress :text-inside="true" :stroke-width="26" :percentage="70" />
      <el-progress :text-inside="true" :stroke-width="24" :percentage="100" status="success" />
      <el-progress :text-inside="true" :stroke-width="22" :percentage="80" status="warning" />
      <el-progress :text-inside="true" :stroke-width="20" :percentage="50" status="exception" />
    </el-card>
    <el-card v-show="active === 3" style="margin-top: 10px">
      <span>1. 结果展示</span>
      <el-divider />
      <span>2. 评分</span>
      <el-divider />
      <span>3. 关键词出现次数</span>
      <el-divider />
      <el-form ref="form" :model="form">
        <el-form-item>
          <el-button type="primary" @click="onSubmit">获取识别结果-PDF</el-button>
          <el-button type="primary" @click="onSubmit">获取识别结果-TXT</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import TagForm from '@/views/ocr/components/tag'
import Upload from '@/views/ocr/components/upload'

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
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
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
  align-items: center;     /* 垂直居中 */
  margin-top: 10px;
  min-height: 500px;
  min-width: 100%;
}
</style>

