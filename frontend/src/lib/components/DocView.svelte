<!-- src/lib/components/DocViewer.svelte -->
<script>
let { data } = $props();
</script>

<article class="max-w-3xl">
    <header class="mb-10">
        <span class="text-xs font-bold tracking-widest text-blue-600 uppercase">
            {data.difficulty || 'Documentation'}
        </span>
        <h1 class="mt-2 text-4xl font-bold text-slate-900">{data.title}</h1>
        <p class="mt-4 text-lg text-slate-600 leading-relaxed">{data.content}</p>
    </header>

    {#if data.instructions && data.instructions.length > 0}
        <section class="mt-8">
            <h2 class="text-xl font-semibold text-slate-800 mb-4">Instructions</h2>
            <ol class="space-y-4 list-decimal list-inside text-slate-700">
                {#each data.instructions as step, i}
                    <li class="pl-2 marker:text-blue-500 marker:font-bold">
                        <span class="ml-2">{step}</span>
                    </li>
                {/each}
            </ol>
        </section>
    {/if}
</article>
