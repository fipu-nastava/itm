<template>
  <div class="todo-list">
    

    <div class="header placeholder" :data-placeholder="suggestedValue">
        <h2>My To Do List</h2>
        <input v-model="newTodo" @keydown.ctrl="acceptSuggested()" @keyup.enter="addItem()" @keyup="suggest($event)" type="text" placeholder="Type your todo list...">
        <span @click="addItem()" class="add-btn">Add</span>
    </div>


    <ul>
        <todo-item v-for="item in todoList" 
                  :key="item.id" 
                  :item="item"
                  @remove:item="removeItem"
                  @update:item="updateItem"
                  />
    </ul>


  </div>
</template>

<script>
import TodoItem from "./TodoItem.vue"


export default {
    name: "todo-list",
    components: {
         TodoItem
    },
    props: {
        todoList: Array
    },
    data() {
        return {
            newTodo: "",
            suggestedValue: ""
        }
    },
    methods: {
        addItem(){

            this.newTodo = this.newTodo.trim()

            if(this.newTodo == "") return

            let newItem = {
                        // id: Math.max.apply(Math, this.todoList.map(function(o) { return o.id; })) + 1,
                        id: -1,
                        content: this.newTodo,
                        created_at: new Date().toDateString(),
                        checked: false
                    }

            // this.todoList.push(newItem)
            // this.todoList = [...this.todoList, newItem]
            this.$emit("create:todo-item", newItem)

            this.newTodo = ""
        },
        removeItem(item) {
            // this.todoList.splice(this.todoList.indexOf(item), 1);
            this.$emit("remove:todo-item", item)
        },
        updateItem(item) {
            this.$emit("update:todo-item", item)            
        },
        acceptSuggested() {

          if(this.suggestedValue != null && this.suggestedValue.length > 9)
            this.newTodo = this.suggestedValue;
        },
        suggest(event) {

          if(event.key == "Control")
            return

          if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
          }
          this.timer = setTimeout(() => {
            this.suggestTask()
          }, 800);
        },
        async suggestTask() {

        this.suggestedValue = "";

          if(this.newTodo != null && this.newTodo.length > 9){
             
             try {
                  const response = await fetch("http://localhost:8011/predict/" + this.newTodo)
                  const data = await response.json()
                  console.log(data)
                  this.suggestedValue = data.predicted
              } catch (error) {
                  console.error(error)
              }

          }
        }
    }
}
</script>


<style>
* {
  box-sizing: border-box;
}

/* Style the header */
.header {
    padding: 30px 40px;
    color: white;
    text-align: center;
    background-color: #a4a4a4;
    border-radius: 4px;
}

/* Clear floats after the header */
.header:after {
  content: "";
  display: table;
  clear: both;
}

/* Style the input */
input {
  margin: 0;
  border: none;
  border-radius: 0;
  width: 75%;
  padding: 10px;
  float: left;
  font-size: 16px;
}

/* Style the "Add" button */
.add-btn {
  padding: 10px;
  width: 25%;
  background: #d9d9d9;
  color: #555;
  float: left;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s;
  border-radius: 0;
}

.add-btn:hover {
  background-color: #bbb;
}


/* Remove margins and padding from the list */
ul {
    margin: 0;
    list-style: none;
    padding: 0;
}

/* Style the list items */
ul li {
  cursor: pointer;
  position: relative;
  padding: 12px 8px 12px 40px;
  background: #eee;
  font-size: 18px;
  transition: 0.2s;

  /* make the list items unselectable */
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Set all odd list items to a different color (zebra-stripes) */
ul li:nth-child(odd) {
  background: #f9f9f9;
}

/* Darker background-color on hover */
ul li:hover {
  background: #ddd;
}

/* When clicked on, add a background color and strike out text */
ul li.checked {
  background: #888;
  color: #fff;
  text-decoration: line-through;
}

/* Add a "checked" mark when clicked on */
ul li.checked::before {
  content: "";
  position: absolute;
  border-color: #fff;
  border-style: solid;
  border-width: 0 2px 2px 0;
  top: 10px;
  left: 16px;
  transform: rotate(45deg);
  height: 15px;
  width: 7px;
}

/* Style the close button */
.close {
  position: absolute;
  right: 0;
  top: 0;
  padding: 12px 16px 12px 16px;
}

.close:hover {
  background-color: #f44336;
  color: white;
}

.placeholder {
    position: relative;
}

.placeholder::after {
    position: relative;
    top: -29px;
    content: attr(data-placeholder);
    pointer-events: none;
    opacity: 0.6;
    left: 10px;
    color: black;
    font-size: 16px;
}


</style>
