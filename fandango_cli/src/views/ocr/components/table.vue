<template>
  <el-table
    :data="props.tableData()"
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
</template>

<script>

export default {
  name: 'Table',
  data() {
    return {
      props: {
        tableData: Array
      }
    }
  }
}
</script>

<style scoped>

</style>
