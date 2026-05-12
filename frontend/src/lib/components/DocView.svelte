<!-- src/lib/components/DocViewer.svelte -->
<script>
  let { data, category } = $props();
</script>

<article class="">
  <header class="mb-10">
    <span class="text-xs font-bold tracking-widest text-blue-600 uppercase">
      {data.difficulty || 'Documentation'}
    </span>
    <h1 class="mt-2 text-4xl font-bold text-slate-900">{data.title}</h1>
    <h2 class="mt-4 text-lg text-slate-600 leading-relaxed">{data.subheading}</h2>
    {#if data.content != undefined}
      {#each data.content as item}
         <!-- content here -->
        <h3>{item.title}</h3>
        <p>{item.paragraph}</p>
      {/each}
      
    {/if}
  </header>

  {#if data.items != undefined}
    {#each Object.entries(data.items) as [key, val]}
      <a
        href="/docs/{category}/{key}"
        class="font-bold text-slate-900 block mb-1"
      >
        {key}
      </a>
    {/each}
  {/if}
</article>
