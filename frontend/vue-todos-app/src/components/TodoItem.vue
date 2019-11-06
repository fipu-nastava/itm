<template>
    
    <li v-bind:class="{ checked: item.checked }" @click="toggle()">

        {{item.content}}

        <span class="close" @click.stop="remove()">×</span>

    </li>

</template>

<script>
export default {
  name: "todo-item",
  props: {
    item: Object
  },
  methods: {
    toggle() {
        this.item.checked = !this.item.checked
        this.$emit("update:item", this.item)
    },
    remove() {
        this.$emit("remove:item", this.item)
    }
  }
}
</script>


<style scoped>

</style>
