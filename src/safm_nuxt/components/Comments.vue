<template>
    <div>
        <ul>
            <li
                class="comment"
                v-for="comment in comments"
                :key="comment.id"
            >
                <p>{{ comment.username }}</p>
                <p>{{ comment.text }}</p>
                <p>{{ comment.datetime }}</p>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    props: ['comments']
}
</script>
