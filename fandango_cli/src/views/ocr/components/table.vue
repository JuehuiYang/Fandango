<template>
  <el-table
    :data="props.tableData()"
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
