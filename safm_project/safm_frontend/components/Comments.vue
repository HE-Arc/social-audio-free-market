<template>
    <section class="comments">
        <h2>Comments</h2>
        <div
            class="comment"
            v-for="comment in comments"
            :key="comment.id"
        >
            <p>{{ comment.username }}</p>
            <p>{{ comment.text }}</p>
            <p>{{ comment.datetime }}</p>
        </div>
    </section>
</template>

<script>
export default {
    props: ['comments']
}
</script>
