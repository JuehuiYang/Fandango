<template>
  <div class="root-container">
    <div class="root-text">Fandango</div>
    <el-divider></el-divider>
    <span>Fandango is an Online OCR service that allows you to extract text from PDF files and mark keywords to give ratings.</span>
  </div>
</template>

<script>
export default {
  name: 'Root'
}
</script>

<style lang="scss" scoped>
.root {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
