<!-- src/lib/components/DocViewer.svelte -->
<script>
let { data } = $props();
</script>

<article class="">
    <header class="mb-10">
        <span class="text-xs font-bold tracking-widest text-blue-600 uppercase">
            {data.difficulty || 'Documentation'}
        </span>
        <h1 class="mt-2 text-4xl font-bold text-slate-900">{data.title}</h1>
        <p class="mt-4 text-lg text-slate-600 leading-relaxed">{data.content}</p>
    </header>
</article>
