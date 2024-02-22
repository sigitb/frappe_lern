<template>
    <div class="mx-20 my-4" v-if="!action.get.loading">
        <div class="flex flex-row item-center justify-between">
            <h1 class="font-black text-5xl text-gray-900">{{ action.doc.title }}</h1>
            <Button @click="router.back()">Go Back</Button>
        </div>
    </div>
    <LoadingIndicator v-else class="w-6 text-blue-500" />
</template>

<script setup>
import { Button, LoadingIndicator, createDocumentResource } from 'frappe-ui';
import { useRouter } from 'vue-router';
const router = useRouter();
const props = defineProps(['name'])

const action = createDocumentResource({
    doctype: 'Action',
    name: props.name,
})
</script>