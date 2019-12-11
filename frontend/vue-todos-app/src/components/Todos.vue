<template>
  <div class="todos">
    <todo-list :todoList="userTodoList"
              @create:todo-item="createTodoItem"
              @update:todo-item="updateTodoItem"
              @remove:todo-item="removeTodoItem"
              />    
  </div>
</template>

<script>
import TodoList from "./TodoList.vue"

export default {
    name: "todos",
    components: {
        TodoList
    },
    data() {
        return {
            userTodoList: [
                {
                    id: 1,
                    content: "Your first task!",
                    created_at: new Date().toDateString(),
                    checked: false
                },
                {
                    id: 2,
                    content: "Your second task!",
                    created_at: new Date().toDateString(),
                    checked: false
                },
                {
                    id: 3,
                    content: "Your third task!",
                    created_at: new Date().toDateString(),
                    checked: false
                }
            ],
        }
    },
    methods: {
        async getTodos() {
            try {
                const response = await fetch("http://localhost:8010/users/1/tasks")
                const data = await response.json()
                console.log(data)
                this.userTodoList = data
            } catch (error) {
                console.error(error)
            }
        },

        async createTodoItem(todoItem) {
            try {

                const args = 
                    {
                        method: "POST",
                        body: JSON.stringify(todoItem),
                        headers: { "Content-type": "application/json; charset=UTF-8" },
                    }

                const response = await fetch("http://localhost:8010/users/1/tasks", args)

                const data = await response.json()
                this.userTodoList = [...this.userTodoList, data]
            } catch (error) {
                console.error(error)
            }
        },

        async updateTodoItem(todoItem) {
            try {

                const args = 
                    {
                        method: "PUT",
                        body: JSON.stringify(todoItem),
                        headers: { "Content-type": "application/json; charset=UTF-8" },
                    }

                const response = await fetch("http://localhost:8010/users/1/tasks/" + todoItem.id, args)
                const data = await response.json()

                this.userTodoList = this.userTodoList.map(ti => (ti.id === data.id ? data : ti))
            
            } catch (error) {
                console.error(error)
            }
        },

        async removeTodoItem(todoItem) {
            try {

                const args = {method: "DELETE"}

                await fetch("http://localhost:8010/users/1/tasks/" + todoItem.id, args);

                this.userTodoList = this.userTodoList.filter(ti => ti.id !== todoItem.id);
            } catch (error) {
                console.error(error);
            }
        }
    },
    mounted() {
        this.getTodos()
    }
}

</script>


<style scoped>

</style>
