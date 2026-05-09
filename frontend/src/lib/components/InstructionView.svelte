<script>
    let { instruction } = $props();
</script>

<div class="space-y-6">
    <header class="flex instructions-baseline justify-between border-b pb-4">
        <h1 class="text-4xl font-bold text-slate-900">{instruction.name}</h1>
          <code class="text-blue-700 font-semibold">{instruction.usage}</code>
    </header>

    <section>
        <h2 class="text-sm uppercase font-semibold text-slate-500 mb-2">Description</h2>
        <p class="text-slate-700 text-lg">{instruction.description}</p>
    </section>

    <div class="grid grid-cols-2 gap-4">
        <section class="bg-slate-900 p-4 rounded-lg">
            <h3 class="text-xs uppercase font-bold text-slate-400 mb-2">Example</h3>
            <code class="text-emerald-400">{instruction.example}</code>
        </section>
    </div>

  {#if instruction.warning}
    <section>
      <h1 class="nes-text is-error text-3xl">Warning / Bad Practice</h1>
      <h2 class="text-sm uppercase font-semibold text-slate-500 mb-2">Description</h2>
      <p class="text-slate-700 text-lg">{instruction.warning.about}</p>
    </section>
    <div class="grid grid-cols-2 gap-4">
      <section class="bg-slate-900 p-4 rounded-lg">
        <h3 class="text-xs uppercase font-bold text-slate-400 mb-2">Example</h3>
        <code class="text-emerald-400">{instruction.warning.code}</code>
      </section>
    </div>
  {/if}
</div>
