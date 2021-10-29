<template>
  <div class="components-container">
    <split-pane split="vertical" @resize="resize">
      <template slot="paneR">
        <div class="right-container">
          <div>给出评分和标注过的pdf文件</div>
        </div>
      </template>
      <template slot="paneL">
        <div class="left-container">
          <div>提交pdf文件，设置关键词</div>
        </div>
      </template>
    </split-pane>
  </div>
</template>

<script>
import splitPane from 'vue-splitpane'

export default {
  name: 'OcrSplineDemo',
  components: { splitPane },
  methods: {
    resize() {
      console.log('resize')
    }
  }
}
</script>

<style scoped>
.components-container {
  position: relative;
  height: 100vh;
}

.left-container {
  background-color: #F38181;
  height: 100%;
}

.right-container {
  background-color: #FCE38A;
  height: 100%;
}

.top-container {
  background-color: #FCE38A;
  width: 100%;
  height: 100%;
}

.bottom-container {
  width: 100%;
  background-color: #95E1D3;
  height: 100%;
}

</style>
