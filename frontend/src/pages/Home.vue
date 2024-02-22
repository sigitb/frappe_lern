<template>
  <div class="mx-20">
    
    <div class="flex flex-row item-center justify-between">
      <h2 class="text-5xl font-black text-gray-900">Lists</h2>
      <Button icon-left="plus">New List</Button>
    </div>
    <div class="mt-2">
      <Card title="General">
        <div>
          <ul>
            <li class="flex space-y-2 flex-row item-center justify-between" v-for="action in actions.data" :key="action.title">
             <router-link :to="`/action/${action.name}`">{{ action.title }}</router-link>
             <Button icon="check" @click="complateAction(action.name)" />
            </li>
          </ul>
          <Button icon-left="plus" @click="addActionDialogShown = true">New Action</Button>
        </div>  
      </Card>
    </div>
    <Dialog v-model="addActionDialogShown">
      <template #body-title>
        <h3>Add New Action</h3>
      </template>
      <template #body-content>
        <div class="space-y-2">
          <TextInput
            :type="'text'"
            size="sm"
            variant="subtle"
            placeholder="Title"
            v-model="action.title"
          />
          <Select
            :options="categoryOptions"
            v-model="action.category"
          />
        </div>
      </template>
      <template #actions>
        <Button @click="addAction" variant="solid">
          Add Action
        </Button>
        <Button
          class="ml-2"
          @click="addActionDialogShown = false"
        >
        Cancel
        </Button>
      </template>
    </Dialog>
    <!-- <Dialog :options="{
      title:'Add New Action',
      actions: [
          {
            label: 'Add Action',
            appearance: 'primary',
            handler: ({ close }) => {
              addAction()
              close() // closes dialog
            },
          },
          { label: 'Cancel' },
        ],
      }" v-model="addActionDialogShown" >
      <template #body-content>
        <p>Custom Body</p>
      </template>
    </Dialog> -->

  </div>
</template>

<script setup>
import { Dialog,createListResource,TextInput,Select } from 'frappe-ui'
import { computed, reactive, ref } from 'vue';

const addActionDialogShown = ref(false)

const action = reactive({
  title: '',
  category: '',
})

const actions = createListResource({
  doctype:'Action',
  fields: ["name","title", "status", "description", "date", "due_date"],
  filters: {
    status:'ToDo'
  },
  limit:10
})

actions.reload()

const categories = createListResource({
  doctype: 'Category',
  fields: ["name", "title"],
  transform(categories) {
    return categories.map((c) => ({ label:c.title, value:c.name}))
  }
})

categories.reload()

const complateAction = (actionName) => {
  actions.setValue.submit({
    name: actionName,
    status:'Complated',
  })
  actions.reload()
}

const categoryOptions = computed(() => {
  if (categories.list.loading || !categories.data) {
    return []
  }
  return categories.data
})

const addAction = () => {
  actions.insert.submit(action)
  addActionDialogShown.value = false
}
</script>
